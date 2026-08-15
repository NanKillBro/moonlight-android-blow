import sys
import os
import re

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

def translate_preferences():
    filepath = 'app/src/main/res/xml/preferences.xml'
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    replacements = [
        ('android:title="默认布局方案"', 'android:title="Default Layout Preset"'),
        ('android:summary="横竖屏支持单独配置。"', 'android:summary="Landscape and portrait modes can be configured separately."'),
        ('android:summary="开启后，虚拟手柄摇杆无法触发L3和R3"', 'android:summary="When enabled, virtual stick center deadzone prevents triggering L3 and R3."'),
        ('android:title="禁用虚拟手柄摇杆中心区域"', 'android:title="Disable Virtual Analog Stick Center Area"'),
        ('android:title="导入虚拟手柄配置"', 'android:title="Import Virtual Gamepad Preset"'),
        ('android:summary="选择一个配置文件，覆盖默认选择的布局方案。(仅横屏模式)"', 'android:summary="Select a configuration file to overwrite the selected layout preset. (Landscape only)"'),
        ('android:title="导出虚拟手柄配置"', 'android:title="Export Virtual Gamepad Preset"'),
        ('android:summary="导出默认选择的布局方案的配置文件。(仅横屏模式)"', 'android:summary="Export configuration file for the selected layout preset. (Landscape only)"'),
        ('android:title="开启Lite精简模式"', 'android:title="Enable Lite Performance Overlay"'),
        ('android:summary="展示简化版性能信息：网速/延迟/解码/丢包率/FPS"', 'android:summary="Show compact performance stats: Bitrate / Latency / Decoder / Packet Loss / FPS"'),
        ('android:title="Lite精简模式点击弹出快捷选项"', 'android:title="Tap Lite Overlay for Quick Menu"'),
        ('android:summary="代替返回键逻辑，弹出游戏快捷菜单。"', 'android:summary="Opens in-game quick menu instead of back button behavior."'),
        ('android:title="Lite精简模式扩展参数"', 'android:title="Lite Overlay Extended Stats"'),
        ('android:summary="开启后，增加分辨率、HDR、解码器等参数。"', 'android:summary="Adds resolution, HDR, decoder, and other details to the overlay."'),
        ('android:dialogMessage="设置精简性能信息距屏幕顶部边距，默认是4dp"', 'android:dialogMessage="Set the top margin for Lite performance overlay, default is 4dp"'),
        ('android:summary="设置精简性能信息距屏幕顶部边距，默认是4dp"', 'android:summary="Set the top margin for Lite performance overlay, default is 4dp"'),
        ('android:title="精简性能控件距顶部距离"', 'android:title="Lite Overlay Top Margin"'),
        ('<PreferenceCategory android:title="阿西西的日常设置"', '<PreferenceCategory android:title="Custom Fork Settings"'),
        ('android:dialogTitle="设置完分辨率后，退出设置页面 重新打开生效！"', 'android:dialogTitle="After setting resolution, re-enter settings to apply!"'),
        (
'''android:summary="添加一个自定义分辨率,x号分割,比较奇怪的分辨率可能无法生效。
            \\n例如：1920x1080
            \\n非原生分辨率如果是刘海屏可能不会默认填充刘海区域，
            \\n如果画面比例一样，可手动设置拉伸画面来充满全屏"''',
'''android:summary="Add a custom resolution formatted as WxH (e.g. 1920x1080).\\nNon-standard resolutions may not fill notch areas by default;\\nstretch to full screen can be enabled if aspect ratios match."'''
        ),
        ('android:title="自定义分辨率"', 'android:title="Custom Resolution"'),
        ('android:title="竖屏显示模式"', 'android:title="Portrait Display Mode"'),
        ('android:summary="搭配自定义分辨率使用，确保你使用的串流端支持并且PC端分辨率是竖直方向"', 'android:summary="Use with custom resolutions; ensure host stream supports vertical resolutions."'),
        ('android:title="兼容Switch JoyCon手柄"', 'android:title="Switch Joy-Con Compatibility"'),
        ('android:summary="如果你的JoyCon无法使用或识别按键有问题，可以尝试开启此功能。适配Android 10及以上"', 'android:summary="Try enabling this if your Joy-Con has button mapping issues. (Android 10+)"'),
        (
'''android:summary="在可用时汇报手柄电池状态。\\n如果在使用触摸屏/触摸板/手写笔/鼠标时偶尔有卡顿现象发生，关闭此选项可能会有用。"''',
'''android:summary="Report controller battery status when available.\\nDisabling this may reduce stutters when using touchscreen/trackpad/mouse."'''
        ),
        ('android:title="启用手柄电池状态报告"', 'android:title="Enable Controller Battery Status Reporting"'),
        ('android:title="启用悬浮球（Beta）"', 'android:title="Enable Floating Button (Beta)"'),
        ('android:summary="开启后，点击打开快捷菜单。"', 'android:summary="When enabled, tap floating button to open quick menu."'),
        ('android:title="虚拟全键盘透明度"', 'android:title="Full Virtual Keyboard Opacity"'),
        ('android:summary="调整虚拟全键盘的高度"', 'android:summary="Adjust height of full virtual keyboard"'),
        ('android:title="虚拟全键盘高度"', 'android:title="Full Virtual Keyboard Height"'),
        ('android:title="全键盘组合键模式"', 'android:title="Full Keyboard Combo Key Mode"'),
        ('android:summary="勾选后默认为选中组合键模式"', 'android:summary="Default to combo key mode when checked"'),
        ('android:title="外接显示器模式（Beta）"', 'android:title="External Display Mode (Beta)"'),
        ('android:summary="串流画面显示在显示器，虚拟按键及性能信息等控件在手机屏幕。"', 'android:summary="Streams video to external display while showing virtual controls and overlay on phone screen."'),
        ('android:title="强制使用设备本身的震动马达"', 'android:title="Force Device Vibration Motor"'),
        ('android:summary="你如果对连接的手柄本身震动效果不满意，可以开启此选项！【对强制使用月光自带USB驱动无效】"', 'android:summary="Uses the phone vibration motor for game rumble instead of the connected controller."'),
        ('android:title="虚拟手柄使用设备本身的陀螺仪"', 'android:title="Virtual Gamepad Gyroscope"'),
        (
'''android:summary="如果你希望虚拟手柄支持陀螺仪功能，开启此选项。\\n可能需要在sunshine后台设置手柄强制为ps4手柄。\\n建议连接物理手柄时关闭此选项。"''',
'''android:summary="Enables phone gyro for virtual gamepad motion controls.\\n(May require configuring Sunshine controller type as PS4 controller)"'''
        ),
        ('android:title="禁用默认的特殊按键指令(快捷键)"', 'android:title="Disable Default Shortcut Keys"'),
        ('android:summary="如果你感觉内置的指令对你没什么用的话，可以禁用，使用自己导入的。"', 'android:summary="Disable built-in shortcuts to use your own custom imported shortcuts only."'),
        ('android:title="禁用游戏模式"', 'android:title="Disable Game Mode"'),
        ('android:summary="可能对Quest 安卓13及以上版本有用"', 'android:summary="May help on Meta Quest devices running Android 13+"'),
        ('android:title="导入自定义无障碍配置文件"', 'android:title="Import Custom Accessibility Config"'),
        ('android:summary="每次都会覆盖原来的，请注意备份。"', 'android:summary="Overwrites current accessibility config file. Please backup before importing."'),
        ('android:title="无障碍键盘模式显示捕获的键值"', 'android:title="Show Captured Keycodes in Accessibility Mode"'),
        ('android:summary="打开无障碍键盘，在月光app任意界面，输入按键，会弹出键值，用于自定义无障碍配置文件使用。"', 'android:summary="Displays keycode toast when pressing keys in accessibility keyboard mode."'),
        ('<PreferenceCategory android:title="虚拟按键"', '<PreferenceCategory android:title="Virtual Controls"'),
        ('android:title="显示虚拟按键"', 'android:title="Show Virtual Controls"'),
        (
'''android:summary="在触摸屏上显示一层虚拟特殊按键。
            \\n按键透明度与上方选项中虚拟手柄共用。"''',
'''android:summary="Show on-screen virtual buttons overlay.\\nOpacity is shared with virtual gamepad."'''
        ),
        ('android:summary="点按屏幕按键时，会触发手机马达震动，此选项也可用于虚拟手柄按钮。"', 'android:summary="Vibrate phone when pressing on-screen controls."'),
        ('android:title="导入虚拟按键配置"', 'android:title="Import Virtual Controls Preset"'),
        ('android:summary="选择一个配置文件，覆盖默认选择的布局方案。(仅横屏模式)"', 'android:summary="Select a config file to overwrite the selected layout preset. (Landscape only)"'),
        ('android:title="导出虚拟按键配置"', 'android:title="Export Virtual Controls Preset"'),
        ('android:summary="导出默认选择的布局方案的配置文件。(仅横屏模式)"', 'android:summary="Export selected layout preset configuration file. (Landscape only)"'),
        ('<PreferenceCategory android:title="音频震动Beta"', '<PreferenceCategory android:title="Audio Haptics (Beta)"'),
        ('android:title="启用音频震动"', 'android:title="Enable Audio Haptics"'),
        ('android:summary="把串流音频转换成震动反馈，更适合爆炸、撞击、低频场景"', 'android:summary="Converts streaming audio to haptic rumble for explosions, impacts, and bass effects."'),
        ('android:title="音频震动输出目标"', 'android:title="Audio Haptics Output Target"'),
        ('android:summary="选择输出到手机，或输出到已接入的手柄"', 'android:summary="Output haptics to phone motor or connected gamepad."'),
        ('android:summary="调整手机或者手柄音频震动强度。"', 'android:summary="Adjust audio haptics vibration strength."'),
        ('android:title="音频震动强度"', 'android:title="Audio Haptics Strength"'),
        ('android:title="语音过滤"', 'android:title="Voice Filter"'),
        ('android:summary="降低人声、语音聊天、播报声对震动的触发"', 'android:summary="Reduces rumble triggered by voice chat and dialogues."'),
        ('android:title="保留普通手柄震动"', 'android:title="Keep Standard Gamepad Rumble"'),
        ('android:summary="当输出目标为手柄时，是否继续保留游戏原本的手柄震动。默认关闭。"', 'android:summary="Retain native game rumble when haptics output target is set to gamepad."'),
        ('<PreferenceCategory android:title="备份恢复数据【注意数据安全】"', '<PreferenceCategory android:title="Backup &amp; Restore Data"'),
        ('android:title="导出配对的电脑数据库文件"', 'android:title="Export Paired Host Database"'),
        ('android:summary="导出一个db格式的sqlite数据库文件"', 'android:summary="Export host pairings as an SQLite .db file"'),
        ('android:title="导出网络请求的证书文件"', 'android:title="Export Network Certificate"'),
        ('android:summary="导出一个crt格式的证书文件"', 'android:summary="Export client certificate (.crt file)"'),
        ('android:title="导出网络请求的key文件"', 'android:title="Export Network Key"'),
        ('android:summary="导出一个key格式的验证文件"', 'android:summary="Export client private key (.key file)"'),
        ('android:title="导入配对的电脑数据库文件"', 'android:title="Import Paired Host Database"'),
        ('android:summary="选择db数据库文件，会覆盖更新原有的电脑列表，需要重新打开APP生效。"', 'android:summary="Import host SQLite database file (overwrites current list, restart app to apply)."'),
        ('android:title="导入网络请求的证书文件"', 'android:title="Import Network Certificate"'),
        ('android:summary="导入一个crt格式的证书文件"', 'android:summary="Import client certificate (.crt file)"'),
        ('android:title="导入网络请求的key文件"', 'android:title="Import Network Key"'),
        ('android:summary="导入一个key格式的验证文件"', 'android:summary="Import client private key (.key file)"'),
        ('<PreferenceCategory android:title="主屏幕设置"', '<PreferenceCategory android:title="Home Screen Settings"'),
        ('android:title="使用自定义背景图"', 'android:title="Use Custom Background Image"'),
        ('android:summary="不勾选则使用默认背景,安卓10以上支持"', 'android:summary="Use custom wallpaper on home screen (Android 10+)"'),
        ('android:title="设置主屏幕背景图"', 'android:title="Set Home Screen Background"'),
        (
'''android:summary="选择一张图片，旋转屏幕生效~\\n容错率不是很高，所以图片大小和类型别太过分，小心崩溃~\\n如果崩溃了清除数据可解决~"''',
'''android:summary="Choose an image for home screen wallpaper.\\n(Rotate screen or restart app to apply)"'''
        ),
        ('android:title="背景图高斯模糊"', 'android:title="Background Gaussian Blur"'),
        ('android:summary="自定义背景图是否进行高斯模糊处理，安卓12以上支持。"', 'android:summary="Apply Gaussian blur to custom wallpaper (Android 12+)"'),
        ('android:dialogTitle="设置主屏幕左侧文本"', 'android:dialogTitle="Set Home Screen Title Text"'),
        ('android:summary="输入你喜欢的文本"', 'android:summary="Custom title text displayed on home screen"'),
        ('android:dialogMessage="输入你喜欢的文本~"', 'android:dialogMessage="Enter title text for home screen"'),
        ('android:title="设置主屏幕左侧文本"', 'android:title="Home Screen Title Text"'),
        ('android:title="忽略掉应用列表菜单选项"', 'android:title="Direct Launch App (Skip Menu)"'),
        ('android:summary="开启此功能，点击图标可直接进入串流界面，无需再点击弹出的菜单选项。"', 'android:summary="Directly launch stream when clicking an app icon without opening popup menu."'),
        ('<PreferenceCategory android:title="关于"', '<PreferenceCategory android:title="About"'),
        ('android:title="关于我们"', 'android:title="About"'),
        ('android:summary="版本信息·获取更新·关注作者"', 'android:summary="Version info, updates, and credits"'),
        ('android:title="Moonlight帮助指南"', 'android:title="Moonlight Setup Guide"'),
        ('android:summary="官方使用文档"', 'android:summary="Official documentation and guides"'),
        ('android:title="串流日志">', 'android:title="Stream Logs">'),
        ('android:title="串流日志采集"', 'android:title="Stream Log Collection"'),
        ('android:summary="每次串流生成一份新日志，用于记录连接、画面、网络、手柄和异常中断；默认关闭"', 'android:summary="Generates session logs recording connection, video, network, gamepad, and crash events."'),
        ('android:title="日志列表"', 'android:title="Log File List"'),
        ('android:summary="查看、导出或删除已保存的串流日志"', 'android:summary="View, export, or delete saved stream logs"'),
    ]

    for old, new in replacements:
        old_crlf = old.replace('\n', '\r\n')
        old_lf = old.replace('\r\n', '\n')
        if old in content:
            content = content.replace(old, new)
        elif old_crlf in content:
            content = content.replace(old_crlf, new.replace('\n', '\r\n'))
        elif old_lf in content:
            content = content.replace(old_lf, new.replace('\r\n', '\n'))
        else:
            print(f"Warning: pattern not found in preferences.xml:\n{old[:50]}")

    with open(filepath, 'w', encoding='utf-8', newline='') as f:
        f.write(content)
    print("Updated preferences.xml")

if __name__ == '__main__':
    translate_preferences()
