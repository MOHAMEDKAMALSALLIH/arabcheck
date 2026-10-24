import pytest

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
    assert "تحذير" in issue["message"]
    assert "آلياً مؤكداً" in issue["message"]


def test_word_position_counts_tokens():
    issues = HamzatQatRule().check("هذا هو الإختبار")
    assert len(issues) == 1
    assert issues[0]["position"] == 3


@pytest.mark.parametrize(
    "word, expected_intended",
    [
        ("الإستخدام", "الاستخدام"),
        ("والإستخدام", "والاستخدام"),
        ("بالإستخدام", "بالاستخدام"),
        ("للإستخدام", "للاستخدام"),
        ("،«للإستخدام».", "للاستخدام"),
        ("وللإستخدام", "وللاستخدام"),
        ("فللإستخدام", "فللاستخدام"),
    ],
)
def test_hamzat_qat_prefixes_and_intended(word, expected_intended):
    issues = HamzatQatRule().check(word)

    assert len(issues) == 1
    assert issues[0]["word"] == word
    assert issues[0]["intended"] == expected_intended


@pytest.mark.parametrize(
    "valid_word",
    ["الأمر", "الإسلام", "والأمر", "للإسلام", "الاستخدام"],
)
def test_hamzat_qat_ignores_valid_words(valid_word):
    assert HamzatQatRule().check(valid_word) == []


@pytest.mark.parametrize(
    "word, expected_intended",
    [
        ("الإِسْتِخْدام", "الاستخدام"),
        ("الإـستخدام", "الاستخدام"),
        ("،«للإِسْتِخْدام».", "للاستخدام"),
    ],
)
def test_hamzat_qat_handles_diacritics_tatweel_and_punctuation(
    word, expected_intended
):
    issues = HamzatQatRule().check(word)

    assert len(issues) == 1
    assert issues[0]["word"] == word
    assert issues[0]["intended"] == expected_intended
