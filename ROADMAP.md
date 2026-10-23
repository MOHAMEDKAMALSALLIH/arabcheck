# ArabCheck Roadmap

## Original Seven Phases

### Phase 1 — Foundation (Completed)
Project structure, Arabic text cleaning and normalization, CLI, file/stdin input, JSON output, exit codes, tests, documentation, and CI.

### Phase 2 — Rules and Scanner (Partially Implemented)
Modular "BaseRule" interface, rule implementation, Scanner engine, rule registration, rule selection and validation, integration with the existing CLI, and backward compatibility.

Each issue result must include:
- Issue type
- Issue location
- Severity

*(Status: Working foundation exists. Verify all requirements before marking fully complete. Current issue results include severity and rule type, but exact position offsets may need verification/completion.)*

### Phase 3 — Arabic Text Quality Rules (Planned)
Rules for invisible Unicode characters, visual homoglyphs/confusables, mojibake, hamza spelling issues, and whitespace/punctuation quality.

**Important principle:** Rules must flag suspicious cases for human review. They must not present uncertain or suspicious cases as confirmed errors. Document uncertainty and avoid claiming linguistic correctness without sufficient evidence.

### Phase 4 — Unified Scan CLI (Planned)
Complete "arabcheck scan", rule selection, input handling, structured JSON output, error handling, and CI integration.

### Phase 5 — Safe Optional Fixes (Planned)
Optional "--fix" support, transparent proposed changes or diffs, and safeguards against silently damaging meaning or text.

### Phase 6 — Dataset Scanning (Planned)
CSV and JSONL input, issue locations, duplicate detection, and text-quality statistics.

Also include:
- Statistics identifying the most frequent issue types.
- A strategy for processing large files without loading the entire dataset into memory.

### Phase 7 — Tests, Documentation, and Release (Planned)
Comprehensive regression tests, Arabic and English documentation, release preparation, packaging verification, and contributor support.

Also include:
- Compatibility verification across supported Python versions 3.8–3.12.
- Updating "README.md", "README.ar.md", and "CHANGELOG.md" when features, behavior, tests, or releases warrant it.

## Other Planned Items
- Extended audit rules (taa marbuta, tanween)
- Publish on PyPI

## Status Policy
- Phase 1 is recorded as completed.
- Phase 2 has a working foundation; verify all requirements before marking it fully complete.
- Phases 3–7 remain in the roadmap, even where partial implementations already exist.
- Do not claim a feature is complete without repository evidence.
- Distinguish implemented, partially implemented, and planned work where evidence supports those labels.
- Performance optimization and benchmarking, Arabic-number auditing, and PII auditing remain separate future enhancements, not replacements for or additions to the original seven phases.
