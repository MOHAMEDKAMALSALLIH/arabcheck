# ArabCheck Roadmap

This roadmap preserves the original seven-phase scope. Status labels describe the current implementation; partial progress does not remove any planned work.

## Original Seven Phases

### Phase 1 — Foundation (Completed)
Project structure, Arabic text cleaning and normalization, CLI, file/stdin input, JSON output, exit codes, tests, documentation, and CI.

### Phase 2 — Rules and Scanner (Partially Implemented)
- Modular `BaseRule` interface.
- Scanner engine and rule registration.
- Rule selection and validation.
- Integration with the existing CLI and backward compatibility.
- Standard issue details: type, location, and severity.

The scanner foundation and selectable rules are implemented. Continue verifying the complete issue schema and behavior before marking this phase complete.

### Phase 3 — Arabic Text Quality Rules (In Progress)
The rule scope remains:
1. Invisible Unicode characters.
2. Visual homoglyphs/confusables.
3. Mojibake.
4. Hamza spelling issues.
5. Whitespace and punctuation quality.

Current implementation includes the `invisible` rule and the conservative `hamzat_qat` rule. The hamza rule reports suspicious forms for human review; its linguistic coverage and precision still require evaluation. The remaining rule categories are planned.

Additional planned audits remain in scope:
- Taa marbuta.
- Tanween.

**Important principle:** Rules must flag suspicious cases for human review. They must not present uncertain cases as confirmed errors or silently alter source text.

### Phase 4 — Unified Scan CLI (Partially Implemented)
- `arabcheck scan` command.
- Rule selection and validation.
- Text, file, and stdin input handling.
- Structured JSON output.
- Error handling and CI integration.

The command, rule selection, text/file/stdin handling, JSON output, and exit-code behavior have a working implementation. Verify the full requirements and edge cases before marking this phase complete.

### Phase 5 — Safe Optional Fixes (Planned)
- Optional `--fix` support.
- Transparent proposed changes or diffs.
- Safeguards against silently damaging meaning or source text.

### Phase 6 — Dataset Scanning (Planned)
- CSV and JSONL input.
- Issue locations.
- Duplicate detection.
- Text-quality statistics, including the most frequent issue types.
- A strategy for processing large files without loading the entire dataset into memory.

### Phase 7 — Tests, Documentation, and Release (In Progress)
- Comprehensive regression tests.
- Arabic and English documentation.
- Release preparation and packaging verification.
- Contributor support.
- Compatibility verification across supported Python versions 3.8–3.12.
- Updating `README.md`, `README.ar.md`, and `CHANGELOG.md` when features, behavior, tests, or releases warrant it.

## Other Planned Items
- Publish and maintain releases on PyPI.
- Continue extended audit rules (taa marbuta and tanween) as part of the broader quality-rule scope.

## Parallel Tracks

### Hardening and Reliability
Regression coverage, edge cases, output compatibility, performance checks, and supported-Python-version verification.

### Post-v1.0 Backlog
Potential future enhancements such as Arabic-number auditing and PII auditing. These do not replace or reduce the original seven phases.

### Business and Investment Strategy
A parallel track covering customer validation, revenue models, grants and sponsorships, incubators, partnerships, and possible startup, investment, or acquisition paths as the project matures. This track does not change the technical roadmap.

## Status Policy
- Phase 1 is recorded as completed.
- Phases 2 and 4 have working foundations but remain partial until their full requirements are verified.
- Phases 3 and 7 are in progress.
- Phases 5 and 6 remain planned.
- Do not claim a feature or phase is complete without repository evidence.
- Distinguish implemented, partially implemented, and planned work.
