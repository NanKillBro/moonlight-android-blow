package com.limelight.log;

import android.content.Context;
import android.os.Build;
import android.os.SystemClock;

import com.limelight.BuildConfig;
import com.limelight.preferences.PreferenceConfiguration;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.nio.charset.StandardCharsets;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Locale;
import java.util.Set;
import java.util.concurrent.ArrayBlockingQueue;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicLong;

public final class StreamSessionLogger {
    private static final int LOG_FORMAT_VERSION = 2;
    private static final int QUEUE_CAPACITY = 1024;
    private static final long FLUSH_INTERVAL_MS = 1000L;
    private static final long CLOSE_WAIT_MS = 2000L;
    private static final long MAX_SESSION_BYTES = 8L * 1024L * 1024L;
    private static final Set<String> ACTIVE_FILES = ConcurrentHashMap.newKeySet();
    private static final LogRecord POISON = new LogRecord(0L, 0L,
            "", "", "", null, true);

    private final Context appContext;
    private final File file;
    private final BufferedWriter writer;
    private final ArrayBlockingQueue<LogRecord> queue = new ArrayBlockingQueue<>(QUEUE_CAPACITY);
    private final AtomicLong droppedRecords = new AtomicLong();
    private final long sessionStartElapsedMs = SystemClock.elapsedRealtime();
    private final Thread writerThread;
    private final Thread.UncaughtExceptionHandler previousExceptionHandler;
    private final Thread.UncaughtExceptionHandler exceptionHandler;
    private volatile boolean closed;

    // Accessed only by writerThread after construction.
    private long writtenBytes;
    private long sessionLimitDroppedRecords;
    private boolean sessionLimitReported;

    public static StreamSessionLogger create(Context context, PreferenceConfiguration config,
                                             String pcName, String appName) {
        if (config == null || !config.enableStreamSessionLogging) {
            return null;
        }
        try {
            return new StreamSessionLogger(context, config, pcName, appName);
        }
        catch (IOException ignored) {
            return null;
        }
    }

    private StreamSessionLogger(Context context, PreferenceConfiguration config,
                                String pcName, String appName) throws IOException {
        appContext = context.getApplicationContext();
        file = StreamLogStore.createSessionFile(appContext, pcName, appName);
        writer = new BufferedWriter(new OutputStreamWriter(new FileOutputStream(file, true), StandardCharsets.UTF_8));
        ACTIVE_FILES.add(file.getAbsolutePath());
        previousExceptionHandler = Thread.getDefaultUncaughtExceptionHandler();
        exceptionHandler = (thread, throwable) -> {
            error("CRASH", "Java uncaught exception, thread=" + thread.getName(), throwable);
            close("Java abnormal exit");
            if (previousExceptionHandler != null) {
                previousExceptionHandler.uncaughtException(thread, throwable);
            }
        };
        Thread.setDefaultUncaughtExceptionHandler(exceptionHandler);

        writeRawDirect("Moonlight Stream Session Log");
        writeRawDirect("Log format: " + LOG_FORMAT_VERSION);
        writeRawDirect("App Version: " + BuildConfig.VERSION_NAME + " (" + BuildConfig.VERSION_CODE + ")");
        writeRawDirect("Device: " + Build.MANUFACTURER + " " + Build.MODEL + ", Android " + Build.VERSION.RELEASE
                + " (API " + Build.VERSION.SDK_INT + "), ABI " + firstAbi());
        writeRawDirect("Target: " + safe(pcName) + " / " + safe(appName));
        writeRawDirect(String.format(Locale.US,
                "Config: %dx%d@%d, Bitrate=%d Kbps, HDR=%s, USB Driver=%s, Audio Haptics=%s",
                config.width, config.height, config.fps, config.bitrate,
                onOff(config.enableHdr), onOff(config.usbDriver),
                onOff(config.enableAudioHaptics)));
        writeRawDirect("Control connection: Touch stutter compatibility=" + onOff(config.touchStutterCompatibility)
                + ", Requested RTT tolerance=" + (config.touchStutterCompatibility ? 10 : 0) + " ms");
        writeRawDirect("Haptics: Audio Output=" + safe(config.audioHapticsOutputTarget)
                + ", Strength=" + config.audioHapticsStrength + "%"
                + ", Keep Standard Rumble=" + onOff(config.audioHapticsKeepControllerRumble));
        boolean explicitDs5 = PreferenceConfiguration.GAMEPAD_EMULATION_DS5.equals(
                PreferenceConfiguration.normalizeGamepadEmulation(config.gamepadEmulation));
        writeRawDirect("Gamepad: Emulation type=" + safe(config.gamepadEmulation)
                + ", Native DS5 haptic PCM=" + onOff(explicitDs5 && config.ds5NativePcmEnabled)
                + ", DS5 speaker=" + onOff(explicitDs5 && config.ds5ControllerSpeakerEnabled));
        writeRawDirect("------------------------------------------------------------");

        writerThread = new Thread(this::runWriter, "StreamSessionLogger");
        writerThread.setDaemon(true);
        writerThread.start();
        info("SESSION", "Session log started");
    }

    public void info(String category, String message) {
        enqueue("INFO", category, message, null, false);
    }

    void important(String category, String message) {
        enqueue("INFO", category, message, null, true);
    }

    public void warn(String category, String message) {
        enqueue("WARN", category, message, null, true);
    }

    public void error(String category, String message, Throwable throwable) {
        enqueue("ERROR", category, message, throwable, true);
    }

    public synchronized void close(String reason) {
        if (closed) {
            return;
        }

        enqueueLocked(new LogRecord(System.currentTimeMillis(),
                SystemClock.elapsedRealtime() - sessionStartElapsedMs,
                "END", "SESSION", reason, null, true));
        closed = true;
        enqueueLocked(POISON);

        if (Thread.currentThread() != writerThread) {
            try {
                writerThread.join(CLOSE_WAIT_MS);
            }
            catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }

        ACTIVE_FILES.remove(file.getAbsolutePath());
        StreamLogStore.clearActive(appContext, file);
        if (Thread.getDefaultUncaughtExceptionHandler() == exceptionHandler) {
            Thread.setDefaultUncaughtExceptionHandler(previousExceptionHandler);
        }
    }

    public File getFile() {
        return file;
    }

    static boolean isFileActive(String path) {
        return path != null && ACTIVE_FILES.contains(path);
    }

    private void enqueue(String level, String category, String message,
                         Throwable throwable, boolean critical) {
        if (closed) {
            return;
        }
        LogRecord record = new LogRecord(System.currentTimeMillis(),
                SystemClock.elapsedRealtime() - sessionStartElapsedMs,
                level, category, message, throwable, critical);
        synchronized (this) {
            if (!closed) {
                enqueueLocked(record);
            }
        }
    }

    private void enqueueLocked(LogRecord record) {
        if (queue.offer(record)) {
            return;
        }

        if (!record.critical) {
            droppedRecords.incrementAndGet();
            return;
        }

        // Critical WARN/ERROR/END records preferentially displace an older low-priority entry
        // instead of blocking a network, decoder, USB, or crash-handler thread on file I/O.
        while (!queue.offer(record)) {
            LogRecord removed = removeQueuedLowPriorityRecord();
            if (removed == null) {
                // An all-critical queue is extremely unlikely. Keep the newest crash/end signal.
                removed = queue.poll();
            }
            if (removed != null && removed != POISON) {
                droppedRecords.incrementAndGet();
            }
        }
    }

    private LogRecord removeQueuedLowPriorityRecord() {
        for (LogRecord queued : queue) {
            if (!queued.critical && queue.remove(queued)) {
                return queued;
            }
        }
        return null;
    }

    private void runWriter() {
        try {
            while (true) {
                LogRecord record = queue.poll(FLUSH_INTERVAL_MS, TimeUnit.MILLISECONDS);
                if (record == null) {
                    writer.flush();
                    continue;
                }
                if (record == POISON) {
                    break;
                }

                writeDroppedRecordNotice();
                writeRecord(record);
                if (queue.isEmpty()) {
                    writer.flush();
                }
            }

            writeDroppedRecordNotice();
            writeSessionLimitNotice();
            writer.flush();
        }
        catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        catch (IOException ignored) {
        }
        finally {
            try {
                writer.flush();
                writer.close();
            }
            catch (IOException ignored) {
            }
        }
    }

    private void writeRecord(LogRecord record) throws IOException {
        String prefix = timestamp(record.wallTimeMs) + " [" + safe(record.level) + "] ["
                + safe(record.category) + "] [t=" + record.elapsedMs + "ms] ";
        writeLine(prefix + safe(record.message), record.critical);
        if (record.throwable != null) {
            writeLine(prefix + record.throwable.getClass().getName() + ": "
                    + safe(record.throwable.getMessage()), true);
            StackTraceElement[] stack = record.throwable.getStackTrace();
            for (int i = 0; i < Math.min(stack.length, 16); i++) {
                writeLine(prefix + "  at " + stack[i], true);
            }
        }
    }

    private void writeDroppedRecordNotice() throws IOException {
        long dropped = droppedRecords.getAndSet(0L);
        if (dropped > 0L) {
            writeLine(timestamp(System.currentTimeMillis()) + " [WARN] [LOGGER] [t="
                    + (SystemClock.elapsedRealtime() - sessionStartElapsedMs)
                    + "ms] Log queue congested, dropped low-priority records=" + dropped, true);
        }
    }

    private void writeSessionLimitNotice() throws IOException {
        if (sessionLimitDroppedRecords > 0L && !sessionLimitReported) {
            sessionLimitReported = true;
            writeLine(timestamp(System.currentTimeMillis()) + " [WARN] [LOGGER] [t="
                    + (SystemClock.elapsedRealtime() - sessionStartElapsedMs)
                    + "ms] Session log reached the 8 MiB limit, omitted normal records="
                    + sessionLimitDroppedRecords, true);
        }
    }

    private void writeRawDirect(String value) throws IOException {
        writeLine(value, true);
        writer.flush();
    }

    private void writeLine(String value, boolean critical) throws IOException {
        byte[] encoded = value.getBytes(StandardCharsets.UTF_8);
        if (!critical && writtenBytes + encoded.length + 2L > MAX_SESSION_BYTES) {
            sessionLimitDroppedRecords++;
            return;
        }
        if (critical && sessionLimitDroppedRecords > 0L && !sessionLimitReported) {
            writeSessionLimitNotice();
        }
        writer.write(value);
        writer.newLine();
        writtenBytes += encoded.length + 2L;
    }

    private static String timestamp(long wallTimeMs) {
        return new SimpleDateFormat("yyyy-MM-dd HH:mm:ss.SSS", Locale.US)
                .format(new Date(wallTimeMs));
    }

    private static String safe(String value) {
        return value == null || value.trim().isEmpty() ? "--" : value.replace('\n', ' ').replace('\r', ' ');
    }

    private static String onOff(boolean enabled) {
        return enabled ? "On" : "Off";
    }

    private static String firstAbi() {
        return Build.SUPPORTED_ABIS.length > 0 ? Build.SUPPORTED_ABIS[0] : Build.CPU_ABI;
    }

    private static final class LogRecord {
        final long wallTimeMs;
        final long elapsedMs;
        final String level;
        final String category;
        final String message;
        final Throwable throwable;
        final boolean critical;

        LogRecord(long wallTimeMs, long elapsedMs, String level, String category,
                  String message, Throwable throwable, boolean critical) {
            this.wallTimeMs = wallTimeMs;
            this.elapsedMs = elapsedMs;
            this.level = level;
            this.category = category;
            this.message = message;
            this.throwable = throwable;
            this.critical = critical;
        }
    }
}
