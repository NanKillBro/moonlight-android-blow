import sys
import os

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

def translate_strings_xml():
    filepath = 'app/src/main/res/values/strings.xml'
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Exact replacements for strings.xml
    replacements = [
        ('<string name="game_menu_hud">(显示/隐藏)性能信息</string>', '<string name="game_menu_hud">Performance Overlay (Show/Hide)</string>'),
        ('<string name="game_menu_switch_mouse_model">鼠标模式切换</string>', '<string name="game_menu_switch_mouse_model">Mouse Mode Switch</string>'),
        ('<string name="game_menu_switch_keyboard_model">(显示/隐藏)特殊按键</string>', '<string name="game_menu_switch_keyboard_model">Special Keys (Show/Hide)</string>'),
        ('<string name="game_menu_switch_virtual_model">(显示/隐藏)虚拟手柄</string>', '<string name="game_menu_switch_virtual_model">Virtual Gamepad (Show/Hide)</string>'),
        ('<string name="game_menu_switch_virtual_keyboard_model">(显示/隐藏)虚拟全键盘</string>', '<string name="game_menu_switch_virtual_keyboard_model">Full Virtual Keyboard (Show/Hide)</string>'),
        ('<string name="game_menu_switch_touch_sensitivity_model">(开启/禁用)触控灵敏度</string>', '<string name="game_menu_switch_touch_sensitivity_model">Touch Sensitivity (Enable/Disable)</string>'),
        ('<string name="game_menu_switch_touch_sensitivity_update_x">触控灵敏度修改X轴</string>', '<string name="game_menu_switch_touch_sensitivity_update_x">Adjust Touch Sensitivity X-Axis</string>'),
        ('<string name="game_menu_switch_touch_sensitivity_update_y">触控灵敏度修改Y轴</string>', '<string name="game_menu_switch_touch_sensitivity_update_y">Adjust Touch Sensitivity Y-Axis</string>'),
        ('<string name="game_menu_gamepad_mouse">手柄键鼠</string>', '<string name="game_menu_gamepad_mouse">Gamepad Mouse</string>'),
        ('<string name="game_menu_connect_gamepad">请连接手柄后使用</string>', '<string name="game_menu_connect_gamepad">Please connect a gamepad first</string>'),
        ('<string name="game_menu_gamepad_mouse_enabled">手柄键鼠模式：已开启</string>', '<string name="game_menu_gamepad_mouse_enabled">Gamepad Mouse Mode: Enabled</string>'),
        ('<string name="game_menu_gamepad_mouse_disabled">手柄键鼠模式：已关闭</string>', '<string name="game_menu_gamepad_mouse_disabled">Gamepad Mouse Mode: Disabled</string>'),
        ('<string name="game_menu_disconnect">断开连接</string>', '<string name="game_menu_disconnect">Disconnect</string>'),
        ('<string name="game_menu_quit_steaming">退出串流</string>', '<string name="game_menu_quit_steaming">Quit Streaming</string>'),
        ('<string name="game_menu_cancel">取消</string>', '<string name="game_menu_cancel">Cancel</string>'),
        ('<string name="game_menu_send_keys">发送特殊按键</string>', '<string name="game_menu_send_keys">Send Special Keys</string>'),
        ('<string name="game_menu_send_keys_ctrl_v">Send Ctrl + V (粘贴剪切板)</string>', '<string name="game_menu_send_keys_ctrl_v">Send Ctrl + V (Paste Clipboard)</string>'),
        ('<string name="game_menu_send_keys_win">Send Win (打开Windows开始菜单)</string>', '<string name="game_menu_send_keys_win">Send Win (Open Start Menu)</string>'),
        ('<string name="game_menu_send_keys_win_d">Send Win + D (返回桌面)</string>', '<string name="game_menu_send_keys_win_d">Send Win + D (Show Desktop)</string>'),
        ('<string name="game_menu_send_keys_win_p">Send Win + P (显示器模式)</string>', '<string name="game_menu_send_keys_win_p">Send Win + P (Display Mode)</string>'),
        ('<string name="game_menu_send_keys_alt_b">Send ALT + B (切换HDR)</string>', '<string name="game_menu_send_keys_alt_b">Send ALT + B (Toggle HDR)</string>'),
        ('<string name="game_menu_send_keys_win_x_u_s">Send Win + X ~ U + S (睡眠)</string>', '<string name="game_menu_send_keys_win_x_u_s">Send Win + X ~ U + S (Sleep)</string>'),
        ('<string name="game_menu_send_keys_win_x_u_r">Send Win + X ~ U + R (重启)</string>', '<string name="game_menu_send_keys_win_x_u_r">Send Win + X ~ U + R (Restart)</string>'),
        ('<string name="game_menu_send_keys_win_x_u_u">Send Win + X ~ U + U (关机)</string>', '<string name="game_menu_send_keys_win_x_u_u">Send Win + X ~ U + U (Shut Down)</string>'),
        ('<string name="game_menu_send_keys_win_x_u_i">Send Win + X ~ U + I (注销)</string>', '<string name="game_menu_send_keys_win_x_u_i">Send Win + X ~ U + I (Sign Out)</string>'),
        ('<string name="game_menu_send_keys_win_g">Send Win + G (打开Xbox Game Bar)</string>', '<string name="game_menu_send_keys_win_g">Send Win + G (Open Xbox Game Bar)</string>'),
        ('<string name="game_menu_send_keys_shift_tab">Send Shift + Tab (打开Steam Overlay)</string>', '<string name="game_menu_send_keys_shift_tab">Send Shift + Tab (Open Steam Overlay)</string>'),
        ('<string name="game_menu_send_keys_win_shift_left">Send Win + shift + left (切换桌面)</string>', '<string name="game_menu_send_keys_win_shift_left">Send Win + Shift + Left (Switch Desktop)</string>'),
        ('<string name="game_menu_send_keys_ctrl_alt_shift_q">Send Ctrl+Alt+Shift+Q (PC退出串流)</string>', '<string name="game_menu_send_keys_ctrl_alt_shift_q">Send Ctrl+Alt+Shift+Q (PC Quit Streaming)</string>'),
        ('<string name="game_menu_send_keys_ctrl_alt_shift_f1">Send Ctrl+Alt+Shift+F1 (切换显示器)</string>', '<string name="game_menu_send_keys_ctrl_alt_shift_f1">Send Ctrl+Alt+Shift+F1 (Switch Display)</string>'),
        ('<string name="game_menu_send_keys_ctrl_alt_shift_f12">Send Ctrl+Alt+Shift+F12 (切换显示器)</string>', '<string name="game_menu_send_keys_ctrl_alt_shift_f12">Send Ctrl+Alt+Shift+F12 (Switch Display)</string>'),
        ('<string name="perf_overlay_lite_decoder">解码器： %1$s</string>', '<string name="perf_overlay_lite_decoder">Decoder: %1$s</string>'),
        (
'''    <string name="axi_add_computer_tips">温馨提示：\\n1、PC端设备开启N卡GeForce Shield 服务或者安装Sunshine并启用串流服务\\n
        2、如果是默认端口[47989]，无需手动输入，自定义端口需要自行拼接\\n
        3、支持ipv4和ipv6地址 例如：\\n
        ipv4：192.168.1.123\\n
        ipv6：[fd00:6868:6868:0:fd6:e0ea:84d9:70ea]:47989
    </string>''',
'''    <string name="axi_add_computer_tips">Helpful Tips:\\n1. Ensure NVIDIA GeForce Shield service or Sunshine is running on your host PC.\\n
        2. If using the default port [47989], there is no need to enter it manually. Custom ports should be specified.\\n
        3. Supports both IPv4 and IPv6 addresses. Example:\\n
        IPv4: 192.168.1.123\\n
        IPv6: [fd00:6868:6868:0:fd6:e0ea:84d9:70ea]:47989
    </string>'''
        ),
        (
'''    <string name="axi_question_1">1、手柄测试界面可用，串流游戏中不识别？</string>
    <string name="axi_question_answer_1">大概率电脑端没有安装虚拟手柄驱动ViGEmBus，在sunshine首页查看是否有相关报错信息.ps:点击网盘资源，内有相关安装文件.
        \\n或者手柄识别为DS4手柄，部分游戏不适配,可在sunshine后台，输入选项卡修改手柄类型为xbox360解决。</string>''',
'''    <string name="axi_question_1">1. Gamepad works in test screen, but is not recognized in stream?</string>
    <string name="axi_question_answer_1">Most likely ViGEmBus virtual gamepad driver is not installed on the PC. Check Sunshine Web UI home page for errors.
        \\nOr the controller is recognized as DS4 which is unsupported by some games; change controller type to Xbox 360 in Sunshine Web UI > Input tab.</string>'''
        ),
        (
'''    <string name="axi_question_2">2、串流如何全屏显示？如何息屏游玩？</string>
    <string name="axi_question_answer_2">使用虚拟显示器或者HDMI欺骗器创建本机相对于分辨率的显示器屏幕.
        \\nHDMI欺骗器需要借助显卡驱动程序创建，设置完成需要设置为主屏幕，sunshine默认捕获主屏幕（可在sunshine后台修改默认捕获屏幕）
        \\n息屏可Win+P或者系统设置-显示器，选择仅显示器1或者2，或者部分sunshine版本后台内置相关无头显示器设置.
        \\n部分sunshine版本自带虚拟显示器，比如Apollo版 ps:点击网盘资源，内有相关安装文件</string>''',
'''    <string name="axi_question_2">2. How to stream in fullscreen or with PC monitor turned off?</string>
    <string name="axi_question_answer_2">Use a virtual display or HDMI dummy plug matched to your client resolution.
        \\nSet it as primary display in Windows Display Settings (Sunshine captures primary display by default).
        \\nTo turn off host screen, press Win+P and choose Second screen only, or use headless display tools like Apollo/IddSampleDriver.</string>'''
        ),
        ('<string name="about_get_res"><u>网盘资源</u></string>', '<string name="about_get_res"><u>Resources</u></string>'),
        ('<string name="about_update_tx"><u>检测更新</u></string>', '<string name="about_update_tx"><u>Check for Updates</u></string>'),
        ('<string name="about_version_history"><u>版本日志</u></string>', '<string name="about_version_history"><u>Changelog</u></string>'),
        ('<string name="about_help"><u>使用帮助</u></string>', '<string name="about_help"><u>Help Guide</u></string>'),
        ('<string name="credits_sponsored_dialog_title">赞赏</string>', '<string name="credits_sponsored_dialog_title">Donate</string>'),
        ('<string name="credits_sponsored_dialog_message">如果你愿意支持项目持续更新，可以直接扫码赞赏。非常感谢你的陪伴与鼓励。</string>', '<string name="credits_sponsored_dialog_message">If you would like to support the ongoing development of this project, you can donate. Thank you very much for your encouragement and support.</string>'),
        ('<string name="game_menu_enable_virtual_mouse">虚拟鼠标</string>', '<string name="game_menu_enable_virtual_mouse">Virtual Mouse</string>'),
        ('<string name="game_menu_disable_virtual_mouse">虚拟鼠标</string>', '<string name="game_menu_disable_virtual_mouse">Virtual Mouse</string>'),
        ('<string name="virtual_mouse_accessibility_hidden">虚拟鼠标已隐藏</string>', '<string name="virtual_mouse_accessibility_hidden">Virtual mouse hidden</string>'),
        ('<string name="virtual_mouse_accessibility_compact">虚拟鼠标，点击展开，拖动可移动</string>', '<string name="virtual_mouse_accessibility_compact">Virtual mouse: tap to expand, drag to move</string>'),
        ('<string name="virtual_mouse_accessibility_expanded">虚拟鼠标已展开，包含左右键、滚轮和指针移动区</string>', '<string name="virtual_mouse_accessibility_expanded">Virtual mouse expanded: left/right click, wheel, and pointer area</string>'),
        ('<string name="virtual_mouse_accessibility_scroll">虚拟鼠标方向滚动</string>', '<string name="virtual_mouse_accessibility_scroll">Virtual mouse scroll</string>'),
        ('<string name="video_zoom_enabled_hint">画面缩放已开启：拖动平移，双指缩放，双击复位，轻点左键</string>', '<string name="video_zoom_enabled_hint">Zoom enabled: Drag to pan, pinch to zoom, double tap to reset, tap to left click</string>'),
        ('<string name="video_zoom_disabled">画面缩放已关闭</string>', '<string name="video_zoom_disabled">Zoom disabled</string>'),
        ('<string name="video_zoom_disabled_retained">画面缩放已关闭，当前画面已保留</string>', '<string name="video_zoom_disabled_retained">Zoom disabled, current view retained</string>'),
        ('<string name="video_zoom_accessibility">画面缩放手势区域</string>', '<string name="video_zoom_accessibility">Video zoom gesture area</string>'),
        ('<string name="home_action_back">返回</string>', '<string name="home_action_back">Back</string>'),
        ('<string name="home_action_support">赞赏</string>', '<string name="home_action_support">Donate</string>'),
        ('<string name="version_history_title">版本日志</string>', '<string name="version_history_title">Changelog</string>'),
        ('<string name="version_history_loading">正在读取版本日志…</string>', '<string name="version_history_loading">Loading changelog…</string>'),
        ('<string name="version_history_empty">暂无版本日志</string>', '<string name="version_history_empty">No changelog available</string>'),
        ('<string name="version_history_load_failed">版本日志加载失败，请稍后重试</string>', '<string name="version_history_load_failed">Failed to load changelog, please try again later</string>'),
        ('<string name="version_history_retry">重新加载</string>', '<string name="version_history_retry">Retry</string>'),
        ('<string name="version_history_current">当前版本</string>', '<string name="version_history_current">Current Version</string>'),
        ('<string name="version_history_latest">最新版本</string>', '<string name="version_history_latest">Latest Version</string>'),
        ('<string name="version_history_unknown">未知版本</string>', '<string name="version_history_unknown">Unknown Version</string>'),
        ('<string name="version_history_empty_description">暂无更新说明</string>', '<string name="version_history_empty_description">No update notes available</string>'),
    ]

    for old, new in replacements:
        # Normalize newlines for match
        old_crlf = old.replace('\n', '\r\n')
        old_lf = old.replace('\r\n', '\n')
        if old in content:
            content = content.replace(old, new)
        elif old_crlf in content:
            content = content.replace(old_crlf, new.replace('\n', '\r\n'))
        elif old_lf in content:
            content = content.replace(old_lf, new.replace('\r\n', '\n'))
        else:
            print(f"Warning: pattern not found in strings.xml:\n{old[:50]}")

    with open(filepath, 'w', encoding='utf-8', newline='') as f:
        f.write(content)
    print("Updated strings.xml")

def translate_arrays_xml():
    filepath = 'app/src/main/res/values/arrays.xml'
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    replacements = [
        ('<item>系统渲染</item>', '<item>System Rendering</item>'),
        ('<item>GLES渲染</item>', '<item>GLES Rendering</item>'),
        ('<item>左右全宽</item>', '<item>Side-by-Side Full</item>'),
        ('<item>左右半宽</item>', '<item>Side-by-Side Half</item>'),
        ('<item>弱</item>', '<item>Weak</item>'),
        ('<item>标准</item>', '<item>Standard</item>'),
        ('<item>强</item>', '<item>Strong</item>'),
        ('<item>近</item>', '<item>Near</item>'),
        ('<item>远</item>', '<item>Far</item>'),
        ('<item>柔和</item>', '<item>Soft</item>'),
        ('<item>极强</item>', '<item>Ultra Sharp</item>'),
        ('<item>兼容 SDR 映射</item>', '<item>Compatible SDR Tone Mapping</item>'),
        ('<item>原生 HDR 直出</item>', '<item>Native HDR Output</item>'),
        ('<item>低</item>', '<item>Low</item>'),
        ('<item>中</item>', '<item>Medium</item>'),
        ('<item>高</item>', '<item>High</item>'),
        ('<item>手机</item>', '<item>Phone</item>'),
        ('<item>手柄</item>', '<item>Gamepad</item>'),
        ('<item>方案1</item>', '<item>Preset 1</item>'),
        ('<item>方案2</item>', '<item>Preset 2</item>'),
        ('<item>方案3</item>', '<item>Preset 3</item>'),
        ('<item>方案4</item>', '<item>Preset 4</item>'),
        ('<item>方案5</item>', '<item>Preset 5</item>'),
        ('<item>多点触控模式</item>', '<item>Multi-touch Mode</item>'),
        ('<item>普通鼠标模式</item>', '<item>Normal Mouse Mode</item>'),
        ('<item>触控板模式</item>', '<item>Trackpad Mode</item>'),
        ('<item>禁用鼠标/触控</item>', '<item>Disable Mouse/Touch</item>'),
        ('<item>普通鼠标「左右键互换」</item>', '<item>Normal Mouse (Swap Left/Right)</item>'),
        ('<item>触控板「仅移动」</item>', '<item>Trackpad (Move Only)</item>'),
        ('<item>触控板「移动+左键点击」</item>', '<item>Trackpad (Move + Left Click)</item>'),
        ('<item>默认居中</item>', '<item>Default Center</item>'),
        ('<item>顶部居中</item>', '<item>Top Center</item>'),
        ('<item>顶部居左</item>', '<item>Top Left</item>'),
        ('<item>顶部居右</item>', '<item>Top Right</item>'),
        ('<item>底部居中</item>', '<item>Bottom Center</item>'),
        ('<item>底部居左</item>', '<item>Bottom Left</item>'),
        ('<item>底部居右</item>', '<item>Bottom Right</item>'),
        ('<item>关闭</item>', '<item>Disabled</item>'),
    ]

    for old, new in replacements:
        content = content.replace(old, new)

    with open(filepath, 'w', encoding='utf-8', newline='') as f:
        f.write(content)
    print("Updated arrays.xml")

if __name__ == '__main__':
    translate_strings_xml()
    translate_arrays_xml()
