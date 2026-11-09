import subprocess
import os
import sys

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

# Re-run all exact-match translations on the current tree.
# Safe after an upstream merge: every step only replaces known Chinese lines
# and keeps the original CRLF/LF line endings.
def preserve_exact_diff():
    # Run values translation
    subprocess.run(['python', 'tools/translate_values.py'], check=True)
    subprocess.run(['python', 'tools/translate_values_remaining.py'], check=True)

    # Run preferences translation
    subprocess.run(['python', 'tools/translate_preferences.py'], check=True)
    subprocess.run(['python', 'tools/translate_preferences_part2.py'], check=True)
    subprocess.run(['python', 'tools/clean_preferences_comment.py'], check=True)

    # Run layouts translation & ampersand fix
    subprocess.run(['python', 'tools/translate_layouts.py'], check=True)
    subprocess.run(['python', 'tools/fix_xml_amp.py'], check=True)

    # Run Java translation & remaining fix
    subprocess.run(['python', 'tools/translate_java.py'], check=True)
    subprocess.run(['python', 'tools/fix_remaining_java.py'], check=True)

    # Run config translations
    subprocess.run(['python', 'tools/translate_configs.py'], check=True)
    subprocess.run(['python', 'tools/translate_configs_remaining.py'], check=True)

    # Run translations added for the 261107 upstream sync
    subprocess.run(['python', 'tools/translate_upstream_261107.py'], check=True)

    print("Re-applied all translations cleanly.")

if __name__ == '__main__':
    preserve_exact_diff()
