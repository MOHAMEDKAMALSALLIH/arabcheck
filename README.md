# ArabCheck 🔍

> A lightweight, open-source toolkit and CLI for cleaning, normalizing, and auditing Arabic text for AI and NLP workflows.

[العربية →](README.ar.md)

[![PyPI - Version](https://img.shields.io/pypi/v/arabcheck)](https://pypi.org/project/arabcheck/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/arabcheck)](https://pypi.org/project/arabcheck/)
[![CI](https://img.shields.io/github/actions/workflow/status/MOHAMEDKAMALSALLIH/arabcheck/ci.yml?label=CI)](https://github.com/MOHAMEDKAMALSALLIH/arabcheck/actions)
[![GitHub Repo stars](https://img.shields.io/github/stars/MOHAMEDKAMALSALLIH/arabcheck)](https://github.com/MOHAMEDKAMALSALLIH/arabcheck/stargazers)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

---

## Why ArabCheck?

Arabic text data often contains noise that breaks NLP pipelines:

- **Unicode variants** — `أ` / `إ` / `آ` / `ا` / `ٱ` all represent alif
- **Diacritics (Tashkeel)** — fatha, damma, shadda, tanween
- **Tatweel (Kashida)** — decorative stretching characters `ـــــ`
- **Quranic marks** and extra whitespace

ArabCheck makes cleaning and auditing this data a one-liner — with full transparency and configurable operations.

---

## Features

- 🕌 **Tashkeel removal** — Harakat + Quranic marks
- 🔤 **Character normalization** — Alif, Yaa, Hamza, Taa Marbuta
- 〰️ **Tatweel removal** — Kashida stretching characters
- 🧹 **Text cleaning** — Whitespace normalization
- 🔍 **Grammar audit** — Detect common hamzat qat/wasl errors
- 📂 **File + stdin support**
- 🤖 **JSON output** for CI/CD pipelines
- 🧩 **Extensible** — easy to add new rules

---

## Install

### From PyPI (recommended)

    pip install arabcheck

### From source

    git clone https://github.com/MOHAMEDKAMALSALLIH/arabcheck.git
    cd arabcheck
    pip install -e .

**Requirements**: Python 3.8+ — no external dependencies.

---

## Quick Start

    arabcheck "النَّصُّ العَرَبِيُّ لِلتَّجْرِبَة" --clean

**Input:**

    النَّصُّ العَرَبِيُّ لِلتَّجْرِبَة

**Output:**

    النص العربي للتجربة

---

## Usage Examples

### 1. Clean text

    arabcheck "العَرَبِيَّةُ ـــ لُغَةٌ جَمِيلَةٌ" --clean
    # → العربية لغة جميلة

### 2. Normalize characters

    arabcheck "أحمد إبراهيم آمن" --normalize
    # → احمد ابراهيم امن

> ⚠️ **Warning**: Normalization loses linguistic information. Use it for search, indexing, or NLP pipelines only.

### 3. Audit text

    arabcheck "الأمر بالأمر" --audit
    # ⚠️  احتمال خطأ: 'الأمر' تبدأ بـ 'ال' + همزة قطع.

### 4. JSON output (for automation)

    arabcheck "النَّصُّ" --clean --json

```json
{
  "input": "النَّصُّ",
  "result": "النص",
  "issues": [],
  "meta": {
    "cleaned": true,
    "normalized": false,
    "audited": false,
    "version": "0.1.0"
  }
}
```

5. Read from file

6. From stdin

---

CLI Reference

Exit Codes

Code Meaning
0 Success, no issues
1 Issues found (with --audit)
2 Input error

---

Use as a Library

```python
from arabcheck import ArabCheck

checker = ArabCheck()

# Clean
text = checker.clean_text("النَّصُّ العَرَبِيُّ ـــ")
print(text)  # → النص العربي

# Normalize
print(checker.normalize("أحمد إبراهيم"))
# → احمد ابراهيم

# Audit
issues = checker.audit("الأمر بالأمر")
for issue in issues:
    print(issue["message"])
```

---

Examples

Full working examples are in the examples/ folder:

· clean_dataset.py — Clean an entire Arabic text dataset for NLP training
· preprocess_for_ai.py — Full preprocessing pipeline for AI models

Run them:

---

Testing

22 tests covering core and CLI — all passing ✅

---

Roadmap

☑ Tashkeel & Tatweel removal
☑ Character normalization
☑ File + stdin support
☑ JSON output
☑ Exit codes for CI/CD
☑ Grammar audit (hamzat qat/wasl)
☐ Extended audit rules
☐ Dataset loading (CSV, JSONL)
☐ Duplicate detection
☐ Text quality statistics

---

Contributing

Contributions, issues, and feature requests are welcome! See CONTRIBUTING.md for guidelines.

---

Releases

See Releases for version history.

---

License

MIT — see LICENSE for details.

---

<p align="center">
  Made with ❤️ for the Arabic NLP community
</p>
```

---

