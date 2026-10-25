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
- **Tatweel (Kashida)** — decorative stretching characters
- **Quranic marks** and extra whitespace

ArabCheck makes cleaning and auditing this data a one-liner.

---

## Features

- 🕌 **Tashkeel removal** — Harakat + Quranic marks
- 🔤 **Character normalization** — Alif, Yaa, Hamza, Taa Marbuta
- 〰️ **Tatweel removal** — Kashida stretching
- 🧹 **Text cleaning** — Whitespace normalization
- 🔍 **Grammar audit** — Hamzat qat/wasl detection
- 📂 **File + stdin support**
- 🤖 **JSON output** for CI/CD
- 🧩 **Extensible**

---

## Install

**From PyPI (recommended):**

    pip install arabcheck

**From source:**

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

**⚠️ Warning**: Normalization loses linguistic information. Use it for search, indexing, or NLP pipelines only.

### 3. Audit text (Legacy)

    arabcheck "الإستخدام" --audit
    # ⚠️  احتمال خطأ إملائي: 'الإستخدام'؛ الصيغة المقترحة للمراجعة هي 'الاستخدام'. تحذير للمراجعة البشرية، وليس تصحيحاً آلياً مؤكداً.

### 4. JSON output

    arabcheck "النَّصُّ" --clean --json

Returns:

    {
      "input": "النَّصُّ",
      "result": "النص",
      "issues": [],
      "meta": {
        "cleaned": true,
        "normalized": false,
        "audited": false,
        "version": "0.2.0"
      }
    }

### 5. Scan text using specific rules

    arabcheck scan "الإستخدام" --rules hamzat_qat

Returns:

    الإستخدام
     ⚠️  احتمال خطأ إملائي: 'الإستخدام'؛ الصيغة المقترحة للمراجعة هي 'الاستخدام'. تحذير للمراجعة البشرية، وليس تصحيحاً آلياً مؤكداً.

### 6. Scan text with JSON output

    arabcheck scan "الإستخدام" --rules hamzat_qat --json

Returns:

    {
      "input": "الإستخدام",
      "issues": [
        {
          "rule": "hamzat_qat",
          "message": "احتمال خطأ إملائي: 'الإستخدام'؛ الصيغة المقترحة للمراجعة هي 'الاستخدام'. تحذير للمراجعة البشرية، وليس تصحيحاً آلياً مؤكداً.",
          "word": "الإستخدام",
          "intended": "الاستخدام",
          "position": 0,
          "severity": "warning"
        }
      ],
      "meta": {
        "rules": [
          "hamzat_qat"
        ],
        "version": "0.2.0"
      }
    }

### 7. Read from file

    arabcheck --file dataset.txt --clean

### 8. From stdin

    cat article.txt | arabcheck --clean

---

## CLI Reference

### Main Command

    usage: arabcheck [-h] [-f FILE] [-c] [-n] [-a] [-j] [-q] [-V] [text]

| Option | Description |
|--------|-------------|
| `-h, --help` | Show help |
| `-f, --file FILE` | Read from file |
| `-c, --clean` | Remove tashkeel, tatweel, extra spaces |
| `-n, --normalize` | Normalize letters |
| `-a, --audit` | Audit spelling issues (Legacy) |
| `-j, --json` | JSON output |
| `-q, --quiet` | Suppress output |
| `-V, --version` | Show version |

### Scan Command

    usage: arabcheck scan [-h] [-f FILE] [--rules RULES] [-j] [-q] [text]

| Option | Description |
|--------|-------------|
| `-h, --help` | Show help |
| `-f, --file FILE` | Read from file |
| `--rules RULES` | Comma-separated list of rules to run (e.g. `hamzat_qat`) |
| `-j, --json` | JSON output |
| `-q, --quiet` | Suppress output |

### Exit Codes

| Code | Meaning |
|:----:|:--------|
| `0` | Success, no issues |
| `1` | Issues found (with `--audit` or `scan`) |
| `2` | Input error or invalid arguments |

---

## Use as a Library

    from arabcheck import ArabCheck

    checker = ArabCheck()

    # Clean
    text = checker.clean_text("النَّصُّ العَرَبِيُّ ـــ")
    print(text)  # → النص العربي

    # Normalize
    print(checker.normalize("أحمد إبراهيم"))

    # Audit
    issues = checker.audit("الأمر بالأمر")
    for issue in issues:
        print(issue["message"])

---

## Examples

Full working examples are in the [`examples/`](examples/) folder:

- **[`clean_dataset.py`](examples/clean_dataset.py)** — Clean an entire Arabic text dataset
- **[`preprocess_for_ai.py`](examples/preprocess_for_ai.py)** — Preprocessing pipeline for AI models

Run them:

    python examples/clean_dataset.py
    python examples/preprocess_for_ai.py

---

## Testing

    pip install -e ".[dev]"
    pytest

Tests covering core and CLI — all passing ✅

---

## Roadmap

- [x] Tashkeel & Tatweel removal
- [x] Character normalization
- [x] File + stdin support
- [x] JSON output
- [x] Exit codes for CI/CD
- [x] Grammar audit
- [ ] Extended audit rules
- [ ] Dataset loading (CSV, JSONL)
- [ ] Duplicate detection
- [ ] Text quality statistics

---

## Contributing

Contributions, issues, and feature requests are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md).

---

## Releases

See [Releases](https://github.com/MOHAMEDKAMALSALLIH/arabcheck/releases) for version history.

---

## License

MIT — see [LICENSE](LICENSE) for details.

---

<p align="center">
  Made with ❤️ for the Arabic NLP community
</p>
