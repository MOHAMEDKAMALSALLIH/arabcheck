# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Extended audit rules (taa marbuta, tanween)
- Dataset loading (CSV, JSONL)
- Duplicate detection
- Text quality statistics
- Publish on PyPI

## [0.1.0] - 2026-09-20

### Added
- Initial release
- Tashkeel (diacritics) removal — harakat + Quranic marks
- Tatweel (kashida) removal
- Character normalization (alif, yaa, hamza, taa marbuta)
- Text cleaning (whitespace normalization)
- Grammar audit (hamzat qat/wasl detection)
- CLI with argparse
- JSON output support for automation
- File and stdin input support
- Correct exit codes for CI/CD (0, 1, 2)
- Test suite with 22 tests (core + CLI)
- CI workflow (GitHub Actions, Python 3.8-3.12)
- Full documentation (README, CONTRIBUTING)

[Unreleased]: https://github.com/MOHAMEDKAMALSALLIH/arabcheck/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/MOHAMEDKAMALSALLIH/arabcheck/releases/tag/v0.1.0