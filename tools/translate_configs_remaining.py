import os
import sys

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

def fix_configs():
    # config_gamepad.txt
    p_gp = 'app/src/main/assets/config/config_gamepad.txt'
    if os.path.exists(p_gp):
        with open(p_gp, 'r', encoding='utf-8') as f:
            c = f.read()
        c = c.replace('"desc":"视图键"', '"desc":"View / Back"')
        c = c.replace('"name":"十字键"', '"name":"D-Pad"')
        c = c.replace('"desc":"常规模式"', '"desc":"Normal Mode"')
        c = c.replace('"name":"右摇杆"', '"name":"Right Stick"')
        c = c.replace('"desc":"XBOX键"', '"desc":"Xbox Button"')
        c = c.replace('"desc":"左扳机"', '"desc":"Left Trigger"')
        c = c.replace('"name":"左摇杆"', '"name":"Left Stick"')
        c = c.replace('"desc":"左肩键"', '"desc":"Left Bumper"')
        c = c.replace('"desc":"菜单键"', '"desc":"Menu / Start"')
        c = c.replace('"desc":"右肩键"', '"desc":"Right Bumper"')
        c = c.replace('"desc":"右扳机"', '"desc":"Right Trigger"')
        with open(p_gp, 'w', encoding='utf-8', newline='') as f:
            f.write(c)
        print("Updated config_gamepad.txt")

    # keyboard.json & keyboard_1.json
    for kb_file in ['keyboard.json', 'keyboard_1.json']:
        p_kb = os.path.join('app/src/main/assets/config', kb_file)
        if os.path.exists(p_kb):
            with open(p_kb, 'r', encoding='utf-8') as f:
                c = f.read()
            c = c.replace('Standard on-screen trackpad widget没有点击事件', 'Trackpad widget without click events')
            with open(p_kb, 'w', encoding='utf-8', newline='') as f:
                f.write(c)
            print(f"Updated {kb_file}")

if __name__ == '__main__':
    fix_configs()
