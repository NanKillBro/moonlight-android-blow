import os
import re
import sys

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

CHINESE_PATTERN = re.compile(r'[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff]')
STRING_LITERAL_PATTERN = re.compile(r'"([^"\\]|\\.)*"')

def inspect_all_java():
    files_with_chinese_strings = {}
    for root, dirs, files in os.walk('app/src/main/java'):
        for file in files:
            if file.endswith('.java'):
                filepath = os.path.normpath(os.path.join(root, file))
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()
                matches = []
                for idx, line in enumerate(lines, 1):
                    # Strip single-line comments before extracting string literals if comment is at end
                    # But simpler: find string literals, check if they contain Chinese
                    # Note: we need to ignore string literals inside comments
                    line_stripped = line.strip()
                    if line_stripped.startswith('//') or line_stripped.startswith('*') or line_stripped.startswith('/*'):
                        continue
                    # Check string literals
                    for m in STRING_LITERAL_PATTERN.finditer(line):
                        lit = m.group(0)
                        if CHINESE_PATTERN.search(lit):
                            matches.append((idx, lit, line_stripped))
                if matches:
                    files_with_chinese_strings[filepath] = matches

    print(f"Total Java files with Chinese string literals: {len(files_with_chinese_strings)}")
    for fp, matches in sorted(files_with_chinese_strings.items()):
        print(f"\n=============================")
        print(f"File: {fp} ({len(matches)} string literals)")
        print(f"=============================")
        for idx, lit, full_line in matches:
            print(f"  Line {idx:4d}: {lit}")

if __name__ == '__main__':
    inspect_all_java()
