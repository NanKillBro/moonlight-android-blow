import sys
import re

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

with open('tools/java_chinese_literals.txt', 'r', encoding='utf-8') as f:
    text = f.read()

sections = text.split('=============================\nFile: ')
with open('tools/ui_java_strings_dump.txt', 'w', encoding='utf-8') as out:
    for s in sections[1:]:
        lines = s.split('\n')
        fname = lines[0].split(' (')[0].strip()
        if fname.endswith('CreditsActivity.java'):
            continue
        out.write(f"\n### {fname}\n")
        for l in lines[2:]:
            if l.strip().startswith('Line'):
                out.write(f"  {l.strip()}\n")

print("Dumped UI Java strings successfully")
