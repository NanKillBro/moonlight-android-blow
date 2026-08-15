package com.limelight.log;

import android.content.Context;
import android.os.Build;

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
import java.util.concurrent.ConcurrentHashMap;

public final class StreamSessionLogger {
    private static final Set<String> ACTIVE_FILES = ConcurrentHashMap.newKeySet();

    private final Context appContext;
    private final File file;
    private final BufferedWriter writer;
    private final Thread.UncaughtExceptionHandler previousExceptionHandler;
    private final Thread.UncaughtExceptionHandler exceptionHandler;
    private boolean closed;

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

        writeRaw("Moonlight Stream Session Log");
        writeRaw("App Version: " + BuildConfig.VERSION_NAME + " (" + BuildConfig.VERSION_CODE + ")");
        writeRaw("Device: " + Build.MANUFACTURER + " " + Build.MODEL + ", Android " + Build.VERSION.RELEASE
                + " (API " + Build.VERSION.SDK_INT + "), ABI " + firstAbi());
        writeRaw("Target: " + safe(pcName) + " / " + safe(appName));
        writeRaw(String.format(Locale.US,
                "Config: %dx%d@%d, Bitrate=%d Kbps, HDR=%s, USB Driver=%s, Audio Haptics=%s",
                config.width, config.height, config.fps, config.bitrate,
                onOff(config.enableHdr), onOff(config.usbDriver),
                onOff(config.enableAudioHaptics)));
        writeRaw("Haptics: Audio Output=" + safe(config.audioHapticsOutputTarget)
                + ", Strength=" + config.audioHapticsStrength + "%"
                + ", Keep Standard Rumble=" + onOff(config.audioHapticsKeepControllerRumble));
        writeRaw("------------------------------------------------------------");
        info("SESSION", "Session log started");
    }

    public synchronized void info(String category, String message) {
        write("INFO", category, message, null);
    }

    public synchronized void warn(String category, String message) {
        write("WARN", category, message, null);
    }

    public synchronized void error(String category, String message, Throwable throwable) {
        write("ERROR", category, message, throwable);
    }

    public synchronized void close(String reason) {
        if (closed) {
            return;
        }
        write("END", "SESSION", reason, null);
        closed = true;
        try {
            writer.close();
        }
        catch (IOException ignored) {
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

    private void write(String level, String category, String message, Throwable throwable) {
        if (closed) {
            return;
        }
        String prefix = timestamp() + " [" + level + "] [" + safe(category) + "] ";
        try {
            writer.write(prefix + safe(message));
            writer.newLine();
            if (throwable != null) {
                writer.write(prefix + throwable.getClass().getName() + ": " + safe(throwable.getMessage()));
                writer.newLine();
                StackTraceElement[] stack = throwable.getStackTrace();
                for (int i = 0; i < Math.min(stack.length, 16); i++) {
                    writer.write(prefix + "  at " + stack[i]);
                    writer.newLine();
                }
            }
            writer.flush();
        }
        catch (IOException ignored) {
        }
    }

    private void writeRaw(String value) {
        try {
            writer.write(value);
            writer.newLine();
            writer.flush();
        }
        catch (IOException ignored) {
        }
    }

    private static String timestamp() {
        return new SimpleDateFormat("yyyy-MM-dd HH:mm:ss.SSS", Locale.US).format(new Date());
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
}
