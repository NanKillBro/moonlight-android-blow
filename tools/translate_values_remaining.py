import sys
import os

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

def translate_strings_xml():
    filepath = 'app/src/main/res/values/strings.xml'
    with open(filepath, 'r', encoding='utf-8', newline='') as f:
        content = f.read()

    # Exact replacements for strings.xml
    replacements = [
        ('<string name="keyboard_service_label">月光·阿西西物理键盘</string>', '<string name="keyboard_service_label">Moonlight Physical Keyboard Service</string>'),
        (
'''    <string name="accessibility_description_text">此功能仅用于外接实体键盘时，某些系统存在特定的键盘快捷键，此情况会影响串流过程中，无法将相关按键指令传输给目标PC。
        \\n\\n月光·阿西西不会观察您输入的文本，也不会收集您的密码、信用卡号或任何其他信息。
        \\n\\n请关注：B站-阿西西的日常</string>''',
'''    <string name="accessibility_description_text">This service is only used when connecting an external physical keyboard to intercept system shortcuts that might otherwise prevent key commands from reaching the host PC.
        \\n\\nMoonlight does not monitor your typed text, passwords, credit card numbers, or any personal data.</string>'''
        ),
        ('<string name="game_menu_toggle_keyboard">弹出软键盘</string>', '<string name="game_menu_toggle_keyboard">On-Screen Keyboard</string>'),
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
            print(f"Warning: pattern not found in strings.xml:\n{old[:50]}")

    with open(filepath, 'w', encoding='utf-8', newline='') as f:
        f.write(content)
    print("Updated strings.xml additional strings")

if __name__ == '__main__':
    translate_strings_xml()
