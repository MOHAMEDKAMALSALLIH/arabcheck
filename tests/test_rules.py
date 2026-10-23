from arabcheck.rules.hamza import HamzatQatRule


def test_detects_common_hamzat_wasl_spelling_mistakes():
    rule = HamzatQatRule()
    issues = rule.check("الإستخدام الإختبار الإجتماع")

    assert [issue["word"] for issue in issues] == [
        "الإستخدام", "الإختبار", "الإجتماع",
    ]
    assert [issue["intended"] for issue in issues] == [
        "الاستخدام", "الاختبار", "الاجتماع",
    ]


def test_ignores_valid_words_and_unlisted_words():
    rule = HamzatQatRule()
    assert rule.check(
        "الأحمد الأمر الإنسان الكتاب الإسلام الإمام الإبداع"
    ) == []
    assert rule.check("نص غير معروف") == []


def test_issue_has_compatible_fields_and_human_review_message():
    issue = HamzatQatRule().check("الإستخدام")[0]

    assert issue["rule"] == "hamzat_qat"
    assert issue["type"] == "hamzat_qat"
    assert issue["severity"] == "warning"
    assert issue["position"] == 1
    assert issue["location"] == {"word": 1}
    assert "الاستخدام" in issue["message"]
    assert "المراجعة البشرية" in issue["message"]


def test_word_position_counts_tokens():
    issues = HamzatQatRule().check("هذا هو الإختبار")
    assert len(issues) == 1
    assert issues[0]["position"] == 3
