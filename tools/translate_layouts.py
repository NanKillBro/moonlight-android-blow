import os
import re
import sys

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

REPLACEMENTS = [
    # activity_about.xml
    ('android:text="随时随地，畅连你的电脑！"', 'android:text="Connect to your PC anytime, anywhere!"'),
    ('android:text="版本号：1.0.0"', 'android:text="Version: 1.0.0"'),
    ('android:text="鸣谢"', 'android:text="Credits"'),
    ('android:text="感谢每一位支持与陪伴的朋友"', 'android:text="Thanks to all friends who supported and accompanied us"'),
    ('android:text="更多应用"', 'android:text="More Apps"'),
    ('android:text="前往开发者个人空间，发现更多应用与作品"', 'android:text="Visit developer space to explore more apps"'),
    ('android:text="在这里找到开发者"', 'android:text="Find developer here"'),

    # activity_add_computer_manually.xml
    ('android:text="根据svr获取"', 'android:text="Fetch via SrvResolver"'),
    ('android:text="追加Razer雷游端口号"', 'android:text="Append Razer Cortex Port"'),

    # activity_app_view_new.xml
    ('tools:text="我的电脑"', 'tools:text="My PC"'),
    ('android:text="长按选中菜单有更多选项"', 'android:text="Long press menu item for more options"'),

    # activity_axitest.xml
    ('android:text="测试键盘按键"', 'android:text="Test Keyboard Keys"'),
    ('android:text="测试设备震动"', 'android:text="Test Device Rumble"'),
    ('android:text="【开/关】振动重定向"', 'android:text="Toggle Rumble Redirection"'),
    ('android:text="刷新手柄列表"', 'android:text="Refresh Gamepad List"'),
    ('android:text="测试USB手柄震动"', 'android:text="Test USB Gamepad Rumble"'),
    ('android:text="测试手柄震动"', 'android:text="Test Gamepad Rumble"'),
    ('android:text="振幅强度"', 'android:text="Rumble Amplitude"'),
    ('android:text="停止测试"', 'android:text="Stop Test"'),
    ('android:text="取消震动"', 'android:text="Stop Rumble"'),
    ('android:text="安卓设备信息"', 'android:text="Android Device Info"'),
    ('android:text="点击刷新按钮刷新手柄信息\\nUSB手柄测试 设置-勾选覆盖USB驱动"', 'android:text="Tap refresh to update gamepad list\\nFor USB gamepad testing: Settings > Enable USB Driver"'),

    # activity_credits.xml
    ('android:text="赞赏"', 'android:text="Donate"'),
    ('android:text="感谢一路同行的你们"', 'android:text="Thank you for walking this journey with us"'),
    ('android:text="这份名单献给每一位支持阿西西的朋友，因为你们，项目才得以持续前进。"', 'android:text="This list is dedicated to everyone who supported this project. Because of you, we keep moving forward."'),
    ('android:text="鸣谢墙"', 'android:text="Credits Wall"'),

    # activity_game.xml
    ('android:text="性能信息"', 'android:text="Performance Stats"'),
    ('tools:text="延迟/解码：109ms/7ms 丢包率：69% FPS：60"', 'tools:text="Latency/Decode: 109ms/7ms Loss: 69% FPS: 60"'),

    # activity_stream_logs.xml
    ('android:contentDescription="返回"', 'android:contentDescription="Back"'),
    ('android:text="串流日志"', 'android:text="Stream Logs"'),
    ('android:text="暂无串流日志\\n开启采集后，每次串流会生成一份新日志"', 'android:text="No stream logs yet\\nWhen enabled, each streaming session will generate a new log"'),

    # app_grid_item_new.xml
    ('tools:text="我的应用"', 'tools:text="My Apps"'),

    # ax_gamepad_top_view.xml
    ('android:text="位移"', 'android:text="Move"'),
    ('android:text="缩放"', 'android:text="Scale"'),
    ('android:text="禁用"', 'android:text="Disable"'),
    ('android:text="应用"', 'android:text="Apply"'),

    # axi_keyboard_top_left_view.xml
    ('android:text="当前按钮：xx"', 'android:text="Button: xx"'),
    ('android:text="键值：xx"', 'android:text="Keycode: xx"'),
    ('android:text="坐标：xx"', 'android:text="Position: xx"'),
    ('android:text="缩放比例：100%"', 'android:text="Scale: 100%"'),
    ('android:text="缩放宽度：100%"', 'android:text="Scale Width: 100%"'),
    ('android:text="缩放高度：100%"', 'android:text="Scale Height: 100%"'),
    ('android:text="锁定模式"', 'android:text="Lock Mode"'),
    ('android:text="方形按钮"', 'android:text="Square Button"'),
    ('android:text="删除"', 'android:text="Delete"'),
    ('android:text="取消"', 'android:text="Cancel"'),

    # axi_keyboard_top_right_view.xml
    ('android:text="新增按钮"', 'android:text="Add Button"'),
    ('android:text="重置布局"', 'android:text="Reset Layout"'),
    ('android:text="保存布局"', 'android:text="Save Layout"'),

    # dialog_axi_gamepad_ds5.xml
    ('android:text="外设"', 'android:text="Peripherals"'),
    ('android:text="应用配置"', 'android:text="Apply Config"'),
    ('android:text="扳机类型"', 'android:text="Trigger Type"'),
    ('android:text="右上角应用配置生效！(每次连接手动执行下)"', 'android:text="Tap Apply Config in top-right corner to take effect! (Manual per connection)"'),
    ('android:text="关闭"', 'android:text="Disabled"'),
    ('android:text="阻尼"', 'android:text="Resistance"'),
    ('android:text="扳机"', 'android:text="Trigger"'),
    ('android:text="自动步枪扳机"', 'android:text="Automatic Gun Trigger"'),
    ('android:text="震动强度"', 'android:text="Rumble Strength"'),
    ('android:text="震动频率"', 'android:text="Rumble Frequency"'),
    ('android:text="起始位置"', 'android:text="Start Position"'),
    ('android:text="结束位置"', 'android:text="End Position"'),

    # dialog_game_menu.xml
    ('android:text="操作"', 'android:text="Actions"'),
    ('android:text="键盘"', 'android:text="Keyboard"'),
    ('android:text="桌面"', 'android:text="Desktop"'),
    ('android:text="全部窗口"', 'android:text="All Windows"'),
    ('android:text="功能与操作"', 'android:text="Quick Actions & Functions"'),
    ('android:text="(只对本次串流生效)"', 'android:text="(Session only)"'),
    ('android:text="断开连接"', 'android:text="Disconnect"'),
    ('android:text="退出串流"', 'android:text="Quit Stream"'),
    ('android:text="旋转屏幕"', 'android:text="Rotate Screen"'),
    ('android:text="虚拟手柄"', 'android:text="Virtual Gamepad"'),
    ('android:text="虚拟按键"', 'android:text="Virtual Controls"'),
    ('android:text="全键盘"', 'android:text="Full Keyboard"'),
    ('android:text="画面缩放"', 'android:text="Video Zoom"'),
    ('android:text="显示器"', 'android:text="Display"'),
    ('android:text="麦克风"', 'android:text="Microphone"'),
    ('android:text="特色功能"', 'android:text="Features"'),
    ('android:text="鼠标与触控"', 'android:text="Mouse & Touch"'),
    ('android:text="快捷键"', 'android:text="Shortcuts"'),
    ('android:text="虚拟手柄与按键"', 'android:text="Virtual Gamepad & Keys"'),
    ('android:text="显示"', 'android:text="Display"'),
    ('android:text="音频震动"', 'android:text="Audio Haptics"'),
    ('android:text="触控灵敏度"', 'android:text="Touch Sensitivity"'),
    ('android:text="杂项"', 'android:text="Miscellaneous"'),

    # dialog_game_menu_audio_haptics.xml
    ('android:text="功能"', 'android:text="Features"'),
    ('android:text="以下选项开关会保存到配置文件"', 'android:text="The following settings will be saved to configuration"'),
    ('android:text="音频震动（Beta）"', 'android:text="Audio Haptics (Beta)"'),
    ('android:text="把串流音频转换成震动反馈，更适合爆炸、撞击、低频场景"', 'android:text="Converts stream audio to haptic rumble for explosions, impacts, and low frequencies"'),
    ('android:text="开启"', 'android:text="Enabled"'),
    ('android:text="音频震动输出目标"', 'android:text="Audio Haptics Output Target"'),
    ('android:text="其中原装DS5有线驱动接管模式，有特殊优化."', 'android:text="Dedicated optimizations when using wired DualSense (DS5) driver."'),
    ('android:text="手机"', 'android:text="Phone"'),
    ('android:text="手柄"', 'android:text="Gamepad"'),
    ('android:text="保留游戏内手柄震动"', 'android:text="Retain In-Game Gamepad Rumble"'),
    ('android:text="音频震动强度：100%"', 'android:text="Audio Haptics Strength: 100%"'),
    ('android:text="音频震动语音过滤"', 'android:text="Audio Haptics Voice Filter"'),
    ('android:text="降低人声、语音聊天、播报声对震动的触发"', 'android:text="Reduces rumble triggered by voice chat and dialogues"'),
    ('android:text="低"', 'android:text="Low"'),
    ('android:text="中"', 'android:text="Medium"'),
    ('android:text="高"', 'android:text="High"'),

    # dialog_game_menu_control.xml
    ('android:text="手柄"', 'android:text="Gamepad"'),
    ('android:text="以下功能可能需要重新连接手柄生效！"', 'android:text="The following options may require reconnecting gamepad to take effect!"'),
    ('android:text="启用月光\\nUSB手柄驱动"', 'android:text="Enable Moonlight\\nUSB Gamepad Driver"'),
    ('android:text="反转握把\\n震动方向"', 'android:text="Invert Grip\\nRumble Motors"'),
    ('android:text="忽略扳机\\n默认死区"', 'android:text="Disable Trigger\\nDefault Deadzone"'),
    ('android:text="上报手柄\\n电池状态"', 'android:text="Report Gamepad\\nBattery Status"'),
    ('android:text="启用USB驱动\\n手柄陀螺仪"', 'android:text="Enable USB Driver\\nGamepad Gyro"'),
    ('android:text="握把震动联动\\n扳机震动"', 'android:text="Sync Grip Rumble\\nTo Triggers"'),
    ('android:text="以下功能需要重新打开串流页面生效！"', 'android:text="The following options take effect on next stream launch!"'),
    ('android:text="强制使用\\n机身震动"', 'android:text="Force Phone\\nBody Rumble"'),
    ('android:text="无手柄使用\\n设备陀螺仪"', 'android:text="Use Phone Gyro\\nWithout Gamepad"'),
    ('android:text="兼容NS\\n手柄按键"', 'android:text="Nintendo Switch\\nLayout Mapping"'),
    ('android:text="PS5手柄自适应扳机"', 'android:text="PS5 DualSense Adaptive Triggers"'),

    # dialog_game_menu_display.xml
    ('android:text="视频信息"', 'android:text="Video Info"'),
    ('android:text="应用配置后，页面关闭，需重新打开串流页面生效！"', 'android:text="Changes will take effect on next streaming session!"'),
    ('android:text="分辨率：1920x1080"', 'android:text="Resolution: 1920x1080"'),
    ('android:text="\\t码率：100 mbps"', 'android:text="\\tBitrate: 100 Mbps"'),
    ('android:text="\\t帧率：60 fps"', 'android:text="\\tFramerate: 60 FPS"'),
    ('android:text="\\t方向：横向"', 'android:text="\\tOrientation: Landscape"'),
    ('android:text="\\t模式：外接显示器"', 'android:text="\\tMode: External Display"'),
    ('android:text="选项"', 'android:text="Options"'),
    ('android:text="分辨率"', 'android:text="Resolution"'),
    ('android:text="模式切换"', 'android:text="Mode Switch"'),
    ('android:text="宽高交换"', 'android:text="Swap W/H"'),
    ('android:text="方向交换"', 'android:text="Swap Orientation"'),
    ('android:text="码率"', 'android:text="Bitrate"'),
    ('android:text="帧率"', 'android:text="Framerate"'),
    ('android:text="解码器"', 'android:text="Decoder"'),
    ('android:text="如果主机软件或显卡不支持编解码器选择，则可能会忽略编解码器选择。"', 'android:text="Codec selection may be ignored if host hardware/software does not support it."'),
    ('android:text="自动"', 'android:text="Auto"'),
    ('android:text="重新打开串流页面生效！"', 'android:text="Reopen stream to apply!"'),
    ('android:text="HDR满亮度"', 'android:text="HDR Max Brightness"'),
    ('android:text="HDR模式下可拉满窗口亮度，默认关闭。"', 'android:text="Maximizes window brightness in HDR mode (default off)."'),
    ('android:text="解码低延迟模式Beta"', 'android:text="Low Latency Decoder (Beta)"'),
    ('android:text="高通8Gen1及以上和联发科9300及以下芯片机型生效！"', 'android:text="Effective on Snapdragon 8 Gen 1+ and Dimensity 9300 and below!"'),
    ('android:text="渲染模式"', 'android:text="Render Mode"'),
    ('android:text="GLES渲染支持FSR和画面处理。"', 'android:text="GLES rendering supports FSR upscaling and shaders."'),
    ('android:text="系统渲染"', 'android:text="System Rendering"'),
    ('android:text="GLES渲染"', 'android:text="GLES Rendering"'),
    ('android:text="3D输出"', 'android:text="3D Output"'),
    ('android:text="支持全宽3840×1080/1200和半宽1920×1080/1200。"', 'android:text="Supports Full SBS 3840x1080/1200 and Half SBS 1920x1080/1200."'),
    ('android:text="左右全宽"', 'android:text="Side-by-Side Full"'),
    ('android:text="左右半宽"', 'android:text="Side-by-Side Half"'),
    ('android:text="景深强度"', 'android:text="Depth Strength"'),
    ('android:text="弱"', 'android:text="Weak"'),
    ('android:text="标准"', 'android:text="Standard"'),
    ('android:text="强"', 'android:text="Strong"'),
    ('android:text="汇聚位置"', 'android:text="Convergence"'),
    ('android:text="近"', 'android:text="Near"'),
    ('android:text="远"', 'android:text="Far"'),
    ('android:text="左右眼"', 'android:text="Left/Right Eye"'),
    ('android:text="正常"', 'android:text="Normal"'),
    ('android:text="交换"', 'android:text="Swap"'),
    ('android:text="FSR 超分"', 'android:text="FSR Upscaling"'),
    ('android:text="选择超分输出目标，HDR由渲染链路自动处理。"', 'android:text="Select upscaling target. HDR handled automatically."'),
    ('android:text="锐化程度"', 'android:text="Sharpness"'),
    ('android:text="柔和"', 'android:text="Soft"'),
    ('android:text="极强"', 'android:text="Ultra Sharp"'),
    ('android:text="FSR HDR输出"', 'android:text="FSR HDR Output"'),
    ('android:text="SDR映射"', 'android:text="SDR Tone Map"'),
    ('android:text="HDR直出"', 'android:text="Native HDR"'),
    ('android:text="忽略HDR校验"', 'android:text="Bypass HDR Check"'),
    ('android:text="虚拟显示器"', 'android:text="Virtual Display"'),
    ('android:text="使用sunshine·阿西西、雷蛇雷游生效，兼容Apollo扩展模式"', 'android:text="Works with Sunshine / Razer Cortex; compatible with Apollo extension mode"'),
    ('android:text="扩展模式"', 'android:text="Extend Mode"'),
    ('android:text="仅虚拟显示屏"', 'android:text="Virtual Display Only"'),
    ('android:text="强制显示模式"', 'android:text="Force Display Mode"'),
    ('android:text="在某些系统(如ColorOS)上启用才能正确设置刷新率/分辨率。"', 'android:text="Enable on certain OS skins (e.g. ColorOS) to properly set resolution/refresh rate."'),
    ('android:text="播放声音"', 'android:text="Audio Output"'),
    ('android:text="本设备发声"', 'android:text="Play on this device"'),
    ('android:text="本设备和PC同时发声"', 'android:text="Play on both PC and this device"'),

    # dialog_game_menu_display_bitrate.xml
    ('android:text="输入码率 单位mbps (只校验非空，别填奇怪的数值)"', 'android:text="Enter bitrate in Mbps (valid numbers only)"'),
    ('android:hint="请输入码率，最大99999"', 'android:hint="Enter bitrate, max 99999"'),
    ('android:text="常用码率"', 'android:text="Presets"'),
    ('android:text="确认"', 'android:text="Confirm"'),
    ('android:text="信息"', 'android:text="Info"'),

    # dialog_game_menu_display_fps.xml
    ('android:text="选择合适的帧率，异常帧率可能黑屏。"', 'android:text="Select appropriate framerate. Unsupported rates may cause black screen."'),
    ('android:hint="请输入帧率"', 'android:hint="Enter framerate"'),
    ('android:text="常用帧率"', 'android:text="Presets"'),

    # dialog_game_menu_display_resolution.xml
    ('android:text="输入宽和高 (保存并使用)"', 'android:text="Enter width and height (Save & Apply)"'),
    ('android:text="宽度"', 'android:text="Width"'),
    ('android:hint="请输入宽度，比如1920"', 'android:hint="Enter width, e.g. 1920"'),
    ('android:text="高度"', 'android:text="Height"'),
    ('android:hint="请输入高度，比如1080"', 'android:hint="Enter height, e.g. 1080"'),
    ('android:text="常用分辨率"', 'android:text="Presets"'),
    ('android:text="本机"', 'android:text="Native"'),
    ('android:text="自定义分辨率 (长按删除)"', 'android:text="Custom Resolutions (Long press to delete)"'),

    # dialog_game_menu_function.xml
    ('android:text="快捷操作"', 'android:text="Quick Actions"'),
    ('android:text="显示器1"', 'android:text="Display 1"'),
    ('android:text="显示器2"', 'android:text="Display 2"'),
    ('android:text="显示器3"', 'android:text="Display 3"'),
    ('android:text="显示器4"', 'android:text="Display 4"'),
    ('android:text="注销"', 'android:text="Sign Out"'),
    ('android:text="关机"', 'android:text="Shut Down"'),
    ('android:text="睡眠"', 'android:text="Sleep"'),
    ('android:text="重启"', 'android:text="Restart"'),
    ('android:text="任务管理器"', 'android:text="Task Manager"'),
    ('android:text="发送剪切板"', 'android:text="Send Clipboard"'),
    ('android:text="打开剪切板"', 'android:text="Open Clipboard"'),
    ('android:text="Win系统设置"', 'android:text="Windows Settings"'),
    ('android:text="我的电脑"', 'android:text="This PC"'),
    ('android:text="移动中心"', 'android:text="Mobility Center"'),
    ('android:text="显示器模式"', 'android:text="Display Mode"'),
    ('android:text="HDR开关"', 'android:text="Toggle HDR"'),

    # dialog_game_menu_game_pad_add.xml
    ('android:text="手柄按键"', 'android:text="Gamepad Buttons"'),

    # dialog_game_menu_keyboard_group_add.xml
    ('android:text="组合键"', 'android:text="Combo Keys"'),
    ('android:text="清空"', 'android:text="Clear"'),
    ('android:text="保存"', 'android:text="Save"'),
    ('android:text="按键名称"', 'android:text="Key Name"'),
    ('android:hint="请输入按键名称，不易过长~"', 'android:hint="Enter button name (keep it short)"'),
    ('android:text="组合键值"', 'android:text="Combo Keycode"'),
    ('android:hint="请输入1~5个按键"', 'android:hint="Enter 1 to 5 keys"'),
    ('android:text="电脑全键盘"', 'android:text="Full Keyboard"'),
    ('android:text="数字键盘"', 'android:text="Numpad"'),
    ('android:text="鼠标与轮盘按键"', 'android:text="Mouse & Wheel Buttons"'),
    ('android:text="功能按键"', 'android:text="Function Keys"'),

    # dialog_game_menu_list.xml / item_game_menu_list.xml
    ('android:text="触控模式"', 'android:text="Touch Mode"'),
    ('android:text="新增"', 'android:text="Add"'),

    # dialog_game_menu_setting.xml
    ('android:text="完整性能"', 'android:text="Full Overlay"'),
    ('android:text="悬浮球"', 'android:text="Floating Button"'),
    ('android:text="悬浮球\\n记住位置"', 'android:text="Floating Button\\nRemember Position"'),
    ('android:text="设备静音"', 'android:text="Mute Device"'),
    ('android:text="关闭缩放后\\n保留画面"', 'android:text="Retain View\\nAfter Zoom Off"'),
    ('android:text="ESC 呼出\\n游戏菜单"', 'android:text="ESC Opens\\nGame Menu"'),
    ('android:text="悬浮球点击操作"', 'android:text="Floating Button Tap Action"'),
    ('android:text="游戏菜单"', 'android:text="Game Menu"'),
    ('android:text="软键盘"', 'android:text="OSK"'),
    ('android:text="精简性能信息"', 'android:text="Lite Overlay Stats"'),
    ('android:text="显示更多\\n扩展参数"', 'android:text="Show Extended\\nParameters"'),
    ('android:text="点击打开\\n游戏菜单"', 'android:text="Tap to Open\\nGame Menu"'),
    ('android:text="显示震动信息"', 'android:text="Show Rumble Stats"'),
    ('android:text="游戏菜单 摇杆鼠标 快捷键"', 'android:text="Game Menu Stick-Mouse Shortcut"'),
    ('android:text="开始键【长按】"', 'android:text="Start [Long Press]"'),
    ('android:text="Xbox键【单击】"', 'android:text="Xbox [Single Tap]"'),
    ('android:text="视图键【长按】"', 'android:text="Back/View [Long Press]"'),
    ('android:text="Z键【单击】"', 'android:text="Z Key [Single Tap]"'),
    ('android:text="多点触控打开软键盘"', 'android:text="Multi-touch Opens OSK"'),
    ('android:text="三指"', 'android:text="3 Fingers"'),
    ('android:text="四指"', 'android:text="4 Fingers"'),
    ('android:text="五指"', 'android:text="5 Fingers"'),
    ('android:text="设备震动相关"', 'android:text="Device Vibration Options"'),
    ('android:text="震动停止方案A"', 'android:text="Rumble Stop Plan A"'),
    ('android:text="强烈震动"', 'android:text="Strong Rumble"'),
    ('android:text="手柄陀螺仪模拟右摇杆 Beta"', 'android:text="Gamepad Gyro Emulates Right Stick (Beta)"'),
    ('android:text="启用"', 'android:text="Enabled"'),
    ('android:text="按下左扳机启用"', 'android:text="Hold Left Trigger to Enable"'),
    ('android:text="反转XY轴"', 'android:text="Invert X/Y Axes"'),
    ('android:text="强制体感灵敏度：120%"', 'android:text="Gyro Sensitivity: 120%"'),
    ('android:text="性能信息 缩放：100%"', 'android:text="Overlay Scale: 100%"'),
    ('android:text="性能信息 边距：4"', 'android:text="Overlay Margin: 4"'),

    # dialog_game_menu_touch.xml
    ('android:text="恢复默认"', 'android:text="Reset Defaults"'),
    ('android:text="多点触控灵敏度"', 'android:text="Multi-Touch Sensitivity"'),
    ('android:text="选项会保存到磁盘中，一直有效！"', 'android:text="Settings will be saved to disk persistently!"'),
    ('android:text="灵敏度开启"', 'android:text="Enable Sensitivity"'),
    ('android:text="自动回中"', 'android:text="Auto Center"'),
    ('android:text="全局生效"', 'android:text="Global Apply"'),
    ('android:text="X轴:100%"', 'android:text="X-Axis: 100%"'),
    ('android:text="Y轴:100%"', 'android:text="Y-Axis: 100%"'),
    ('android:text="触控板模式灵敏度（默认启用没有开关）"', 'android:text="Trackpad Mode Sensitivity"'),
    ('android:text="触控板控件灵敏度（默认启用没有开关）"', 'android:text="On-Screen Trackpad Widget Sensitivity"'),
    ('android:text="手柄键鼠模式 鼠标指针灵敏度"', 'android:text="Gamepad Mouse Mode Pointer Sensitivity"'),
    ('android:text="灵敏度:100%"', 'android:text="Sensitivity: 100%"'),
    ('android:text="虚拟鼠标滚轮移动距离"', 'android:text="Virtual Mouse Scroll Distance"'),
    ('android:text="距离:5"', 'android:text="Distance: 5"'),
    ('android:text="触控板外设灵敏度"', 'android:text="Physical Trackpad Sensitivity"'),
    ('android:text="滚轮速度:5"', 'android:text="Scroll Speed: 5"'),

    # dialog_game_menu_virtual_gamepad.xml
    ('android:text="虚拟手柄与虚拟按键"', 'android:text="Virtual Gamepad & Virtual Controls"'),
    ('android:text="更新配置"', 'android:text="Update Config"'),
    ('android:text="模式切换:需要先打开虚拟手柄开关~"', 'android:text="Mode switch: Turn on virtual gamepad first"'),
    ('android:text="默认"', 'android:text="Default"'),
    ('android:text="编辑模式"', 'android:text="Edit Mode"'),
    ('android:text="默认布局方案"', 'android:text="Default Layout Preset"'),
    ('android:text="方案1"', 'android:text="Preset 1"'),
    ('android:text="方案2"', 'android:text="Preset 2"'),
    ('android:text="方案3"', 'android:text="Preset 3"'),
    ('android:text="方案4"', 'android:text="Preset 4"'),
    ('android:text="方案5"', 'android:text="Preset 5"'),
    ('android:text="模式切换:需要先打开虚拟按键开关~"', 'android:text="Mode switch: Turn on virtual controls first"'),
    ('android:text="通用"', 'android:text="General"'),
    ('android:text="如果按键布局出现过，点击右上角按钮刷新"', 'android:text="If layout glitched, tap top-right button to refresh"'),
    ('android:text="按键震动"', 'android:text="Button Haptic Feedback"'),
    ('android:text="虚拟手柄震动"', 'android:text="Virtual Gamepad Rumble"'),
    ('android:text="控件默认模式颜色(手柄与按键通用)"', 'android:text="Control Color Theme (Gamepad & Buttons)"'),
    ('android:text="黑色"', 'android:text="Black"'),
    ('android:text="白色"', 'android:text="White"'),
    ('android:text="灰色"', 'android:text="Gray"'),
    ('android:text="控件透明度(手柄与按键通用)"', 'android:text="Control Opacity (Gamepad & Buttons)"'),
    ('android:text="不透明度:100%"', 'android:text="Opacity: 100%"'),
    ('android:text="全键盘面板透明度"', 'android:text="Full Keyboard Opacity"'),
    ('android:text="不透明度：100%"', 'android:text="Opacity: 100%"'),
    ('android:text="全键盘高度"', 'android:text="Full Keyboard Height"'),
    ('android:text="高度:200"', 'android:text="Height: 200"'),
    ('android:text="虚拟手柄按键缩放"', 'android:text="Virtual Gamepad Button Scale"'),
    ('android:text="缩放：100%"', 'android:text="Scale: 100%"'),

    # dialog_update_channels.xml
    ('android:text="选择下载渠道"', 'android:text="Select Download Channel"'),
    ('android:text="可根据你的习惯选择下载渠道。"', 'android:text="Choose your preferred download channel."'),

    # dialog_update_prompt.xml
    ('android:text="发现新版本"', 'android:text="Update Available"'),
    ('android:text="新版本已经准备好了，可以查看更新内容后选择下载。"', 'android:text="A new version is ready. Check release notes and download."'),
    ('android:text="版本信息"', 'android:text="Version Info"'),
    ('android:text="更新内容"', 'android:text="Changelog"'),
    ('android:text="跳过本次更新"', 'android:text="Skip This Version"'),
    ('android:text="下载"', 'android:text="Download"'),

    # item_layout_axixi_keyboard.xml & digitpad & mouse
    ('android:text="空格"', 'android:text="Space"'),
    ('android:text="左键"', 'android:text="L-Click"'),
    ('android:text="中键"', 'android:text="M-Click"'),
    ('android:text="右键"', 'android:text="R-Click"'),
    ('android:text="回车"', 'android:text="Enter"'),
    ('android:text="滚轮⬆"', 'android:text="Wheel ⬆"'),
    ('android:text="滚轮⬇"', 'android:text="Wheel ⬇"'),
    ('android:text="触控板"', 'android:text="Trackpad"'),
    ('android:text="常规模式"', 'android:text="Normal Mode"'),

    # layout_axixi_keyboard.xml
    ('android:text="电脑全键盘"', 'android:text="Full PC Keyboard"'),
    ('android:text="数字键盘"', 'android:text="Numpad"'),
    ('android:text="组合键模式"', 'android:text="Combo Keys Mode"'),
    ('android:text="手机软键盘"', 'android:text="On-Screen Keyboard"'),
]

def translate_layouts():
    folders = ['app/src/main/res/layout', 'app/src/main/res/layout-land']
    updated_files = 0
    for folder in folders:
        for file in sorted(os.listdir(folder)):
            if file.endswith('.xml'):
                filepath = os.path.join(folder, file)
                with open(filepath, 'r', encoding='utf-8', newline='') as f:
                    content = f.read()
                orig_content = content
                for old, new in REPLACEMENTS:
                    old_crlf = old.replace('\n', '\r\n')
                    old_lf = old.replace('\r\n', '\n')
                    if old in content:
                        content = content.replace(old, new)
                    elif old_crlf in content:
                        content = content.replace(old_crlf, new.replace('\n', '\r\n'))
                    elif old_lf in content:
                        content = content.replace(old_lf, new.replace('\r\n', '\n'))
                if content != orig_content:
                    with open(filepath, 'w', encoding='utf-8', newline='') as f:
                        f.write(content)
                    updated_files += 1
                    print(f"Updated: {filepath}")

    print(f"\nTotal layout files updated: {updated_files}")

if __name__ == '__main__':
    translate_layouts()
