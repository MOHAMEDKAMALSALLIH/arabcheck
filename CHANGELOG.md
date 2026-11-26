# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Modular `BaseRule` interface and scanner engine.
- `arabcheck scan` command with selectable rules and JSON output.
- Conservative `hamzat_qat` rule that reports suspicious forms for human review.
- `invisible` rule for selected invisible Unicode and control characters.
- Issue location details, including word, line, column, and character offset, where applicable.
- Tests for invisible-character coverage, position reporting, edge cases, and performance behavior.

### Changed
- Integrated the modular rule system with the existing CLI while retaining the legacy commands.
- Optimized invisible-character position lookup using binary search without changing the expected issue output.

## [0.1.1] - 2026-09-21

### Fixed
- Updated README formatting, badges, and examples.

### Added
- `examples/` folder with two working scripts.
- Arabic README (`README.ar.md`).

## [0.1.0] - 2026-09-20

### Added
- Initial release.
- Tashkeel (diacritics) removal — harakat and Quranic marks.
- Tatweel (kashida) removal.
- Character normalization (alif, yaa, hamza, taa marbuta).
- Text cleaning (whitespace normalization).
- Legacy spelling audit for common hamzat qat/wasl patterns.
- CLI with argparse.
- JSON output support for automation.
- File and stdin input support.
- Exit codes for CI/CD (0, 1, 2).
- Test suite and GitHub Actions CI for Python 3.8–3.12.

### Planned
- Visual homoglyph/confusable detection.
- Mojibake detection.
- Whitespace and punctuation quality rules.
- Extended audits for taa marbuta and tanween.
- CSV/JSONL dataset scanning, duplicate detection, and text-quality statistics.

[Unreleased]: https://github.com/MOHAMEDKAMALSALLIH/arabcheck/compare/v0.1.1...HEAD
[0.1.1]: https://github.com/MOHAMEDKAMALSALLIH/arabcheck/releases/tag/v0.1.1
[0.1.0]: https://github.com/MOHAMEDKAMALSALLIH/arabcheck/releases/tag/v0.1.0
