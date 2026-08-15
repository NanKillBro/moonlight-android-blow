import os
import re
import sys
import xml.etree.ElementTree as ET
import json

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

CHINESE_PATTERN = re.compile(r'[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff]')

IGNORE_DIRS = {'.git', '.gradle', 'build', '.idea', 'bin', 'obj', 'out', 'tools'}
IGNORE_EXTS = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp', '.ico',
               '.jar', '.aar', '.so', '.apk', '.zip', '.tar', '.gz', '.7z',
               '.class', '.dex', '.pyc', '.pyo', '.keystore', '.jks',
               '.ttf', '.otf', '.woff', '.woff2', '.eot', '.pdf', '.db', '.dat', '.a'}

def verify_xml_syntax():
    errors = 0
    for root, dirs, files in os.walk('app/src/main/res'):
        for file in files:
            if file.endswith('.xml'):
                filepath = os.path.join(root, file)
                try:
                    ET.parse(filepath)
                except Exception as e:
                    print(f"[XML SYNTAX ERROR] {filepath}: {e}")
                    errors += 1
    if errors == 0:
        print("[PASSED] All XML files are well-formed and valid XML.")
    return errors

def verify_json_syntax():
    errors = 0
    for root, dirs, files in os.walk('app/src/main/assets'):
        for file in files:
            if file.endswith('.json'):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        json.load(f)
                except Exception as e:
                    print(f"[JSON SYNTAX ERROR] {filepath}: {e}")
                    errors += 1
    if errors == 0:
        print("[PASSED] All JSON files are well-formed and valid JSON.")
    return errors

def verify_no_leftover_ui_chinese():
    print("\n--- Scanning for leftover UI Chinese strings ---")
    STRING_LITERAL_PATTERN = re.compile(r'"([^"\\]|\\.)*"')
    leftover_count = 0

    for root, dirs, files in os.walk('app/src/main'):
        # skip zh and ja locales
        if 'values-zh' in root or 'values-ja' in root:
            continue
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in IGNORE_EXTS:
                continue
            if file == 'CreditsActivity.java': # skip patron usernames
                continue
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()

            for idx, line in enumerate(lines, 1):
                s = line.strip()
                if ext == '.xml':
                    # Ignore pure XML comments
                    if s.startswith('<!--') and s.endswith('-->'):
                        continue
                    # Ignore language names array items (e.g. 中文, 日本語 in language selector)
                    if file == 'arrays.xml' and ('中文' in s or '日本語' in s):
                        continue
                    if CHINESE_PATTERN.search(line):
                        print(f"[XML CHINESE] {filepath}:{idx}: {s}")
                        leftover_count += 1
                elif ext == '.java':
                    if s.startswith('//') or s.startswith('*') or s.startswith('/*'):
                        continue
                    for m in STRING_LITERAL_PATTERN.finditer(line):
                        if CHINESE_PATTERN.search(m.group(0)):
                            print(f"[JAVA CHINESE LITERAL] {filepath}:{idx}: {m.group(0)}")
                            leftover_count += 1
                elif ext in ('.json', '.txt') and ('assets\\config' in filepath or 'assets/config' in filepath):
                    if CHINESE_PATTERN.search(line):
                        print(f"[CONFIG CHINESE] {filepath}:{idx}: {s}")
                        leftover_count += 1

    if leftover_count == 0:
        print("[PASSED] 0 leftover user-facing Chinese strings detected across the entire codebase!")
    else:
        print(f"[FAILED] Found {leftover_count} leftover Chinese strings.")
    return leftover_count

def main():
    xml_err = verify_xml_syntax()
    json_err = verify_json_syntax()
    leftovers = verify_no_leftover_ui_chinese()

    if xml_err == 0 and json_err == 0 and leftovers == 0:
        print("\n==========================================")
        print("ALL VERIFICATIONS COMPLETED SUCCESSFULLY!")
        print("==========================================")

if __name__ == '__main__':
    main()
