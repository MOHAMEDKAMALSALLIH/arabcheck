# ArabCheck 🔍

> A lightweight, open-source Python toolkit and CLI for cleaning, normalizing, and auditing Arabic text for AI and NLP workflows.

[العربية →](README.ar.md)

[![PyPI - Version](https://img.shields.io/pypi/v/arabcheck)](https://pypi.org/project/arabcheck/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/arabcheck)](https://pypi.org/project/arabcheck/)
[![CI](https://img.shields.io/github/actions/workflow/status/MOHAMEDKAMALSALLIH/arabcheck/ci.yml?label=CI)](https://github.com/MOHAMEDKAMALSALLIH/arabcheck/actions)
[![GitHub Repo stars](https://img.shields.io/github/stars/MOHAMEDKAMALSALLIH/arabcheck)](https://github.com/MOHAMEDKAMALSALLIH/arabcheck/stargazers)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

---

## Why ArabCheck?

Arabic text data can contain noise that complicates NLP workflows:

- Unicode variants and inconsistent character forms.
- Diacritics (tashkeel), Quranic marks, and tatweel.
- Invisible or control characters.
- Extra whitespace and inconsistent formatting.

ArabCheck provides text-cleaning and normalization utilities alongside rule-based checks. Detection rules report findings for review; they do not automatically rewrite the input.

## Features

- **Tashkeel removal** — harakat and supported Quranic marks.
- **Tatweel removal** — decorative stretching characters.
- **Text cleaning** — whitespace normalization.
- **Character normalization** — configurable normalization of alif, yaa, hamza, and optionally taa marbuta.
- **Rule-based scanning** — current rules include `hamzat_qat` and `invisible`.
- **File and stdin input**.
- **JSON output** for automation.
- **Extensible rule interface**.

## Install

**From PyPI:**

```bash
pip install arabcheck
```

**From source:**

```bash
git clone https://github.com/MOHAMEDKAMALSALLIH/arabcheck.git
cd arabcheck
pip install -e .
```

Requirements: Python 3.8+; no runtime dependencies.

## Quick Start

```bash
arabcheck "النَّصُّ العَرَبِيُّ لِلتَّجْرِبَة" --clean
```

Output:

```text
النص العربي للتجربة
```

## Usage Examples

### 1. Clean text

```bash
arabcheck "العَرَبِيَّةُ ـــ لُغَةٌ جَمِيلَةٌ" --clean
# العربية لغة جميلة
```

### 2. Normalize characters

```bash
arabcheck "أحمد إبراهيم آمن" --normalize
# احمد ابراهيم امن
```

Normalization is lossy. Use it only when that loss is appropriate for your search, indexing, or NLP workflow.

### 3. Run the scanner

When `--rules` is omitted, `arabcheck scan` runs the registered default rules: `hamzat_qat` and `invisible`.

```bash
arabcheck scan "الإستخدام"
```

To select one rule:

```bash
arabcheck scan "الإستخدام" --rules hamzat_qat
arabcheck scan "النص" --rules invisible
```

The `hamzat_qat` rule flags defined suspicious forms as warnings for human review. A warning is not a confirmed correction.

The `invisible` rule reports selected invisible and control characters, including examples such as U+200B ZERO WIDTH SPACE and U+FEFF BOM. It does not modify or remove them. A reported issue causes the scanner to return exit code `1`.

### 4. JSON output

```bash
arabcheck scan "الإستخدام" --rules hamzat_qat --json
```

JSON output includes the original input, detected issues, and metadata such as selected rules and package version. Issue fields depend on the rule; the invisible-character rule includes character and location details.

### 5. Read from a file or stdin

```bash
arabcheck --file dataset.txt --clean
cat article.txt | arabcheck --clean
```

The scanner also accepts file and stdin input:

```bash
arabcheck scan --file dataset.txt
cat article.txt | arabcheck scan
```

## CLI Reference

### Main command

```text
arabcheck [-h] [-f FILE] [-c] [-n] [-a] [-j] [-q] [-V] [text]
```

| Option | Description |
|---|---|
| `-h, --help` | Show help |
| `-f, --file FILE` | Read from a UTF-8 file |
| `-c, --clean` | Remove tashkeel, tatweel, and extra whitespace |
| `-n, --normalize` | Normalize supported character variants |
| `-a, --audit` | Run the legacy spelling audit |
| `-j, --json` | JSON output |
| `-q, --quiet` | Suppress the processed text |
| `-V, --version` | Show package version |

### Scan command

```text
arabcheck scan [-h] [-f FILE] [--rules RULES] [-j] [-q] [text]
```

| Option | Description |
|---|---|
| `-h, --help` | Show help |
| `-f, --file FILE` | Read from a UTF-8 file |
| `--rules RULES` | Comma-separated rule names |
| `-j, --json` | JSON output |
| `-q, --quiet` | Suppress the input text |

### Exit codes

| Code | Meaning |
|:---:|---|
| `0` | No issues were reported |
| `1` | One or more issues were reported |
| `2` | Invalid arguments or input error |

## Use as a Python library

```python
from arabcheck import ArabCheck

checker = ArabCheck()

cleaned = checker.clean_text("النَّصُّ العَرَبِيُّ ـــ")
print(cleaned)  # النص العربي

normalized = checker.normalize("أحمد إبراهيم")
print(normalized)  # احمد ابراهيم

issues = checker.audit("الإستخدام")
for issue in issues:
    print(issue["message"])
```

## Examples

Working scripts are available in [`examples/`](examples/):

- [`clean_dataset.py`](examples/clean_dataset.py) — clean an Arabic text dataset.
- [`preprocess_for_ai.py`](examples/preprocess_for_ai.py) — prepare text for AI workflows.

## Testing

Install development dependencies and run the test suite:

```bash
pip install -e ".[dev]"
pytest
```

## Roadmap

ArabCheck is under active development. The original seven-phase scope includes additional Arabic text-quality rules, safe optional fixes, dataset scanning, duplicate detection, and text-quality statistics. See [`ROADMAP.md`](ROADMAP.md) for implementation status and the full plan.

## Contributing

Contributions, issues, and feature requests are welcome. See [`CONTRIBUTING.md`](CONTRIBUTING.md).

## Releases

See [GitHub Releases](https://github.com/MOHAMEDKAMALSALLIH/arabcheck/releases) and [PyPI](https://pypi.org/project/arabcheck/) for published versions.

## License

MIT — see [`LICENSE`](LICENSE).
