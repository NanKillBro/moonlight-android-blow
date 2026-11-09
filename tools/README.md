# Translation & Inspection Tools

This directory contains the automation and inspection toolchain used for translating and verifying English localization in the **moonlight-android-blow** fork.

For full architectural instructions and maintenance guidelines, see **[`TRANSLATION_GUIDE.md`](./TRANSLATION_GUIDE.md)**.

## Quick Reference

- **Verify everything**:
  ```bash
  python tools/verify_translation.py
  ```

- **Re-apply clean translation**:
  ```bash
  python tools/apply_clean_translation.py
  ```

- **Re-apply the 261107 upstream sync translations**:
  ```bash
  python tools/translate_upstream_261107.py
  ```

- **Scan for remaining Chinese characters**:
  ```bash
  python tools/find_chinese.py --exclude-locales
  ```
