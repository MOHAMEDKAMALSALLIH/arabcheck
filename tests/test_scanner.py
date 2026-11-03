import pytest

from arabcheck.scanner import Scanner


def test_scanner_registers_rules_by_default():
    assert Scanner().available_rules() == ["hamzat_qat", "invisible"]


def test_scanner_detects_suspicious_hamza_issue_not_valid_words():
    scanner = Scanner()
    issues = scanner.scan("الأحمد الكتاب الإستخدام")

    assert len(issues) == 1
    assert issues[0]["rule"] == "hamzat_qat"
    assert issues[0]["word"] == "الإستخدام"
    assert issues[0]["intended"] == "الاستخدام"
    assert issues[0]["position"] == 3


def test_scanner_detects_invisible_character_by_default():
    issues = Scanner().scan("هذا ب\u200bت")

    assert len(issues) == 1
    assert issues[0]["rule"] == "invisible"
    assert issues[0]["type"] == "invisible"
    assert issues[0]["char"] == "U+200B"


def test_scanner_can_select_rules():
    scanner = Scanner()
    assert scanner.scan("الإستخدام", rule_names=["hamzat_qat"])
    assert scanner.scan("ب\u200bت", rule_names=["invisible"])


def test_scanner_can_keep_legacy_hamza_only_results():
    issues = Scanner().scan("الأحمد الإستخدام ب\u200bت", rule_names=["hamzat_qat"])
    assert len(issues) == 1
    assert issues[0]["rule"] == "hamzat_qat"
    assert issues[0]["word"] == "الإستخدام"


def test_scanner_rejects_unknown_rule():
    with pytest.raises(ValueError, match="Unknown rule"):
        Scanner().scan("الإستخدام", rule_names=["not_a_rule"])


def test_scanner_rejects_duplicate_rule_selection():
    with pytest.raises(ValueError, match="Duplicate rule selection"):
        Scanner().scan(
            "الإستخدام", rule_names=["hamzat_qat", "hamzat_qat"]
        )


def test_scanner_returns_no_issues_for_empty_or_valid_text():
    scanner = Scanner()
    assert scanner.scan("") == []
    assert scanner.scan("الأحمد الأمر الإنسان الكتاب") == []
