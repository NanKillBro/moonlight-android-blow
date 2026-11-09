import sys
import os

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

def translate_preferences():
    filepath = 'app/src/main/res/xml/preferences.xml'
    with open(filepath, 'r', encoding='utf-8', newline='') as f:
        content = f.read()

    replacements = [
        ('android:dialogTitle="输入视频码率Mbps"', 'android:dialogTitle="Enter Video Bitrate (Mbps)"'),
        (
'''android:summary="如果你感觉Seek控件滑动不太好用，可以选择手动输入。\\n超过Seek滑动最大值，可能不显示但是串流时是生效的~"''',
'''android:summary="Manually input video bitrate instead of using the slider.\\nValues exceeding slider maximum still take effect during stream."'''
        ),
        ('android:dialogMessage="请输入数字，小数点只能识别到x.5，超过会四舍五入~"', 'android:dialogMessage="Enter a number (supports .5 increments)"'),
        ('android:title="强制设置视频码率（覆盖上方滑动码率）"', 'android:title="Force Custom Video Bitrate"'),
        ('android:title="优化解码低延迟模式(Beta)"', 'android:title="Low Latency Decoder Optimization (Beta)"'),
        ('android:summary="(实验性) 高通8Gen1及以上和联发科9300及以下芯片机型生效。"', 'android:summary="(Experimental) Effective for Snapdragon 8 Gen 1+ and Dimensity 9300 and below."'),
        ('android:title="小米玄戒 O1 优化"', 'android:title="Xiaomi Xuanjie O1 Optimization"'),
        ('android:summary="仅小米玄戒 O1 机型生效，启用后使用专属解码兼容与低延迟优化；关闭则保持原逻辑。"', 'android:summary="Applies dedicated low latency decoder compatibility optimization for Xiaomi Xuanjie O1."'),
        ('android:title="渲染模式"', 'android:title="Render Mode"'),
        ('android:summary="GLES 渲染支持 FSR 和画面处理功能。"', 'android:summary="GLES rendering supports FSR and post-processing features."'),
        ('android:title="3D输出"', 'android:title="3D Output"'),
        ('android:summary="全宽输出3840×1080/1200，半宽输出1920×1080/1200；仅支持GLES渲染。"', 'android:summary="Full SBS outputs 3840x1080/1200, Half SBS outputs 1920x1080/1200 (GLES only)."'),
        ('android:title="3D景深"', 'android:title="3D Depth"'),
        ('android:summary="控制左右眼最大视差，建议从标准开始。"', 'android:summary="Controls stereo parallax. Recommended to start with Standard."'),
        ('android:title="3D汇聚"', 'android:title="3D Convergence"'),
        ('android:summary="调整画面位于屏幕前后的基准位置。"', 'android:summary="Adjusts screen plane convergence depth."'),
        ('android:title="交换左右眼"', 'android:title="Swap Left/Right Eye"'),
        ('android:summary="当远近关系相反或眼镜眼序不一致时开启。"', 'android:summary="Enable if 3D glasses eye order is inverted."'),
        ('android:title="超分目标"', 'android:title="Upscaling Target"'),
        ('android:summary="GLES 渲染下启用 FSR 超分到 2K 或 4K。"', 'android:summary="Enable FSR upscaling to 2K or 4K under GLES rendering."'),
        ('android:title="锐化程度"', 'android:title="Sharpness Strength"'),
        ('android:summary="仅在启用 FSR 超分时生效，数值越高边缘越锐利。"', 'android:summary="Effective when FSR is enabled. Higher values produce sharper edges."'),
        ('android:title="FSR HDR输出"', 'android:title="FSR HDR Output"'),
        ('android:summary="兼容 SDR 映射更稳定；原生 HDR 直出为实验性，需要设备支持 BT2020 PQ。"', 'android:summary="Compatible SDR Tone Mapping is more stable; Native HDR Output requires BT2020 PQ support."'),
        ('android:title="填充刘海区域"', 'android:title="Fill Display Cutout / Notch Area"'),
        ('android:title="横竖屏自由切换"', 'android:title="Auto-Rotate Screen Orientation"'),
        ('android:title="画面显示位置（默认居中）"', 'android:title="Screen Alignment (Default Center)"'),
        ('android:summary="可能对折叠屏手机或者平板有点帮助,请自行DIY分辨率和画面位置。"', 'android:summary="Aligns video stream on foldable devices or tablets with custom resolutions."'),
        ('android:title="部分页面主题色为白色"', 'android:title="Light Theme for Certain Pages"'),
        ('android:summary="安卓10及以上生效"', 'android:summary="Effective on Android 10+"'),
        ('android:title="反转握把震动"', 'android:title="Invert Grip Rumble Motors"'),
        ('android:summary="如果你发现扣动左扳机是右边握把震动，则开启此选项。"', 'android:summary="Inverts left/right rumble motors if trigger haptics are reversed."'),
        ('android:title="禁用默认13%的手柄扳机死区"', 'android:title="Disable Default 13% Trigger Deadzone"'),
        ('android:summary="勾选后 手柄扳机死区 Moonlight不做限制【某些ASUS Gamepad设备除外】。"', 'android:summary="Removes default trigger deadzone clamping (except certain ASUS gamepads)."'),
        ('android:title="触控/鼠标模式 【默认多点触控】"', 'android:title="Touch / Mouse Mode"'),
        ('android:summary="可选择一种鼠标模式，多点触控需要搭配sunshine使用~"', 'android:summary="Select mouse/touch mode (multi-touch requires Sunshine host)."'),
        ('android:title="使用本地鼠标光标"', 'android:title="Use Local System Mouse Cursor"'),
        ('android:summary="默认外接物理鼠标的光标会被捕获，此选项可显示安卓系统光标"', 'android:summary="Displays Android system cursor instead of capturing pointer for host-rendered cursor."'),
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
    print("Updated preferences.xml part 2")

if __name__ == '__main__':
    translate_preferences()
