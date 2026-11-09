#!/usr/bin/env python3
"""Re-apply English translations for strings added in upstream 261107.

Each entry maps one original Chinese source line to its English replacement.
Matching is done per line and the original CRLF/LF terminator is kept, so
this script is idempotent and safe to run after every upstream sync.
"""

import os


FILE_REPLACEMENTS = {
    'app/src/main/java/com/limelight/Game.java': [
        ('            addPerfRow("USB/IP地址", buildUsbIpAddressText(), true);', '            addPerfRow("USB/IP Address", buildUsbIpAddressText(), true);'),
        ('            addPerfRow("系统HDR峰值亮度", buildHdrTargetPeakLuminanceText(hdrDisplay));', '            addPerfRow("System HDR Peak Brightness", buildHdrTargetPeakLuminanceText(hdrDisplay));'),
        ('                addPerfRow("HDR/SDR比率", hdrSdrRatioText);', '                addPerfRow("HDR/SDR Ratio", hdrSdrRatioText);'),
        ('            addPerfRow("主机HDR母版峰值",', '            addPerfRow("Host HDR Mastering Peak",'),
        ('        addPerfRow("USB/IP地址", buildUsbIpAddressText(), true);', '        addPerfRow("USB/IP Address", buildUsbIpAddressText(), true);'),
        ('            return "系统未报告";', '            return "Not reported by system";'),
        ('                return "系统未报告";', '                return "Not reported by system";'),
        ('                : "主机未提供";', '                : "Not provided by host";'),
        ('                        + "延迟 %d±%d ms, 视频帧丢失 %.2f%%, 解码 %.2f ms, 主机 %.2f ms, "', '                        + "Latency %d±%d ms, video frame loss %.2f%%, decode %.2f ms, host %.2f ms, "'),
        ('                        + "统计年龄 %d ms",', '                        + "stats age %d ms",'),
        ('                + "；系统手柄=" + (controllerHandler != null', '                + "; System Gamepad=" + (controllerHandler != null'),
        ('                        ? controllerHandler.getSystemControllerDiagnosticsDisplayName() : "未初始化")', '                        ? controllerHandler.getSystemControllerDiagnosticsDisplayName() : "not initialized")'),
        ('            throw new java.io.IOException("串流已断开");', '            throw new java.io.IOException("Stream disconnected");'),
    ],
    'app/src/main/java/com/limelight/binding/input/ControllerHandler.java': [
        ('            markNativeGameHapticsOutput("原生PCM", outputDevices);', '            markNativeGameHapticsOutput("Native PCM", outputDevices);'),
        ('            return "无";', '            return "None";'),
    ],
    'app/src/main/java/com/limelight/log/StreamSessionLogger.java': [
        ('        writeRawDirect("日志格式: " + LOG_FORMAT_VERSION);', '        writeRawDirect("Log format: " + LOG_FORMAT_VERSION);'),
        ('        writeRawDirect("控制连接: 触控卡顿兼容=" + onOff(config.touchStutterCompatibility)', '        writeRawDirect("Control connection: Touch stutter compatibility=" + onOff(config.touchStutterCompatibility)'),
        ('                + ", 请求RTT容忍=" + (config.touchStutterCompatibility ? 10 : 0) + " ms");', '                + ", Requested RTT tolerance=" + (config.touchStutterCompatibility ? 10 : 0) + " ms");'),
        ('        writeRawDirect("手柄: 串流类型=" + safe(config.gamepadEmulation)', '        writeRawDirect("Gamepad: Emulation type=" + safe(config.gamepadEmulation)'),
        ('                + ", 原生DS5触觉PCM=" + onOff(explicitDs5 && config.ds5NativePcmEnabled)', '                + ", Native DS5 haptic PCM=" + onOff(explicitDs5 && config.ds5NativePcmEnabled)'),
        ('                + ", DS5扬声器=" + onOff(explicitDs5 && config.ds5ControllerSpeakerEnabled));', '                + ", DS5 speaker=" + onOff(explicitDs5 && config.ds5ControllerSpeakerEnabled));'),
        ('                    + "ms] 日志队列拥塞，已丢弃低优先级记录=" + dropped, true);', '                    + "ms] Log queue congested, dropped low-priority records=" + dropped, true);'),
        ('                    + "ms] 单会话日志达到 8 MiB 上限，已省略普通记录="', '                    + "ms] Session log reached the 8 MiB limit, omitted normal records="'),
    ],
    'app/src/main/java/com/limelight/nvstream/http/HostDisplayApiUnavailableException.java': [
        ('        super("此主机不支持显示器管理接口");', '        super("This host does not support the display management API");'),
        ('        return new HostHttpResponseException(status, "显示器管理请求失败");', '        return new HostHttpResponseException(status, "Display management request failed");'),
    ],
    'app/src/main/java/com/limelight/nvstream/http/NvHTTP.java': [
        ('                throw new IOException("主机返回空的显示器管理响应");', '                throw new IOException("Host returned an empty display management response");'),
        ('                    throw new IOException("主机返回无效的显示器管理响应", error);', '                    throw new IOException("Host returned an invalid display management response", error);'),
    ],
    'app/src/main/java/com/limelight/preferences/SettingsCatalog.java': [
        ('        new Group("显示", "分辨率、帧率与画面增强",', '        new Group("Display", "Resolution, frame rate, and image enhancements",'),
        ('            new Section("视频参数", "list_resolution", "list_fps", "seekbar_bitrate_kbps", "video_format", "vdValue"),', '            new Section("Video Settings", "list_resolution", "list_fps", "seekbar_bitrate_kbps", "video_format", "vdValue"),'),
        ('            new Section("画面布局", "checkbox_stretch_video", "checkbox_cutout_mode_video",', '            new Section("Layout", "checkbox_stretch_video", "checkbox_cutout_mode_video",'),
        ('            new Section("画面增强", "list_video_render_mode", "list_fsr_target", "list_fsr_sharpness",', '            new Section("Image Enhancements", "list_video_render_mode", "list_fsr_target", "list_fsr_sharpness",'),
        ('            new Section("兼容与性能", "frame_pacing", "enable_lowLatency_experiment",', '            new Section("Compatibility & Performance", "frame_pacing", "enable_lowLatency_experiment",'),
        ('        new Group("外设", "USB 共享、手柄映射、体感与震动",', '        new Group("Peripherals", "USB sharing, gamepad mapping, motion, and rumble",'),
        ('            new Section("USB 外设共享", "checkbox_usbip_mode"),', '            new Section("USB Peripheral Sharing", "checkbox_usbip_mode"),'),
        ('            new Section("连接与映射", "list_gamepad_emulation", "checkbox_multi_controller", "seekbar_deadzone",', '            new Section("Connection & Mapping", "list_gamepad_emulation", "checkbox_multi_controller", "seekbar_deadzone",'),
        ('            new Section("鼠标与体感", "checkbox_mouse_emulation", "analog_scrolling",', '            new Section("Mouse & Motion", "checkbox_mouse_emulation", "analog_scrolling",'),
        ('            new Section("震动与 DualSense", "checkbox_flip_rumble_ff", "checkbox_enable_device_rumble",', '            new Section("Rumble & DualSense", "checkbox_flip_rumble_ff", "checkbox_enable_device_rumble",'),
        ('        new Group("触摸与鼠标", "触屏、鼠标与实体键盘",', '        new Group("Touch & Mouse", "Touchscreen, mouse, and physical keyboard",'),
        ('            new Section("鼠标与触屏", "mouse_model_list_axi", "checkbox_touch_stutter_compatibility", "checkbox_mouse_local_cursor",', '            new Section("Mouse & Touchscreen", "mouse_model_list_axi", "checkbox_touch_stutter_compatibility", "checkbox_mouse_local_cursor",'),
        ('            new Section("实体键盘与辅助输入", "checkbox_keyboard_esc_opens_game_menu",', '            new Section("Physical Keyboard & Assistive Input", "checkbox_keyboard_esc_opens_game_menu",'),
        ('        new Group("声音", "声道与播放位置",', '        new Group("Audio", "Channels and playback location",'),
        ('            new Section("音频输出", "list_audio_config", "checkbox_enable_audiofx", "checkbox_host_audio")),', '            new Section("Audio Output", "list_audio_config", "checkbox_enable_audiofx", "checkbox_host_audio")),'),
        ('        new Group("音频震动", "输出目标、强度与语音过滤",', '        new Group("Audio Haptics", "Output target, strength, and voice filter",'),
        ('            new Section("音频震动", "checkbox_enable_audio_haptics", "list_audio_haptics_output_target",', '            new Section("Audio Haptics", "checkbox_enable_audio_haptics", "list_audio_haptics_output_target",'),
        ('        new Group("虚拟按键", "屏幕按键与完整键盘",', '        new Group("Virtual Buttons", "On-screen buttons and full keyboard",'),
        ('            new Section("屏幕按键", "checkbox_enable_keyboard", "keyboard_axi_list", "checkbox_vibrate_keyboard"),', '            new Section("On-screen Buttons", "checkbox_enable_keyboard", "keyboard_axi_list", "checkbox_vibrate_keyboard"),'),
        ('            new Section("完整键盘", "seekbar_keyboard_axi_opacity", "seekbar_keyboard_axi_height",', '            new Section("Full Keyboard", "seekbar_keyboard_axi_opacity", "seekbar_keyboard_axi_height",'),
        ('            new Section("按键配置", "import_keyboard_file", "export_keyboard_file")),', '            new Section("Button Configuration", "import_keyboard_file", "export_keyboard_file")),'),
        ('        new Group("虚拟手柄", "布局、透明度与触感",', '        new Group("Virtual Gamepad", "Layout, opacity, and haptics",'),
        ('            new Section("屏幕手柄", "checkbox_show_onscreen_controls", "gamepad_axi_list", "seekbar_osc_opacity",', '            new Section("On-screen Gamepad", "checkbox_show_onscreen_controls", "gamepad_axi_list", "seekbar_osc_opacity",'),
        ('            new Section("手柄配置", "import_gamepad_file", "export_gamepad_file")),', '            new Section("Gamepad Configuration", "import_gamepad_file", "export_gamepad_file")),'),
        ('        new Group("悬浮信息", "性能数据与悬浮球",', '        new Group("Overlay Info", "Performance stats and floating button",'),
        ('            new Section("性能信息", "performance_overlay_mode", "list_perf_overlay_lite_position",', '            new Section("Performance Info", "performance_overlay_mode", "list_perf_overlay_lite_position",'),
        ('            new Section("悬浮球", "checkbox_enable_ax_floating")),', '            new Section("Floating Button", "checkbox_enable_ax_floating")),'),
        ('        new Group("备份与恢复", "导出或导入主机配对数据",', '        new Group("Backup & Restore", "Export or import host pairing data",'),
        ('            new Section("主机与配对数据", "export_pairing_backup", "import_pairing_backup")),', '            new Section("Host & Pairing Data", "export_pairing_backup", "import_pairing_backup")),'),
        ('        new Group("日志采集", "记录串流并管理日志文件",', '        new Group("Logging", "Record streams and manage log files",'),
        ('            new Section("串流日志", "checkbox_enable_stream_session_logging", "manage_stream_session_logs"),', '            new Section("Stream Logs", "checkbox_enable_stream_session_logging", "manage_stream_session_logs"),'),
        ('            new Section("输入调试", "checkbox_enable_accessibility_show_log")),', '            new Section("Input Debugging", "checkbox_enable_accessibility_show_log")),'),
        ('        new Group("界面与通用", "语言、首页与应用行为",', '        new Group("Interface & General", "Language, home screen, and app behavior",'),
        ('            new Section("界面", "list_languages", "change_screen_label_key",', '            new Section("Interface", "list_languages", "change_screen_label_key",'),
        ('            new Section("应用行为", "checkbox_enable_pip", "checkbox_enable_exdisplay",', '            new Section("App Behavior", "checkbox_enable_pip", "checkbox_enable_exdisplay",'),
    ],
    'app/src/main/java/com/limelight/preferences/SettingsPanelDialog.java': [
        ('                        row("性能信息", null, hudLabel(), null, key, () -> openEditor(key));', '                        row("Performance Info", null, hudLabel(), null, key, () -> openEditor(key));'),
        ('            title.setText("性能信息");', '            title.setText("Performance Info");'),
        ('            String[] labels = {"关闭", "精简", "完整"};', '            String[] labels = {"Off", "Compact", "Full"};'),
        ('        return new String[] {"关闭", "精简", "完整"}[mode];', '        return new String[] {"Off", "Compact", "Full"}[mode];'),
        ('            row.setContentDescription(label + (checked ? "，已开启" : "，已关闭")', '            row.setContentDescription(label + (checked ? ", on" : ", off")'),
        ('                    + (TextUtils.isEmpty(detail) ? "" : "，" + detail));', '                    + (TextUtils.isEmpty(detail) ? "" : ", " + detail));'),
    ],
    'app/src/main/java/com/limelight/preferences/SettingsProfilePicker.java': [
        ('            item.setContentDescription(profileName + (i == active ? "，已选中" : "，未选中"));', '            item.setContentDescription(profileName + (i == active ? ", selected" : ", not selected"));'),
    ],
    'app/src/main/java/com/limelight/ui/gamemenu/GameHostDisplayChoiceFragment.java': [
        ('            status.setText("无法读取显示参数，请返回刷新后重试");', '            status.setText("Unable to read display settings. Go back, refresh, and try again.");'),
        ('            case "resolution": return "分辨率";', '            case "resolution": return "Resolution";'),
        ('            case "refresh": return "刷新率";', '            case "refresh": return "Refresh Rate";'),
        ('            case "scale": return "缩放比例";', '            case "scale": return "Scale";'),
        ('            choices.add(new Choice("on", "开启", operation("hdr").put("enabled", true)));', '            choices.add(new Choice("on", "On", operation("hdr").put("enabled", true)));'),
        ('            choices.add(new Choice("off", "关闭", operation("hdr").put("enabled", false)));', '            choices.add(new Choice("off", "Off", operation("hdr").put("enabled", false)));'),
        ('        HostDisplayMenuViews.section(content, "可用" + title());', '        HostDisplayMenuViews.section(content, "Available " + title());'),
        ('            status.setText("正在应用主机显示设置…");', '            status.setText("Applying host display settings…");'),
        ('            status.setText("此显示器暂无可用选项，请返回刷新后重试。");', '            status.setText("No options are available for this display. Go back, refresh, and try again.");'),
        ('            status.setText(device.optInt("width") + " × " + device.optInt("height") + " · 点击刷新率即可应用。");', '            status.setText(device.optInt("width") + " × " + device.optInt("height") + " · Tap a refresh rate to apply.");'),
        ('            status.setText("点击选项即可应用到 PC 显示器。");', '            status.setText("Tap an option to apply it to the PC display.");'),
        ('            status.setText("显示器页面已关闭，请返回重试");', '            status.setText("The display page was closed. Go back and try again.");'),
        ('            status.setText("应用失败：" + error);', '            status.setText("Apply failed: " + error);'),
    ],
    'app/src/main/java/com/limelight/ui/gamemenu/GameHostDisplaysFragment.java': [
        ('            if (choice != null) choice.complete(false, "正在读取显示器，请稍后重试");', '            if (choice != null) choice.complete(false, "Reading displays. Try again in a moment.");'),
        ('                ? "正在切换串流显示器…" : "正在应用主机显示设置…");', '                ? "Switching streaming display…" : "Applying host display settings…");'),
        ('                        failure = applied.optString("message", "主机拒绝了这项设置");', '                        failure = applied.optString("message", "The host rejected this setting");'),
        ('                    throw new java.io.IOException(inventory.optString("message", "无法读取显示器"));', '                    throw new java.io.IOException(inventory.optString("message", "Unable to read displays"));'),
        ('                        ? "请更新 StarCore星核 PC 端以使用显示器管理"', '                        ? "Update the StarCore PC host to use display management"'),
        ('                        : error.getMessage() == null ? "无法连接主机" : error.getMessage();', '                        : error.getMessage() == null ? "Unable to connect to the host" : error.getMessage();'),
        ('                    showStatus("读取或应用失败：" + error + "，可点击刷新重试");', '                    showStatus("Read or apply failed: " + error + ". Tap Refresh to try again.");'),
        ('                            ? "目标显示器已断开，未完成切换，可点击刷新重试"', '                            ? "The target display disconnected before the switch completed. Tap Refresh to try again."'),
        ('                            : "切换尚未完成，请确认当前串流画面后刷新重试");', '                            : "The switch is not complete yet. Check the current stream image, then tap Refresh to try again.");'),
        ('                    showStatus("正在切换串流显示器…");', '                    showStatus("Switching streaming display…");'),
        ('                    status.setText("PC 当前没有可用显示器");', '                    status.setText("No displays are currently available on the PC");'),
        ('        HostDisplayMenuViews.section(content, "显示器");', '        HostDisplayMenuViews.section(content, "Displays");'),
        ('            String detail = row.optBoolean("primary") ? "主屏" : "";', '            String detail = row.optBoolean("primary") ? "Primary" : "";'),
        ('            if (row.optBoolean("capturing")) detail += (detail.isEmpty() ? "" : " · ") + "正在串流";', '            if (row.optBoolean("capturing")) detail += (detail.isEmpty() ? "" : " · ") + "Streaming";'),
        ('            if (!row.optBoolean("active")) detail += (detail.isEmpty() ? "" : " · ") + "未启用";', '            if (!row.optBoolean("active")) detail += (detail.isEmpty() ? "" : " · ") + "Disabled";'),
        ('            HostDisplayMenuViews.row(content, row.optString("name", "显示器"), detail, "", "device-" + id,', '            HostDisplayMenuViews.row(content, row.optString("name", "Display"), detail, "", "device-" + id,'),
        ('        HostDisplayMenuViews.section(content, "显示参数");', '        HostDisplayMenuViews.section(content, "Display Settings");'),
        ('        parameter("分辨率", active ? device.optInt("width") + " × " + device.optInt("height") : "未启用",', '        parameter("Resolution", active ? device.optInt("width") + " × " + device.optInt("height") : "Disabled",'),
        ('        parameter("刷新率", active ? hz(device.optDouble("refresh_hz")) + " Hz" : "未启用", "refresh", hasModes);', '        parameter("Refresh Rate", active ? hz(device.optDouble("refresh_hz")) + " Hz" : "Disabled", "refresh", hasModes);'),
        ('        parameter("缩放比例", device.isNull("scale_percent") ? "不可用" : device.optInt("scale_percent") + "%",', '        parameter("Scale", device.isNull("scale_percent") ? "Unavailable" : device.optInt("scale_percent") + "%",'),
        ('        parameter("HDR", hdr ? device.optBoolean("hdr_enabled") ? "开启" : "关闭" : "不支持", "hdr", editable && hdr);', '        parameter("HDR", hdr ? device.optBoolean("hdr_enabled") ? "On" : "Off" : "Unsupported", "hdr", editable && hdr);'),
        ('        HostDisplayMenuViews.note(content, "以上设置作用于 PC 显示器，与串流分辨率和帧率分别设置。");', '        HostDisplayMenuViews.note(content, "These settings apply to the PC display and are configured separately from stream resolution and frame rate.");'),
        ('            showStatus("显示设置参数无效");', '            showStatus("Invalid display settings");'),
    ],
    'app/src/main/java/com/limelight/ui/gamemenu/HostDisplayMenuViews.java': [
        ('        row.setContentDescription(title + (subtitle.isEmpty() ? "" : "，" + subtitle)', '        row.setContentDescription(title + (subtitle.isEmpty() ? "" : ", " + subtitle)'),
        ('                + (value.isEmpty() ? "" : "，" + value) + (selected ? "，已选中" : ""));', '                + (value.isEmpty() ? "" : ", " + value) + (selected ? ", selected" : ""));'),
    ],
    'app/src/main/res/layout/activity_about.xml': [
        ('                        android:text="Sunshine·阿西西"', '                        android:text="Sunshine · Axixi"'),
        ('                        android:text="搭配月光支持虚拟显示器、麦克风、DS5虚拟手柄等功能"', '                        android:text="Works with Moonlight to support virtual displays, microphones, virtual DS5 gamepads, and more"'),
        ('                        android:text="StarCore 星核"', '                        android:text="StarCore"'),
        ('                        android:text="Mac被控端应用，搭配月光实现macOS端串流。"', '                        android:text="Mac host app; works with Moonlight to stream from macOS."'),
    ],
    'app/src/main/res/layout/dialog_game_menu_display.xml': [
        ('                        android:text="HDR窗口亮度最大"', '                        android:text="Max HDR Window Brightness"'),
        ('                        android:text="提高整体亮度，部分设备可能降低HDR高光对比度。"', '                        android:text="Raises overall brightness; may reduce HDR highlight contrast on some devices."'),
        ('                    android:text="串流手柄类型"', '                    android:text="Streaming Gamepad Type"'),
        ('                    android:text="使用 sunshine·阿西西 生效"', '                    android:text="Takes effect with Sunshine · Axixi"'),
        ('                        android:text="DS5手柄扬声器"', '                        android:text="DS5 Controller Speaker"'),
        ('                        android:text="关闭不影响原生触觉反馈"', '                        android:text="Disabling does not affect native haptic feedback"'),
        ('                        android:text="原生 DS5 触觉 PCM"', '                        android:text="Native DS5 Haptic PCM"'),
        ('                        android:text="关闭后退回普通震动，保存后重连生效"', '                        android:text="When off, reverts to standard rumble; reconnect after saving to apply"'),
    ],
    'app/src/main/res/layout/dialog_game_menu_host_displays.xml': [
        ('            android:text="主机显示器"', '            android:text="Host Displays"'),
        ('            android:text="刷新"', '            android:text="Refresh"'),
        ('        android:text="正在读取 StarCore星核 PC 显示器…"', '        android:text="Reading StarCore PC displays…"'),
    ],
    'app/src/main/res/layout/dialog_game_menu_setting.xml': [
        ('                    android:layout_marginTop="8dp" android:text="启动条件"', '                    android:layout_marginTop="8dp" android:text="Activation"'),
        ('                        android:text="始终"', '                        android:text="Always"'),
        ('                        android:text="按下左扳机"', '                        android:text="Left Trigger"'),
        ('                        android:text="按下右扳机"', '                        android:text="Right Trigger"'),
    ],
    'app/src/main/res/values/arrays.xml': [
        ('        <item>自动</item>', '        <item>Auto</item>'),
        ('        <item>触控板「多手势」</item>', '        <item>Trackpad (Multi-gesture)</item>'),
    ],
    'app/src/main/res/values/extension_ime_keyboard_styles.xml': [
        ('    <string name="extension_ime_key_cmd_description" translatable="false">CMD，可锁定</string>', '    <string name="extension_ime_key_cmd_description" translatable="false">CMD, can lock</string>'),
        ('    <string name="extension_ime_key_ctrl_description" translatable="false">CTRL，可锁定</string>', '    <string name="extension_ime_key_ctrl_description" translatable="false">CTRL, can lock</string>'),
        ('    <string name="extension_ime_key_alt_description" translatable="false">ALT，可锁定</string>', '    <string name="extension_ime_key_alt_description" translatable="false">ALT, can lock</string>'),
    ],
    'app/src/main/res/values/strings.xml': [
        ('    <string name="title_usbip_mode">USB/IP 模式</string>', '    <string name="title_usbip_mode">USB/IP Mode</string>'),
        ('    <string name="summary_usbip_mode">搭配 StarCore星核 PC 端使用，将鼠标、键盘、PS5（DualSense）、Xbox、雷蛇等 USB 外设共享给 Windows。局域网 IPv4/IPv6 自动直连，公网 IPv6 使用加密连接；公网需要网络允许电脑回连本机。\\n一次共享一个 USB 设备，需授权并由 Windows 导入。同一设备共享时与 Android 本地 USB 驱动互斥，共享失败时恢复本地输入。\\n可在「完整性能信息」查看 USB/IP 状态、IP 和端口。修改后重新连接串流生效。</string>', '    <string name="summary_usbip_mode">Works with the StarCore PC host to share USB peripherals such as mice, keyboards, PS5 (DualSense), Xbox, and Razer devices with Windows. On the local network, IPv4/IPv6 connects directly; public IPv6 uses an encrypted connection and requires the network to allow the PC to connect back to this device.\\nOne USB device is shared at a time, and it must be authorized and imported by Windows. Sharing a device is mutually exclusive with Android\\\'s local USB driver; if sharing fails, local input is restored.\\nUSB/IP status, IP, and port are shown in \\"Full performance info\\". Reconnect the stream after changing this setting.</string>'),
        ('    <string name="usbip_waiting">USB/IP 等待 Windows 导入（TCP 3240，设备 1-1）</string>', '    <string name="usbip_waiting">USB/IP waiting for Windows import (TCP 3240, device 1-1)</string>'),
        ('    <string name="usbip_imported">PC端已导入</string>', '    <string name="usbip_imported">Imported by PC</string>'),
        ('    <string name="usbip_initializing">Windows 正在初始化 USB 设备</string>', '    <string name="usbip_initializing">Windows is initializing the USB device</string>'),
        ('    <string name="usbip_disabled">未启用</string>', '    <string name="usbip_disabled">Disabled</string>'),
        ('    <string name="usbip_waiting_session">等待串流连接</string>', '    <string name="usbip_waiting_session">Waiting for stream connection</string>'),
        ('    <string name="usbip_waiting_device">等待连接 USB 键鼠或手柄</string>', '    <string name="usbip_waiting_device">Waiting for a USB keyboard, mouse, or gamepad</string>'),
        ('    <string name="usbip_waiting_permission">等待 USB 设备授权</string>', '    <string name="usbip_waiting_permission">Waiting for USB device authorization</string>'),
        ('    <string name="usbip_permission_denied">USB 设备授权被拒绝</string>', '    <string name="usbip_permission_denied">USB device authorization denied</string>'),
        ('    <string name="usbip_open_failed">USB 设备打开失败</string>', '    <string name="usbip_open_failed">Failed to open USB device</string>'),
        ('    <string name="usbip_fallback">USB/IP 未连接，已恢复本地输入</string>', '    <string name="usbip_fallback">USB/IP not connected. Local input restored</string>'),
        ('    <string name="usbip_host_required">当前连接不满足 USB/IP 条件。局域网支持 IPv4/IPv6；公网 IPv6 需要支持加密 USB/IP 的新版星核 PC 端。</string>', '    <string name="usbip_host_required">This connection does not meet USB/IP requirements. IPv4/IPv6 is supported on the local network; public IPv6 requires a newer StarCore PC host that supports encrypted USB/IP.</string>'),
        ('    <string name="usbip_android_required">USB/IP 需要 Android 8.0 或更高版本</string>', '    <string name="usbip_android_required">USB/IP requires Android 8.0 or later</string>'),
        ('    <string name="usbip_secure_error">USB/IP 加密会话协商失败，请更新两端并重新连接串流</string>', '    <string name="usbip_secure_error">USB/IP encrypted session negotiation failed. Update both ends and reconnect the stream.</string>'),
        ('    <string name="title_gamepad_emulation">主机虚拟手柄类型</string>', '    <string name="title_gamepad_emulation">Host virtual gamepad type</string>'),
        ('    <string name="summary_gamepad_emulation">自动时遵循 Sunshine 设置和手柄能力；明确选择时覆盖 Sunshine 的手柄类型</string>', '    <string name="summary_gamepad_emulation">Auto follows Sunshine settings and gamepad capabilities; an explicit choice overrides Sunshine\\\'s gamepad type</string>'),
        ('    <string name="game_menu_ds_touchpad">DS触控板</string>', '    <string name="game_menu_ds_touchpad">DS touchpad</string>'),
        ('    <string name="game_menu_ds_touchpad_shown">DS触控板已开启：5秒无操作后自动隐藏；触摸原位置可唤醒，按住右下角可拖动位置</string>', '    <string name="game_menu_ds_touchpad_shown">DS touchpad enabled: hides automatically after 5 seconds of inactivity; touch its original position to wake it, or hold the bottom-right corner to move it</string>'),
        ('    <string name="game_menu_ds_touchpad_hidden">DS触控板已隐藏</string>', '    <string name="game_menu_ds_touchpad_hidden">DS touchpad hidden</string>'),
        ('    <string name="game_menu_ds_touchpad_drag_handle">拖动DS触控板</string>', '    <string name="game_menu_ds_touchpad_drag_handle">Move DS touchpad</string>'),
    ],
    'app/src/main/res/values/strings_settings_panel.xml': [
        ('    <string name="settings_panel_title">设置</string>', '    <string name="settings_panel_title">Settings</string>'),
        ('    <string name="settings_panel_back">返回</string>', '    <string name="settings_panel_back">Back</string>'),
        ('    <string name="settings_panel_close">关闭</string>', '    <string name="settings_panel_close">Close</string>'),
        ('    <string name="settings_panel_hint">配置下次串流使用的选项</string>', '    <string name="settings_panel_hint">Options applied to the next stream session</string>'),
        ('    <string name="settings_panel_custom">自定义分辨率</string>', '    <string name="settings_panel_custom">Custom resolution</string>'),
        ('    <string name="settings_panel_apply">保存</string>', '    <string name="settings_panel_apply">Save</string>'),
        ('    <string name="settings_panel_reset">使用默认值</string>', '    <string name="settings_panel_reset">Use defaults</string>'),
        ('    <string name="settings_panel_resolution_hint">宽 × 高，例如 1920x1080</string>', '    <string name="settings_panel_resolution_hint">Width × height, e.g. 1920x1080</string>'),
        ('    <string name="settings_panel_resolution_error">请输入 2–16384 之间的偶数宽高，例如 1920x1080</string>', '    <string name="settings_panel_resolution_error">Enter an even width and height between 2–16384, e.g. 1920x1080</string>'),
        ('    <string name="settings_panel_range_error">请输入 %1$s–%2$s 之间的数值</string>', '    <string name="settings_panel_range_error">Enter a value between %1$s–%2$s</string>'),
        ('    <string name="settings_panel_empty">当前设备没有可用选项</string>', '    <string name="settings_panel_empty">No options available for this device</string>'),
        ('    <string name="settings_panel_width">宽度</string>', '    <string name="settings_panel_width">Width</string>'),
        ('    <string name="settings_panel_height">高度</string>', '    <string name="settings_panel_height">Height</string>'),
        ('    <string name="settings_panel_swap">交换宽高</string>', '    <string name="settings_panel_swap">Swap width and height</string>'),
        ('    <string name="settings_panel_pixels">像素</string>', '    <string name="settings_panel_pixels">pixels</string>'),
        ('    <string name="settings_panel_bitrate_hint">手动输入，最大 99999 Mbps</string>', '    <string name="settings_panel_bitrate_hint">Enter manually, max 99999 Mbps</string>'),
        ('    <string name="settings_panel_bitrate_presets">常用码率 · Mbps</string>', '    <string name="settings_panel_bitrate_presets">Common bitrates · Mbps</string>'),
        ('    <string name="settings_profile_switch">切换配置</string>', '    <string name="settings_profile_switch">Switch profile</string>'),
        ('    <string name="settings_profile_name">配置 %1$s</string>', '    <string name="settings_profile_name">Profile %1$s</string>'),
        ('    <string name="settings_profile_current">当前：配置 %1$s</string>', '    <string name="settings_profile_current">Current: Profile %1$s</string>'),
        ('    <string name="settings_profile_title">设置 · %1$s</string>', '    <string name="settings_profile_title">Settings · %1$s</string>'),
        ('    <string name="settings_profile_reset">重置数据</string>', '    <string name="settings_profile_reset">Reset data</string>'),
        ('    <string name="settings_profile_reset_hint">恢复当前配置的默认设置</string>', '    <string name="settings_profile_reset_hint">Restore the default settings for the current profile</string>'),
        ('    <string name="settings_profile_reset_confirm">将配置 %1$s 的设置恢复为默认值。其他配置、主机配对、日志和已导入的文件会保留。</string>', '    <string name="settings_profile_reset_confirm">Reset the settings of profile %1$s to defaults. Other profiles, host pairings, logs, and imported files are kept.</string>'),
        ('    <string name="settings_profile_reset_action">恢复默认</string>', '    <string name="settings_profile_reset_action">Restore defaults</string>'),
        ('    <string name="settings_profile_working">正在保存配置…</string>', '    <string name="settings_profile_working">Saving profile…</string>'),
        ('    <string name="settings_profile_failed">配置保存失败，请重试。</string>', '    <string name="settings_profile_failed">Failed to save profile. Try again.</string>'),
        ('    <string name="settings_profile_choose_hint">切换时自动保存当前配置，新配置使用默认设置。</string>', '    <string name="settings_profile_choose_hint">The current profile is saved automatically when switching; the new profile starts with default settings.</string>'),
    ],
    'app/src/main/res/values/strings_stylus.xml': [
        ('    <string name="stylus_mode_title">手写笔模式</string>', '    <string name="stylus_mode_title">Stylus mode</string>'),
        ('    <string name="stylus_follow">跟随触控模式</string>', '    <string name="stylus_follow">Follow touch mode</string>'),
        ('    <string name="stylus_native">原生笔</string>', '    <string name="stylus_native">Native pen</string>'),
        ('    <string name="stylus_mouse">鼠标</string>', '    <string name="stylus_mouse">Mouse</string>'),
        ('    <string name="stylus_follow_description">按当前触控模式处理；多点触控时作为触屏输入。</string>', '    <string name="stylus_follow_description">Handled by the current touch mode; treated as touch input when multi-touch is active.</string>'),
        ('    <string name="stylus_native_description">发送悬停、压感与倾斜；主机不支持时使用鼠标。</string>', '    <string name="stylus_native_description">Sends hover, pressure, and tilt; falls back to mouse when the host doesn\\\'t support it.</string>'),
        ('    <string name="stylus_mouse_description">笔尖定位，落笔和拖动时按住左键，抬笔释放。</string>', '    <string name="stylus_mouse_description">Pen tip positions the cursor; holds the left button while touching and dragging, releases on lift.</string>'),
    ],
    'app/src/main/res/values/strings_touchpad_rotation.xml': [
        ('    <string name="touchpad_rotation_title">触控板方向</string>', '    <string name="touchpad_rotation_title">Touchpad orientation</string>'),
        ('    <string name="touchpad_rotation_description">校正外接触控板方向，即时生效；角度为逆时针。</string>', '    <string name="touchpad_rotation_description">Corrects the orientation of an external touchpad; applies immediately. Angles are counterclockwise.</string>'),
        ('    <string name="touchpad_rotation_normal">正常</string>', '    <string name="touchpad_rotation_normal">Normal</string>'),
        ('    <string name="mouse_rotation_title">实体鼠标方向</string>', '    <string name="mouse_rotation_title">Physical mouse orientation</string>'),
        ('    <string name="mouse_rotation_description">校正实体鼠标移动方向，即时生效；角度为逆时针。</string>', '    <string name="mouse_rotation_description">Corrects the movement direction of a physical mouse; applies immediately. Angles are counterclockwise.</string>'),
    ],
    'app/src/main/res/xml/preferences.xml': [
        ('            android:title="画面显示位置"', '            android:title="Screen Position"'),
        ('            android:title="触控/鼠标模式"', '            android:title="Mouse/Touch Mode"'),
        ('            android:title="精简模式点击选项"', '            android:title="Lite Overlay Tap Action"'),
        ('            android:title="精简模式扩展参数"', '            android:title="Lite Overlay Extended Stats"'),
        ('            android:title="启用悬浮球"', '            android:title="Enable Floating Button"'),
        ('    <PreferenceCategory android:key="category_settings_additional" android:title="其他配置">', '    <PreferenceCategory android:key="category_settings_additional" android:title="Additional Settings">'),
        ('            android:title="HDR 高亮度"', '            android:title="HDR High Brightness"'),
        ('            android:summary="在支持的设备上提高 HDR 画面亮度"', '            android:summary="Increases HDR brightness on supported devices"'),
        ('            android:title="强制显示模式"', '            android:title="Force Display Mode"'),
        ('            android:summary="优先使用匹配串流帧率的显示模式；显示异常时可关闭"', '            android:summary="Prefers a display mode matching the stream frame rate; disable if display issues occur"'),
        ('            android:title="保留画面缩放"', '            android:title="Keep Video Zoom"'),
        ('            android:summary="关闭缩放调节时保留已调整的画面比例"', '            android:summary="Keeps the adjusted video scaling when zoom is disabled"'),
        ('            android:title="Esc 打开游戏菜单"', '            android:title="Esc Opens Game Menu"'),
        ('            android:summary="使用实体键盘 Esc 键打开串流快捷菜单"', '            android:summary="Use the physical keyboard Esc key to open the in-stream quick menu"'),
        ('            android:title="DualSense 原生音频震动"', '            android:title="DualSense Native Audio Haptics"'),
        ('            android:summary="接收支持的主机发送的原生 PCM 触觉数据"', '            android:summary="Receives native PCM haptic data from supported hosts"'),
        ('            android:title="DualSense 手柄扬声器"', '            android:title="DualSense Controller Speaker"'),
        ('            android:summary="向支持的 DualSense 手柄输出游戏扬声器音频"', '            android:summary="Routes game speaker audio to supported DualSense controllers"'),
    ],
}


def translate_file(filepath, replacements):
    with open(filepath, 'r', encoding='utf-8', newline='') as f:
        lines = f.readlines()
    changed = False
    for old, new in replacements:
        for index, line in enumerate(lines):
            body = line.rstrip('\r\n')
            if body == old:
                lines[index] = new + line[len(body):]
                changed = True
    if changed:
        with open(filepath, 'w', encoding='utf-8', newline='') as f:
            f.writelines(lines)
    return changed


def translate_files():
    updated = 0
    for filepath, replacements in FILE_REPLACEMENTS.items():
        if os.path.isfile(filepath) and translate_file(filepath, replacements):
            updated += 1
    print(f'Re-applied upstream 261107 translations in {updated} files.')


if __name__ == '__main__':
    translate_files()
