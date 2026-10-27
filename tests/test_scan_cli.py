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


def test_scan_json_reports_suspicious_hamza_and_location():
    result = run_cli("scan", "الأحمد الإستخدام الكتاب", "--json")
    assert result.returncode == 1
    data = json.loads(result.stdout)
    assert len(data["issues"]) == 1
    issue = data["issues"][0]
    assert issue["rule"] == "hamzat_qat"
    assert issue["word"] == "الإستخدام"
    assert issue["intended"] == "الاستخدام"
    assert issue["position"] == 2


def test_scan_clean_text_returns_zero():
    result = run_cli("scan", "الأحمد الأمر الإنسان", "--json")
    assert result.returncode == 0
    assert json.loads(result.stdout)["issues"] == []


def test_scan_can_select_hamza_rule():
    result = run_cli(
        "scan", "الإستخدام", "--rules", "hamzat_qat", "--json",
    )
    assert result.returncode == 1
    assert len(json.loads(result.stdout)["issues"]) == 1


def test_scan_unknown_rule_is_reported_as_usage_error():
    result = run_cli("scan", "نص", "--rules", "missing_rule", "--json")
    assert result.returncode == 2


def test_scan_empty_rules_is_reported_as_usage_error():
    for rules in ("", " , ", ",,,"):
        result = run_cli("scan", "الإستخدام", "--rules", rules, "--json")
        assert result.returncode == 2
        assert "قاعدة واحدة على الأقل" in result.stderr
