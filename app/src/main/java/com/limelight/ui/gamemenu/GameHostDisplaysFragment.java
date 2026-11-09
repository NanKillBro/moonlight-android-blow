package com.limelight.ui.gamemenu;

import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.os.SystemClock;
import android.view.View;
import android.widget.LinearLayout;
import android.widget.ScrollView;
import android.widget.TextView;

import com.limelight.Game;
import com.limelight.R;
import com.limelight.nvstream.http.HostDisplayApiUnavailableException;
import com.limelight.ui.BaseFragmentDialog.BaseGameMenuDialog;
import com.limelight.utils.UiHelper;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.Locale;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

/** Paired PC displays, using the same rows and independent sheets as the game display menu. */
public class GameHostDisplaysFragment extends BaseGameMenuDialog {
    private final Handler main = new Handler(Looper.getMainLooper());
    private ExecutorService worker;
    private LinearLayout content;
    private ScrollView scroll;
    private TextView status;
    private JSONArray devices = new JSONArray();
    private String selectedId = "";
    private String lastInventory = "";
    private boolean busy;
    private final HostDisplayCaptureState captureSwitch = new HostDisplayCaptureState();
    private int generation;
    private final Runnable refresh = () -> load(null, null);

    @Override public int getLayoutRes() {
        return R.layout.dialog_game_menu_host_displays;
    }

    @Override public void bindView(View view) {
        super.bindView(view);
        worker = Executors.newSingleThreadExecutor();
        content = view.findViewById(R.id.host_displays_content);
        scroll = view.findViewById(R.id.host_displays_scroll);
        status = view.findViewById(R.id.host_displays_status);
        view.findViewById(R.id.ibtn_back).setOnClickListener(v -> dismiss());
        view.findViewById(R.id.host_displays_refresh).setOnClickListener(v -> load(null, null));
        load(null, null);
    }

    @Override public void onSaveInstanceState(Bundle out) {
        super.onSaveInstanceState(out);
        out.putString("selected_id", selectedId);
    }

    @Override public void onCreate(Bundle savedState) {
        super.onCreate(savedState);
        if (savedState != null) selectedId = savedState.getString("selected_id", "");
    }

    private boolean choicesOpen() {
        return getFragmentManager() != null && getFragmentManager()
                .findFragmentByTag(GameHostDisplayChoiceFragment.TAG) != null;
    }

    /** Keep HTTP off the UI thread, suspend polling behind a choice sheet and reject stale replies. */
    private void load(JSONObject operation, GameHostDisplayChoiceFragment choice) {
        if (busy || content == null || !(getActivity() instanceof Game)) {
            if (choice != null) choice.complete(false, "Reading displays. Try again in a moment.");
            return;
        }
        if (operation == null && choicesOpen()) return;
        busy = true;
        main.removeCallbacks(refresh);
        int requestGeneration = generation;
        Game game = (Game) getActivity();
        if (operation != null) showStatus(captureSwitch.isPending()
                ? "Switching streaming display…" : "Applying host display settings…");
        worker.execute(() -> {
            JSONObject inventory = null;
            String failure = null;
            boolean legacyHost = false;
            try {
                if (operation != null) {
                    JSONObject applied = game.requestHostDisplays(operation);
                    if (!applied.optBoolean("status")) {
                        failure = applied.optString("message", "The host rejected this setting");
                    }
                }
                inventory = game.requestHostDisplays(null);
                if (!inventory.optBoolean("status")) {
                    throw new java.io.IOException(inventory.optString("message", "Unable to read displays"));
                }
            } catch (Exception error) {
                legacyHost = operation == null && error instanceof HostDisplayApiUnavailableException;
                failure = error instanceof java.io.FileNotFoundException
                        ? "Update the StarCore PC host to use display management"
                        : error.getMessage() == null ? "Unable to connect to the host" : error.getMessage();
            }
            JSONObject result = inventory;
            String error = failure;
            boolean useLegacyControls = legacyHost;
            main.post(() -> {
                if (generation != requestGeneration || content == null || !isAdded()) return;
                busy = false;
                if (useLegacyControls && getTargetFragment() instanceof GameMenuFragment
                        && getDialog() != null && getDialog().isShowing()) {
                    game.markHostDisplayApiUnavailable();
                    captureSwitch.failed();
                    main.removeCallbacks(refresh);
                    ((GameMenuFragment) getTargetFragment()).showLegacyDisplayControls();
                    dismiss();
                    return;
                }
                if (result != null && result.optBoolean("status")) {
                    JSONArray list = result.optJSONArray("devices");
                    devices = list == null ? new JSONArray() : list;
                }
                if (error != null) {
                    captureSwitch.failed();
                    showStatus("Read or apply failed: " + error + ". Tap Refresh to try again.");
                    render();
                    if (choice != null) choice.complete(false, error);
                    return;
                }
                String capturedId = "";
                boolean targetActive = false;
                for (int i = 0; i < devices.length(); i++) {
                    JSONObject row = devices.optJSONObject(i);
                    if (row == null) continue;
                    if (row.optBoolean("active") && row.optBoolean("capturing")) capturedId = row.optString("device_id");
                    if (captureSwitch.pendingId().equals(row.optString("device_id"))) targetActive = row.optBoolean("active");
                }
                HostDisplayCaptureState.Result switched = captureSwitch.observe(capturedId, targetActive,
                        SystemClock.elapsedRealtime());
                if (switched == HostDisplayCaptureState.Result.UNAVAILABLE
                        || switched == HostDisplayCaptureState.Result.TIMED_OUT) {
                    showStatus(switched == HostDisplayCaptureState.Result.UNAVAILABLE
                            ? "The target display disconnected before the switch completed. Tap Refresh to try again."
                            : "The switch is not complete yet. Check the current stream image, then tap Refresh to try again.");
                    render();
                    return;
                }
                if (captureSwitch.isPending()) {
                    showStatus("Switching streaming display…");
                } else {
                    status.setVisibility(devices.length() == 0 ? View.VISIBLE : View.GONE);
                    status.setText("No displays are currently available on the PC");
                }
                if (!devices.toString().equals(lastInventory) || operation != null || content.getChildCount() == 0
                        || switched == HostDisplayCaptureState.Result.COMPLETE) {
                    lastInventory = devices.toString();
                    render();
                }
                if (choice != null) choice.complete(true, null);
                if (!choicesOpen()) main.postDelayed(refresh, captureSwitch.isPending() ? 500 : 2500);
            });
        });
    }

    private void showStatus(String message) {
        status.setVisibility(View.VISIBLE);
        status.setText(message);
    }

    private JSONObject selected() {
        JSONObject previous = null;
        JSONObject capturing = null;
        for (int i = 0; i < devices.length(); i++) {
            JSONObject row = devices.optJSONObject(i);
            if (row != null && selectedId.equals(row.optString("device_id"))) previous = row;
            if (row != null && row.optBoolean("active") && row.optBoolean("capturing")) capturing = row;
        }
        JSONObject result = capturing != null ? capturing : previous != null ? previous : devices.optJSONObject(0);
        if (result != null) selectedId = result.optString("device_id");
        return result;
    }

    /** Preserve the main sheet's selection, focus and scroll position when inventory changes. */
    private void render() {
        if (content == null) return;
        int scrollY = scroll.getScrollY();
        View focused = content.findFocus();
        Object focusedTag = focused == null ? null : focused.getTag();
        content.removeAllViews();
        JSONObject device = selected();
        if (device == null) return;
        HostDisplayMenuViews.section(content, "Displays");
        for (int i = 0; i < devices.length(); i++) {
            JSONObject row = devices.optJSONObject(i);
            if (row == null) continue;
            String id = row.optString("device_id");
            String detail = row.optBoolean("primary") ? "Primary" : "";
            if (row.optBoolean("capturing")) detail += (detail.isEmpty() ? "" : " · ") + "Streaming";
            if (!row.optBoolean("active")) detail += (detail.isEmpty() ? "" : " · ") + "Disabled";
            HostDisplayMenuViews.row(content, row.optString("name", "Display"), detail, "", "device-" + id,
                    row.optBoolean("active") && row.optBoolean("capturing"), false,
                    row.optBoolean("active") && !captureSwitch.isPending(),
                    () -> submitCapture(id, row.optBoolean("active"), row.optBoolean("capturing")));
        }
        HostDisplayMenuViews.section(content, "Display Settings");
        boolean active = device.optBoolean("active");
        boolean editable = active && !captureSwitch.isPending();
        JSONArray modes = device.optJSONArray("modes");
        boolean hasModes = editable && modes != null && modes.length() > 0;
        parameter("Resolution", active ? device.optInt("width") + " × " + device.optInt("height") : "Disabled",
                "resolution", hasModes);
        parameter("Refresh Rate", active ? hz(device.optDouble("refresh_hz")) + " Hz" : "Disabled", "refresh", hasModes);
        JSONArray scales = device.optJSONArray("scale_options");
        parameter("Scale", device.isNull("scale_percent") ? "Unavailable" : device.optInt("scale_percent") + "%",
                "scale", editable && scales != null && scales.length() > 0);
        boolean hdr = device.optBoolean("hdr_supported");
        parameter("HDR", hdr ? device.optBoolean("hdr_enabled") ? "On" : "Off" : "Unsupported", "hdr", editable && hdr);
        HostDisplayMenuViews.note(content, "These settings apply to the PC display and are configured separately from stream resolution and frame rate.");
        if (focusedTag != null) {
            View restored = content.findViewWithTag(focusedTag);
            if (restored != null) restored.requestFocus();
        }
        scroll.post(() -> { if (scroll != null) scroll.scrollTo(0, scrollY); });
    }

    private void parameter(String label, String value, String kind, boolean enabled) {
        HostDisplayMenuViews.row(content, label, "", value, kind, false, true, enabled, () -> choose(kind));
    }

    private void choose(String kind) {
        if (busy || captureSwitch.isPending() || choicesOpen()) return;
        JSONObject device = selected();
        if (device == null) return;
        main.removeCallbacks(refresh);
        GameHostDisplayChoiceFragment choice = new GameHostDisplayChoiceFragment();
        Bundle arguments = new Bundle();
        arguments.putString("device", device.toString());
        arguments.putString("kind", kind);
        choice.setArguments(arguments);
        choice.setTargetFragment(this, 0);
        choice.setWidth(UiHelper.dpToPx(getActivity(), 364));
        choice.show(getFragmentManager(), GameHostDisplayChoiceFragment.TAG);
    }

    /** Apply a choice using the exact device ID and supported mode captured by its own sheet. */
    void submitChoice(JSONObject operation, GameHostDisplayChoiceFragment choice) {
        load(operation, choice);
    }

    void onChoiceDismissed() {
        if (content != null) {
            main.removeCallbacks(refresh);
            main.postDelayed(refresh, 300);
        }
    }

    /** A monitor-row click starts the switch; the green dot follows host capture observations only. */
    private void submitCapture(String id, boolean active, boolean capturing) {
        if (busy) return;
        try {
            JSONObject operation = new JSONObject().put("device_id", id).put("action", "capture");
            if (!captureSwitch.request(id, active, capturing, SystemClock.elapsedRealtime())) return;
            render();
            load(operation, null);
        } catch (JSONException error) {
            captureSwitch.failed();
            showStatus("Invalid display settings");
        }
    }

    private String hz(double value) {
        return String.format(Locale.US, Math.abs(value - Math.round(value)) < 0.01 ? "%.0f" : "%.2f", value);
    }

    @Override public void onDestroyView() {
        ++generation;
        main.removeCallbacks(refresh);
        if (worker != null) worker.shutdownNow();
        content = null;
        scroll = null;
        busy = false;
        captureSwitch.failed();
        lastInventory = "";
        super.onDestroyView();
    }
}
