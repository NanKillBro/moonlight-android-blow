import sys

def main():
    filepath = 'app/src/main/res/xml/preferences.xml'
    with open(filepath, 'r', encoding='utf-8') as f:
        c = f.read()
    c = c.replace('android:title="多点触控屏幕模式"', 'android:title="Multi-touch Screen Mode"')
    c = c.replace('开启此选项可以实现surface一样多点触控操作windows系统效果。', 'Enable multi-touch gestures on Windows like Surface.')
    c = c.replace('仅支持sunshine 0.21及以上版本', 'Requires Sunshine 0.21+')
    with open(filepath, 'w', encoding='utf-8', newline='') as f:
        f.write(c)
    print("Preferences completely clean")

if __name__ == '__main__':
    main()
