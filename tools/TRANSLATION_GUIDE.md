# Moonlight Android Translation & Maintenance Guide

This guide documents the workflow, tools, and best practices for translating and maintaining the English localization of the **moonlight-android-blow** fork while preserving clean upstream compatibility with `Axixi2233/moonlight-android`.

---

## 1. Upstream Conflict Minimization Rules

When maintaining this fork against upstream commits:
1. **In-place String Replacement**: Never restructure Java code or layouts to add new `@string/...` identifiers when translating hardcoded strings. Replace the string literal in-place on the same line (e.g. `dialogFragment.setTitle("显示")` -> `dialogFragment.setTitle("Display")`). This allows git 3-way merge to resolve cleanly when upstream modifies surrounding code.
2. **XML Entity Escaping**: In XML layout/resource attributes, always escape special characters such as `&` as `&amp;` (e.g. `android:text="Quick Actions &amp; Functions"`).
3. **Leave `values-zh*` Untouched**: Do not delete the `values-zh-rCN` or `values-zh-rTW` folders. The default `res/values/` contains the English strings and acts as the fallback for all non-Chinese locales.
4. **Ignore Non-UI Comments**: Do not modify comments in `.glsl` shaders, drawable XML backgrounds, or build scripts to avoid hundreds of useless diff lines.

---

## 2. Key Tools in `tools/` Directory

| Script | Purpose | How to Run |
| :--- | :--- | :--- |
| `verify_translation.py` | Full verification suite: validates XML syntax, JSON syntax, and scans for any leftover UI Chinese characters. | `python tools/verify_translation.py` |
| `find_chinese.py` | Scans the codebase for CJK characters with optional locale exclusion. | `python tools/find_chinese.py --exclude-locales` |
| `apply_clean_translation.py` | Master automation script that cleanly re-applies all translation steps across values, preferences, layouts, Java files, and assets. | `python tools/apply_clean_translation.py` |
| `inspect_java_chinese.py` | Extracts all Java files containing Chinese characters in string literals (excluding comments). | `python tools/inspect_java_chinese.py` |
| `inspect_xml_chinese.py` | Extracts all XML files containing Chinese characters in attributes or text (excluding comments). | `python tools/inspect_xml_chinese.py` |

---

## 3. Translation Categories & Targets

### A. Default Resources (`app/src/main/res/values/`)
- `strings.xml`: In-game quick menu items, shortcuts, HUD labels, setup guides, and update notifications.
- `arrays.xml`: Rendering modes, 3D stereo modes, FSR upscaling options, preset names, mouse/touch modes, and screen gravity alignment.

### B. Preference Definitions (`app/src/main/res/xml/`)
- `preferences.xml`: Custom resolutions, Joy-Con mapping, battery reporting, floating button, virtual keyboard, external display mode, vibration redirection, gyro emulation, audio haptics, backup/restore, and stream logs.

### C. Layout XMLs (`app/src/main/res/layout/` and `app/src/main/res/layout-land/`)
- In-game quick menu dialogs (`dialog_game_menu*.xml`)
- Virtual gamepad & keyboard controllers (`layout_axixi_keyboard.xml`, `item_layout_axixi_keyboard*.xml`, `ax_gamepad_top_view.xml`, `axi_keyboard_top_*.xml`)
- Activity layouts (`activity_about.xml`, `activity_axitest.xml`, `activity_game.xml`, `activity_stream_logs.xml`)

### D. Java Classes (`app/src/main/java/com/limelight/`)
- `Game.java`: HUD statistics, connection states, external display notifications.
- `StreamSettings.java`: Backup/restore toasts and dialog confirmations.
- `KeyBoardController.java`: Edit mode prompts and position labels.
- `GameKeyboardUpdateFragment.java` & `GamePadAddFragment.java`: Button and key type names.
- `UpdateChecker.java`: Update dialogs and release notes parser.
- `StreamLogFilesActivity.java` & `StreamSessionLogger.java`: Session log headers and file management.

### E. Asset Presets (`app/src/main/assets/config/`)
- `keyboard.json`, `keyboard_1.json`, `keyboard_2.json`: On-screen stick, D-pad, and button layouts.
- `config_keyboard.txt`, `config_gamepad.txt`: Preset button assignments.
- `buttonSwitch.json`, `specialbuttons.json`: Shortcut codes and accessibility mappings.

---

## 4. GitHub Actions CI Build

- **Workflow File**: `.github/workflows/android.yml`
- **JDK Version**: Java 17 (Temurin distribution)
- **Submodules**: `submodules: recursive` (required for `moonlight-common-c`)
- **Gradle Command**: `./gradlew assembleDebug assembleRelease`
- **Artifacts Output**: `app/build/outputs/apk/**/*.apk`

## 5. Upstream Sync Workflow

1. `git fetch upstream`
2. `git merge upstream/master` (never push).
3. On conflicts in `app/`, prefer upstream code over the translated side, then re-apply translations instead of hand-resolving every line:
   ```bash
   git rm -rf -q app && git checkout upstream/master -- app
   python tools/apply_clean_translation.py
   ```
4. Keep fork-only code changes such as the `RazerUtils` robustness fix when resetting `app/`.
5. Run `python tools/verify_translation.py` and translate any new leftovers with AI. Store the new exact line mappings in a `tools/translate_upstream_<tag>.py` script and call it from `apply_clean_translation.py`, so the next sync is automatic.
6. All translation scripts must open files with `newline=''` and replace whole lines, preserving the original mixed CRLF/LF line endings from upstream.

## 6. Vietnamese Localization (`values-vi`)

- Default `values/` holds English; `values-vi/` mirrors every translatable default resource.
- Keep `values-vi/strings.xml` in sync with `values/strings.xml` (493 entries as of upstream tag 261107), plus `values-vi/arrays.xml`, `strings_settings_panel.xml`, `strings_stylus.xml`, and `strings_touchpad_rotation.xml`.
- Preserve format specifiers, escapes, XML entities, and the CRLF line endings used by `values-vi/strings.xml`.
- Hardcoded Java/layout strings are translated to English in place only. They are not localized per-locale, to avoid restructuring code and creating upstream conflicts.
- `values-zh-rCN`, `values-zh-rTW`, and `values-ja` are intentionally left as upstream.

## Custom instruction (original promt)
help me translate this project to english
just ignore the chinese, we don't need it so you can delete it if you want.
the problem with this project some line is hardcoded chinsese and not in locale file.
i have some chinese tools that you may can use in tools folder, it also contain some instruction that you can read
try your best to not make to much edit, because i don't want it to conflict with future upstream commit
use your knowledge to translate, AI translate is still far better than any legacy translator like google translator 