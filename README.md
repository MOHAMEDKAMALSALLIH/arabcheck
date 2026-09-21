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

```bash
pip install arabcheck
