from arabcheck.rules.hamza import HamzatQatRule


def test_detects_hamzat_qat_words():
    rule = HamzatQatRule()
    issues = rule.check("الأحمد الكتاب الإنسان")

    assert len(issues) == 2
    assert [issue["word"] for issue in issues] == [
        "الأحمد",
        "الإنسان",
    ]


def test_ignores_words_without_matching_pattern():
    rule = HamzatQatRule()

    assert rule.check("الكتاب مدرسة جميل") == []


def test_issue_contains_rule_and_severity():
    rule = HamzatQatRule()
    issues = rule.check("الأحمد")

    assert issues[0]["rule"] == "hamzat_qat"
    assert issues[0]["severity"] == "warning"
    assert issues[0]["position"] == 1
