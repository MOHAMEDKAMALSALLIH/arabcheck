"""Tests for the ArabCheck CLI."""
import json
import subprocess
import sys
from pathlib import Path

import pytest


def run_cli(*args, input_text=None):
    """Helper to run the CLI and capture output."""
    return subprocess.run(
        [sys.executable, "-m", "arabcheck", *args],
        capture_output=True,
        text=True,
        input=input_text,
        encoding="utf-8",
    )


# ---------- Version ----------
def test_cli_version():
    result = run_cli("--version")
    assert result.returncode == 0
    assert "arabcheck" in result.stdout.lower()


# ---------- Clean ----------
def test_cli_clean():
    result = run_cli("النَّصُّ العَرَبِيُّ", "--clean")
    assert result.returncode == 0
    assert "النص العربي" in result.stdout


def test_cli_clean_with_tatweel():
    result = run_cli("مــرحبــا", "--clean")
    assert result.returncode == 0
    assert "مرحبا" in result.stdout


# ---------- Normalize ----------
def test_cli_normalize():
    result = run_cli("أحمد إبراهيم", "--normalize")
    assert result.returncode == 0
    assert "احمد ابراهيم" in result.stdout


# ---------- Audit & exit codes ----------
def test_cli_audit_clean_returns_zero():
    result = run_cli("السلام عليكم", "--audit")
    assert result.returncode == 0


def test_cli_audit_issues_returns_one():
    result = run_cli("الأمر", "--audit")
    assert result.returncode == 1


# ---------- JSON ----------
def test_cli_json_output():
    result = run_cli("النَّصُّ", "--clean", "--json")
    assert result.returncode == 0
    data = json.loads(result.stdout)
    assert data["input"] == "النَّصُّ"
    assert data["result"] == "النص"
    assert "issues" in data
    assert "meta" in data
    assert data["meta"]["cleaned"] is True


def test_cli_json_with_audit():
    result = run_cli("الأمر", "--audit", "--json")
    data = json.loads(result.stdout)
    assert len(data["issues"]) == 1
    assert data["issues"][0]["type"] == "hamzat_qat"
    assert result.returncode == 1


# ---------- Quiet ----------
def test_cli_quiet():
    result = run_cli("النَّصُّ", "--clean", "--quiet")
    assert result.returncode == 0
    assert "النص" not in result.stdout


# ---------- File input ----------
def test_cli_file_input(tmp_path):
    f = tmp_path / "input.txt"
    f.write_text("النَّصُّ العَرَبِيُّ", encoding="utf-8")
    result = run_cli("--file", str(f), "--clean")
    assert result.returncode == 0
    assert "النص العربي" in result.stdout


def test_cli_missing_file_returns_two():
    result = run_cli("--file", "/nonexistent/file.txt", "--clean")
    assert result.returncode == 2


# ---------- stdin ----------
def test_cli_stdin():
    result = run_cli("--clean", input_text="النَّصُّ")
    assert result.returncode == 0
    assert "النص" in result.stdout