from arabcheck.rules.hamza import HamzatQatRule


def test_ignores_valid_words():
    rule = HamzatQatRule()
    assert rule.check("الأحمد الأمر الإنسان الكتاب") == []


def test_suspicious_hamzat_qat_forms():
    rule = HamzatQatRule()
    issues = rule.check("الإستخدام الإختبار الإجتماع")

    assert len(issues) == 3
    assert [issue["word"] for issue in issues] == [
        "الإستخدام",
        "الإختبار",
        "الإجتماع",
    ]
    assert [issue["intended"] for issue in issues] == [
        "الاستخدام",
        "الاختبار",
        "الاجتماع",
    ]


def test_ignores_words_without_matching_pattern():
    rule = HamzatQatRule()
    assert rule.check("الكتاب مدرسة جميل") == []


def test_issue_contains_rule_and_severity():
    rule = HamzatQatRule()
    issues = rule.check("الإستخدام")

    assert len(issues) == 1
    assert issues[0]["rule"] == "hamzat_qat"
    assert issues[0]["severity"] == "warning"
    assert issues[0]["position"] == 1
