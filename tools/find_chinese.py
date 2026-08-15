import os
import re
import sys
import argparse

# Ensure UTF-8 output encoding for standard output on Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

# Regex pattern for Chinese characters (CJK Unified Ideographs & CJK Extension A)
CHINESE_PATTERN = re.compile(r'[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff]')

# Directories to ignore by default
IGNORE_DIRS = {
    '.git', '.gradle', 'build', '.idea', 'captures', '.externalNativeBuild',
    'bin', 'obj', 'node_modules', '.vs', '.gemini', 'out'
}

# File extensions to ignore by default
IGNORE_EXTS = {
    '.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp', '.ico',
    '.jar', '.aar', '.so', '.apk', '.zip', '.tar', '.gz', '.7z',
    '.class', '.dex', '.pyc', '.pyo', '.keystore', '.jks',
    '.ttf', '.otf', '.woff', '.woff2', '.eot', '.pdf', '.db', '.dat'
}

def is_chinese(text):
    return CHINESE_PATTERN.search(text) is not None

def find_chinese_in_file(filepath):
    matches = []
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            for line_idx, line in enumerate(f, 1):
                if is_chinese(line):
                    chinese_chars = CHINESE_PATTERN.findall(line)
                    matches.append((line_idx, line.strip(), "".join(chinese_chars)))
    except Exception:
        pass
    return matches

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    default_root = os.path.dirname(script_dir)  # Project root directory

    parser = argparse.ArgumentParser(description="Scan project files to detect Chinese characters.")
    parser.add_argument("--root", type=str, default=default_root, help="Root directory to scan (defaults to project root)")
    parser.add_argument("--exclude-locales", action="store_true", help="Exclude standard Chinese locale resource directories (values-zh*)")
    args = parser.parse_args()

    root_dir = os.path.abspath(args.root)
    output_file = os.path.join(script_dir, "chinese_scan_report.txt")
    
    print(f"Scanning directory: {root_dir}")
    if args.exclude_locales:
        print("Excluding standard locale resource directories (values-zh*)\n")

    results = {}
    total_lines = 0

    for current_dir, dirs, files in os.walk(root_dir):
        # Prune ignored directories
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]

        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in IGNORE_EXTS:
                continue

            filepath = os.path.join(current_dir, file)
            rel_path = os.path.relpath(filepath, root_dir)

            # Skip scanner files and report files
            if file in ('find_chinese.py', 'chinese_scan_report.txt', 'find_leftover_chinese.py'):
                continue

            if args.exclude_locales and ('values-zh' in rel_path or 'values-ja' in rel_path):
                continue

            matches = find_chinese_in_file(filepath)
            if matches:
                results[rel_path] = matches
                total_lines += len(matches)

    # Write report to file
    with open(output_file, 'w', encoding='utf-8') as out:
        out.write(f"Found {total_lines} lines containing Chinese characters in {len(results)} files:\n\n")
        out.write("=" * 80 + "\n")

        for rel_path, matches in sorted(results.items()):
            out.write(f"\n[File]: {rel_path} ({len(matches)} lines)\n")
            for line_num, line_str, chars in matches:
                out.write(f"  Line {line_num:4d}: {line_str}\n")

        out.write("\n" + "=" * 80 + "\n")
        out.write(f"Total matching files: {len(results)}\n")
        out.write(f"Total matching lines: {total_lines}\n")

    print(f"Scan complete. Report saved to: {output_file}")
    print(f"Found {total_lines} lines containing Chinese characters in {len(results)} files.")

if __name__ == '__main__':
    main()
