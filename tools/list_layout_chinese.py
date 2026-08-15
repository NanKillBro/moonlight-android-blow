import os
import re
import sys

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

CHINESE = re.compile(r'[\u4e00-\u9fff]')

def list_layout_chinese():
    results = {}
    for folder in ['app/src/main/res/layout', 'app/src/main/res/layout-land']:
        for file in sorted(os.listdir(folder)):
            if file.endswith('.xml'):
                filepath = os.path.join(folder, file)
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()
                matches = []
                for idx, line in enumerate(lines, 1):
                    # check if line contains Chinese and not a commented out tag
                    if CHINESE.search(line):
                        matches.append((idx, line.rstrip()))
                if matches:
                    results[filepath] = matches

    print(f"Found {len(results)} layout files with Chinese:")
    for fp, matches in sorted(results.items()):
        print(f"\n=== {fp} ({len(matches)} lines) ===")
        for idx, line in matches:
            print(f"  {idx:4d}: {line.strip()}")

if __name__ == '__main__':
    list_layout_chinese()
