import os
import re
import sys

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

CHINESE_PATTERN = re.compile(r'[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff]')

def inspect_xml_files():
    xml_matches = {}
    for root, dirs, files in os.walk('app/src/main/res'):
        if 'values-zh' in root or 'values-ja' in root:
            continue
        for file in files:
            if file.endswith('.xml'):
                filepath = os.path.normpath(os.path.join(root, file))
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()
                matches = []
                for idx, line in enumerate(lines, 1):
                    line_stripped = line.strip()
                    # Skip pure comments like <!-- 填充的颜色 -->
                    if line_stripped.startswith('<!--') and line_stripped.endswith('-->'):
                        continue
                    if CHINESE_PATTERN.search(line):
                        matches.append((idx, line_stripped))
                if matches:
                    xml_matches[filepath] = matches

    print(f"Total XML files with non-comment Chinese: {len(xml_matches)}")
    for fp, matches in sorted(xml_matches.items()):
        print(f"\n=============================")
        print(f"File: {fp} ({len(matches)} lines)")
        print(f"=============================")
        for idx, line in matches:
            print(f"  Line {idx:4d}: {line}")

if __name__ == '__main__':
    inspect_xml_files()
