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
```

To test `invisible`, the input must contain an invisible character. This Bash example inserts U+200B ZERO WIDTH SPACE:

```bash
# Bash
arabcheck scan $'نص\u200bمخفي' --rules invisible
```

The `hamzat_qat` rule flags a defined set of suspicious forms as warnings for human review. A warning is not a confirmed correction; for example, the rule suggests a spelling for `الإستخدام`.

The `invisible` rule reports selected invisible and control characters, including U+200B ZERO WIDTH SPACE and U+FEFF BOM. It does not modify or remove them. A reported issue causes the scanner to return exit code `1`.

A UTF-8 file saved with a BOM begins with U+FEFF. The `invisible` rule reports that leading BOM, and `arabcheck scan --file file.txt` returns exit code `1` when it is the only reported issue.

### 4. JSON output

Run:

```bash
arabcheck scan "الإستخدام" --rules hamzat_qat --json
```

The JSON document contains `input`, `issues`, and `meta`. The following is a compact illustration of the issue structure; exact values and messages come from the selected rule:

```json
{
  "input": "الإستخدام",
  "issues": [
    {
      "rule": "hamzat_qat",
      "type": "hamzat_qat",
      "severity": "warning",
      "word": "الإستخدام",
      "intended": "الاستخدام",
      "position": 1,
      "location": {"word": 1},
      "message": "..."
    }
  ],
  "meta": {
    "rules": ["hamzat_qat"],
    "version": "0.2.0"
  }
}
```

For `invisible`, each issue also includes the character code, Unicode name, and location details (`word`, `line`, `column`, and `offset`). The `position` and `location.word` values can be `null` when the character is not associated with a word.

### 5. Legacy audit and the scanner

The original `--audit` option remains available on the main command:

```bash
arabcheck "الإستخدام" --audit
```

It calls the legacy `ArabCheck.audit()` behavior. The newer `arabcheck scan` command uses the modular `Scanner` and registered rules (`hamzat_qat` and `invisible` by default). These are separate interfaces; use `scan` when you want to select modular rules with `--rules`.

### 6. Read from a file or stdin

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

Use the legacy `ArabCheck` helpers for cleaning, normalization, and the legacy audit:

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

Use the modular scanner through its module. The current constructor accepts rule objects (not rule-name strings):

```python
from arabcheck.scanner import Scanner
from arabcheck.rules.hamza import HamzatQatRule
from arabcheck.rules.invisible import InvisibleRule

scanner = Scanner(rules=[HamzatQatRule(), InvisibleRule()])
issues = scanner.scan("نص للإستخدام")
for issue in issues:
    print(issue["rule"], issue["message"])
```

## Examples

Working scripts are available in [`examples/`](examples/):

- [`clean_dataset.py`](examples/clean_dataset.py) — clean an Arabic text dataset.
- [`preprocess_for_ai.py`](examples/preprocess_for_ai.py) — prepare text for AI workflows.

Run them from the repository root:

```bash
python examples/clean_dataset.py
python examples/preprocess_for_ai.py
```

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
