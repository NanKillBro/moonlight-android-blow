import os
import json
import sys

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

def translate_configs():
    # 1. buttonSwitch.json
    p_button_switch = 'app/src/main/assets/config/buttonSwitch.json'
    if os.path.exists(p_button_switch):
        with open(p_button_switch, 'r', encoding='utf-8', newline='') as f:
            c = f.read()
        c = c.replace('无障碍模式 按键映射对应关系 键值：https://developer.android.com/reference/android/view/KeyEvent', 'Accessibility mode key mappings. Keycodes: https://developer.android.com/reference/android/view/KeyEvent')
        c = c.replace('win键 这个值给自己看的，程序不需要', 'Win Key (User reference note)')
        with open(p_button_switch, 'w', encoding='utf-8', newline='') as f:
            f.write(c)
        print("Updated buttonSwitch.json")

    # 2. config_keyboard.txt
    p_config_kb = 'app/src/main/assets/config/config_keyboard.txt'
    if os.path.exists(p_config_kb):
        with open(p_config_kb, 'r', encoding='utf-8', newline='') as f:
            c = f.read()
        c = c.replace('"name":"桌面"', '"name":"Desktop"')
        c = c.replace('"desc":"常规模式"', '"desc":"Normal Mode"')
        c = c.replace('"desc":"锁定模式"', '"desc":"Lock Mode"')
        c = c.replace('"name":"鼠标·左键"', '"name":"Mouse Left"')
        c = c.replace('"name":"鼠标·右键"', '"name":"Mouse Right"')
        c = c.replace('"name":"触控板·右"', '"name":"Trackpad Right"')
        c = c.replace('"desc":"右键"', '"desc":"Right Click"')
        with open(p_config_kb, 'w', encoding='utf-8', newline='') as f:
            f.write(c)
        print("Updated config_keyboard.txt")

    # 3. keyboard.json & keyboard_1.json & keyboard_2.json
    for kb_file in ['keyboard.json', 'keyboard_1.json', 'keyboard_2.json']:
        p_kb = os.path.join('app/src/main/assets/config', kb_file)
        if os.path.exists(p_kb):
            with open(p_kb, 'r', encoding='utf-8', newline='') as f:
                c = f.read()
            c = c.replace('rocker=摇杆|dpad=十字键|keystroke=普通按钮', 'rocker=Stick|dpad=D-Pad|keystroke=Button')
            c = c.replace('"name": "摇杆"', '"name": "Stick"')
            c = c.replace('"name": "十字键"', '"name": "D-Pad"')
            c = c.replace('"name": "触控板(右)"', '"name": "Trackpad (Right)"')
            c = c.replace('"name": "触控板"', '"name": "Trackpad"')
            c = c.replace('"name": "触控板(左)"', '"name": "Trackpad (Left)"')
            c = c.replace('"name": "触控板(中)"', '"name": "Trackpad (Middle)"')
            c = c.replace('"name": "触控板(无)"', '"name": "Trackpad (Look)"')
            c = c.replace('简单描述下，上下左右中按键code值为keycode查阅附赠的keycode-android.java文件获取，elementId值是唯一的,middleCode是中键的小圆点，双击可以触发', 'Stick keycodes for up/down/left/right/center. Double tap center dot triggers middleCode.')
            c = c.replace('简单描述下，上下左右按键code值为keycode查阅附赠的keycode-android.java文件获取，elementId值是唯一的', 'D-Pad keycodes for up/down/left/right.')
            c = c.replace('简单描述下，code值固定，name为按钮显示文字，ML左键、MM中键、MR右键', 'Mouse button configuration: ML=Left, MM=Middle, MR=Right')
            c = c.replace('特殊触控板按键适合魔兽转视野，name的数值可以清空，但是怕不好区分，可以修改成其他的', 'Special trackpad button for camera panning')
            c = c.replace('普通触控板控件', 'Standard on-screen trackpad widget')
            c = c.replace('一直按着左键不放~', 'Hold down left mouse button')
            c = c.replace('一直按着鼠标中键不放~', 'Hold down middle mouse button')
            c = c.replace('普通触控板控件没有点击事件', 'Trackpad widget without tap-to-click')
            with open(p_kb, 'w', encoding='utf-8', newline='') as f:
                f.write(c)
            print(f"Updated {kb_file}")

    # 4. specialbuttons.json
    p_special = 'app/src/main/assets/config/specialbuttons.json'
    if os.path.exists(p_special):
        with open(p_special, 'r', encoding='utf-8', newline='') as f:
            c = f.read()
        c = c.replace('游戏快捷菜单中快捷指令，键值参考PC端：https://learn.microsoft.com/en-us/windows/win32/inputdev/virtual-key-codes', 'Quick menu shortcuts. Virtual keycodes reference: https://learn.microsoft.com/en-us/windows/win32/inputdev/virtual-key-codes')
        c = c.replace('"name": "自定义导入数据 (切换显示器)"', '"name": "Custom Import (Switch Display)"')
        c = c.replace('"name": "自定义导入数据 (ALT+F4)"', '"name": "Custom Import (ALT+F4)"')
        c = c.replace('data中的数值为上方链接获取的16进制code，例如ctrl为0xA2,alt为0xA4，shift为0xA0，f12为0x7B，win为0x5B', 'Data values are hex virtual keycodes from the link above (e.g. Ctrl=0xA2, Alt=0xA4, Shift=0xA0, F12=0x7B, Win=0x5B)')
        with open(p_special, 'w', encoding='utf-8', newline='') as f:
            f.write(c)
        print("Updated specialbuttons.json")

if __name__ == '__main__':
    translate_configs()
