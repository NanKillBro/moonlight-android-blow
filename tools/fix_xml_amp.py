import os

def fix_ampersands():
    folders = ['app/src/main/res/layout', 'app/src/main/res/layout-land']
    for folder in folders:
        for file in os.listdir(folder):
            if file.endswith('.xml'):
                filepath = os.path.join(folder, file)
                with open(filepath, 'r', encoding='utf-8') as f:
                    c = f.read()
                orig = c
                # Fix unescaped ampersands in XML attributes
                c = c.replace('Quick Actions & Functions', 'Quick Actions &amp; Functions')
                c = c.replace('Mouse & Touch', 'Mouse &amp; Touch')
                c = c.replace('Virtual Gamepad & Keys', 'Virtual Gamepad &amp; Keys')
                c = c.replace('Save & Apply', 'Save &amp; Apply')
                c = c.replace('Mouse & Wheel Buttons', 'Mouse &amp; Wheel Buttons')
                c = c.replace('Virtual Gamepad & Virtual Controls', 'Virtual Gamepad &amp; Virtual Controls')
                c = c.replace('Control Color Theme (Gamepad & Buttons)', 'Control Color Theme (Gamepad &amp; Buttons)')
                c = c.replace('Control Opacity (Gamepad & Buttons)', 'Control Opacity (Gamepad &amp; Buttons)')
                if c != orig:
                    with open(filepath, 'w', encoding='utf-8', newline='') as f:
                        f.write(c)
                    print(f"Fixed ampersands in {file}")

if __name__ == '__main__':
    fix_ampersands()
