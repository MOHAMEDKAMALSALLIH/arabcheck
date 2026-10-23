from arabcheck.rules.hamza import HamzatQatRule


def test_detects_hamzat_qat_words():
    rule = HamzatQatRule()
    # verify the rule correctly ignores words like "الأمر", "الإنسان", and "الأحمد"
    issues = rule.check("الأحمد الأمر الإنسان الكتاب")

    assert len(issues) == 0


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

    assert issues[0]["rule"] == "hamzat_qat"
    assert issues[0]["severity"] == "warning"
    assert issues[0]["position"] == 1
