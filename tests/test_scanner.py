import pytest

from arabcheck.scanner import Scanner


def test_scanner_registers_hamza_rule_by_default():
    scanner = Scanner()
    assert scanner.available_rules() == ["hamzat_qat"]


def test_scanner_detects_hamza_issue():
    scanner = Scanner()
    issues = scanner.scan("الإستخدام الكتاب")

    assert len(issues) == 1
    assert issues[0]["rule"] == "hamzat_qat"
    assert issues[0]["word"] == "الإستخدام"
    assert issues[0]["position"] == 1


def test_scanner_can_select_rules():
    scanner = Scanner()
    assert scanner.scan("الإستخدام", rule_names=["hamzat_qat"])


def test_scanner_rejects_unknown_rule():
    scanner = Scanner()

    with pytest.raises(ValueError, match="Unknown rule"):
        scanner.scan("الإستخدام", rule_names=["not_a_rule"])


def test_scanner_returns_no_issues_for_empty_text():
    scanner = Scanner()
    assert scanner.scan("") == []
