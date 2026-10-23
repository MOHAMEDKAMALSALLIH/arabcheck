"""Tests for the new scan CLI subcommand."""
import json
import subprocess
import sys


def run_cli(*args):
    return subprocess.run(
        [sys.executable, "-m", "arabcheck", *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )


def test_scan_help_is_available():
    result = run_cli("scan", "--help")
    assert result.returncode == 0
    assert "--rules" in result.stdout
    assert "--json" in result.stdout


def test_scan_text_with_json_reports_hamza_issue():
    result = run_cli("scan", "الإستخدام الكتاب", "--json")
    assert result.returncode == 1

    data = json.loads(result.stdout)
    assert len(data["issues"]) == 1
    assert data["issues"][0]["rule"] == "hamzat_qat"
    assert data["issues"][0]["word"] == "الإستخدام"


def test_scan_clean_text_returns_zero():
    result = run_cli("scan", "مرحبا بكم", "--json")
    assert result.returncode == 0

    data = json.loads(result.stdout)
    assert data["issues"] == []


def test_scan_can_select_hamza_rule():
    result = run_cli(
        "scan", "الإستخدام الكتاب",
        "--rules", "hamzat_qat", "--json",
    )
    assert result.returncode == 1

    data = json.loads(result.stdout)
    assert len(data["issues"]) == 1
