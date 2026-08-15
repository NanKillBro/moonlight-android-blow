import os

def fix_remaining():
    # AppView.java
    f_app_view = 'app/src/main/java/com/limelight/AppView.java'
    with open(f_app_view, 'r', encoding='utf-8') as f:
        c = f.read()
    c = c.replace('dialogFragment.setTitle("显示");', 'dialogFragment.setTitle("Display");')
    with open(f_app_view, 'w', encoding='utf-8', newline='') as f:
        f.write(c)

    # StreamSessionLogger.java
    f_logger = 'app/src/main/java/com/limelight/log/StreamSessionLogger.java'
    with open(f_logger, 'r', encoding='utf-8') as f:
        c = f.read()
    c = c.replace('return enabled ? "开" : "关";', 'return enabled ? "On" : "Off";')
    with open(f_logger, 'w', encoding='utf-8', newline='') as f:
        f.write(c)

    print("Fixed remaining Java strings")

if __name__ == '__main__':
    fix_remaining()
