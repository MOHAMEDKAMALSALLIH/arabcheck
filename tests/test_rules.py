from arabcheck.rules.hamza import HamzatQatRule


def test_detects_suspicious_hamzat_qat_words():
    rule = HamzatQatRule()
    issues = rule.check("الإستخدام الكتاب الإجتماع الإختبار")

    assert len(issues) == 3
    assert [issue["word"] for issue in issues] == [
        "الإستخدام",
        "الإجتماع",
        "الإختبار",
    ]


def test_ignores_correct_hamzat_qat_words():
    rule = HamzatQatRule()
    # These are correct words that naturally start with hamza
    assert rule.check("الأحمد الأمر الإنسان الأول الأسد") == []


def test_ignores_words_without_matching_pattern():
    rule = HamzatQatRule()

    assert rule.check("الكتاب مدرسة جميل الاستخدام") == []


def test_issue_contains_rule_and_severity():
    rule = HamzatQatRule()
    issues = rule.check("الإستخدام")

    assert issues[0]["rule"] == "hamzat_qat"
    assert issues[0]["severity"] == "warning"
    assert issues[0]["position"] == 1
