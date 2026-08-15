import os
import re
import sys

# Ensure UTF-8 output encoding for standard output on Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

CHINESE_PATTERN = re.compile(r'[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff]')
STRING_LITERAL_PATTERN = re.compile(r'"([^"\\]|\\.)*"')

def main():
    java_string_matches = []
    java_comment_only_matches = []

    for root, dirs, files in os.walk('app/src/main/java'):
        for file in files:
            if file.endswith('.java'):
                filepath = os.path.normpath(os.path.join(root, file))
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()
                for idx, line in enumerate(lines, 1):
                    if CHINESE_PATTERN.search(line):
                        has_chinese_string = False
                        for m in STRING_LITERAL_PATTERN.finditer(line):
                            if CHINESE_PATTERN.search(m.group(0)):
                                has_chinese_string = True
                                java_string_matches.append((filepath, idx, line.strip(), m.group(0)))
                        if not has_chinese_string:
                            java_comment_only_matches.append((filepath, idx, line.strip()))

    print(f'Total Java files with Chinese in string literals: {len(set(m[0] for m in java_string_matches))}')
    print(f'Total occurrences of Chinese in string literals: {len(java_string_matches)}')
    print(f'Total occurrences of Chinese in comments only: {len(java_comment_only_matches)}')

    print('\n--- Files with string literals ---')
    for f in sorted(list(set(m[0] for m in java_string_matches))):
        count = sum(1 for m in java_string_matches if m[0] == f)
        print(f'{f}: {count} string literals')

    print('\n--- Details of string literals ---')
    for f, idx, line, lit in java_string_matches:
        print(f'{f}:{idx}: {lit}')

if __name__ == '__main__':
    main()
