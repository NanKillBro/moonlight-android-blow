import subprocess
import os
import sys

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

# Re-run translations with original line endings from upstream/master
def preserve_exact_diff():
    # 1. Reset working copy to upstream/master
    subprocess.run(['git', 'checkout', 'HEAD', '--', 'app'], check=True)
    
    # 2. Run values translation
    subprocess.run(['python', 'tools/translate_values.py'], check=True)
    subprocess.run(['python', 'tools/translate_values_remaining.py'], check=True)

    # 3. Run preferences translation
    subprocess.run(['python', 'tools/translate_preferences.py'], check=True)
    subprocess.run(['python', 'tools/translate_preferences_part2.py'], check=True)
    subprocess.run(['python', 'tools/clean_preferences_comment.py'], check=True)

    # 4. Run layouts translation & ampersand fix
    subprocess.run(['python', 'tools/translate_layouts.py'], check=True)
    subprocess.run(['python', 'tools/fix_xml_amp.py'], check=True)

    # 5. Run Java translation & remaining fix
    subprocess.run(['python', 'tools/translate_java.py'], check=True)
    subprocess.run(['python', 'tools/fix_remaining_java.py'], check=True)

    # 6. Run config translations
    subprocess.run(['python', 'tools/translate_configs.py'], check=True)
    subprocess.run(['python', 'tools/translate_configs_remaining.py'], check=True)

    print("Re-applied all translations cleanly.")

if __name__ == '__main__':
    preserve_exact_diff()
