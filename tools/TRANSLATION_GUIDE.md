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
