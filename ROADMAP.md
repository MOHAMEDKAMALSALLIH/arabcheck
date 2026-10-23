# ArabCheck Development Roadmap

This document outlines the seven-phase development roadmap for ArabCheck. The original phases are preserved to guide the project's evolution.

## Phase 1 — Foundation (Completed)
- Project structure
- Arabic text cleaning and normalization
- CLI
- file/stdin input
- JSON output
- exit codes
- tests
- documentation
- CI

## Phase 2 — Rules and Scanner (Working Foundation)
*Status: Working foundation complete. Verify remaining requirements before marking fully complete.*
- Modular BaseRule interface
- rule implementation
- Scanner engine
- rule registration
- rule selection and validation
- integration with the existing CLI
- backward compatibility

## Phase 3 — Arabic Text Quality Rules
*Status: Planned (Remains in roadmap)*
- Rules for invisible Unicode characters
- visual homoglyphs/confusables
- mojibake
- hamza spelling issues
- whitespace/punctuation quality

## Phase 4 — Unified Scan CLI
*Status: Planned (Remains in roadmap)*
- Complete "arabcheck scan"
- rule selection
- input handling
- structured JSON output
- error handling
- CI integration

## Phase 5 — Safe Optional Fixes
*Status: Planned (Remains in roadmap)*
- Optional "--fix" support
- transparent proposed changes or diffs
- safeguards against silently damaging meaning or text

## Phase 6 — Dataset Scanning
*Status: Planned (Remains in roadmap)*
- CSV and JSONL input
- issue locations
- duplicate detection
- text-quality statistics

## Phase 7 — Tests, Documentation, and Release
*Status: Planned (Remains in roadmap)*
- Comprehensive regression tests
- Arabic and English documentation
- release preparation
- packaging verification
- contributor support

---

### Future Enhancements
*Note: The following are separate future enhancements, not replacements for or additions to the original seven phases.*
- Performance optimization and benchmarking
- Arabic-number auditing
- PII auditing
