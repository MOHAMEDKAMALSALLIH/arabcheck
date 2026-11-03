import unicodedata

import pytest

from arabcheck.rules.invisible import InvisibleRule


REPORTED_EXPLICIT = [
    0x200B, 0x2060, 0x00AD, 0xFEFF,
    *range(0x202A, 0x202F),
    *range(0x2066, 0x206A),
    *range(0xE0000, 0xE0080),
]
REPORTED_C0_C1 = [
    cp for cp in range(0x110000)
    if unicodedata.category(chr(cp)) == "Cc" and cp not in {9, 10, 13}
]
NEVER_REPORTED = [
    0x0600, 0x0601, 0x0602, 0x0603, 0x0604, 0x0605, 0x06DD,
    0x200C, 0x200D, 0x200E, 0x200F, 0x061C, 0x00A0, 0x202F,
]


@pytest.mark.parametrize("codepoint", sorted(set(REPORTED_EXPLICIT + REPORTED_C0_C1)))
def test_reports_each_listed_codepoint(codepoint):
    issue = InvisibleRule().check("ب" + chr(codepoint) + "ت")[0]
    assert issue["char"] == "U+{:04X}".format(codepoint)
    assert issue["type"] == "invisible"
    assert issue["rule"] == "invisible"
    assert issue["severity"] == "warning"
    assert issue["name"] == unicodedata.name(
        chr(codepoint), "UNNAMED UNICODE CHARACTER"
    )


@pytest.mark.parametrize("codepoint", NEVER_REPORTED)
def test_does_not_report_legitimate_or_context_dependent_characters(codepoint):
    assert InvisibleRule().check("ب" + chr(codepoint) + "ت") == []


def test_clean_arabic_text_has_no_issues():
    assert InvisibleRule().check("هذا نص عربي سليم") == []


def test_ayah_end_marker_is_not_reported():
    assert InvisibleRule().check("بسم الله الرحمن الرحيم ۝") == []


def test_persian_zwnj_is_not_reported():
    assert InvisibleRule().check("می‌روم") == []


def test_multiple_invisibles_in_one_word_keep_same_word_position():
    issues = InvisibleRule().check("هذا ب\u200bت\u2060ث")
    assert [issue["position"] for issue in issues] == [2, 2]
    assert [issue["location"]["word"] for issue in issues] == [2, 2]


def test_invisible_only_text_has_no_word_position():
    issues = InvisibleRule().check("\u200b \u2060")
    assert [issue["position"] for issue in issues] == [None, None]
    assert [issue["location"]["word"] for issue in issues] == [None, None]


def test_invisible_characters_inside_words_do_not_split_word_positions():
    issues = InvisibleRule().check("أ\u200bب ت\u2060ث")
    assert [issue["position"] for issue in issues] == [1, 2]


def test_invisible_in_whitespace_between_words_has_none_position():
    issues = InvisibleRule().check("كلمة \u200b أخرى")
    assert len(issues) == 1
    assert issues[0]["position"] is None
    assert issues[0]["location"]["word"] is None


def test_multiple_invisibles_attached_to_word_keep_word_position():
    issues = InvisibleRule().check("\u200b\u2060كلمة")
    assert len(issues) == 2
    assert [issue["position"] for issue in issues] == [1, 1]

    issues_trailing = InvisibleRule().check("كلمة\u200b\u2060")
    assert len(issues_trailing) == 2
    assert [issue["position"] for issue in issues_trailing] == [1, 1]


def test_bom_at_start_has_file_bom_message():
    issue = InvisibleRule().check("\ufeffمرحبا")[0]
    assert issue["char"] == "U+FEFF"
    assert issue["location"]["offset"] == 0
    assert "BOM" in issue["message"]


def test_bom_in_middle_has_general_invisible_message():
    issue = InvisibleRule().check("مرح\ufeffبا")[0]
    assert issue["location"]["offset"] == 3
    assert "BOM" not in issue["message"]


def test_offsets_lines_columns_and_word_positions():
    issues = InvisibleRule().check("أول\nثا\u200bني كلمة\nثالث")

    issue = issues[0]
    assert issue["position"] == 2
    assert issue["location"] == {
        "word": 2, "line": 2, "column": 3, "offset": 6,
    }


def test_crlf_line_and_column_offsets():
    issues = InvisibleRule().check("أول\r\nثا\u200bني\r\nثالث")
    issue = issues[0]
    assert issue["location"] == {
        "word": 2, "line": 2, "column": 3, "offset": 7,
    }


def test_nul_and_escape_controls_are_reported():
    issues = InvisibleRule().check("أ\x00ب\x1bج")
    assert [issue["char"] for issue in issues] == ["U+0000", "U+001B"]


def test_tabs_newlines_and_carriage_returns_are_not_reported():
    assert InvisibleRule().check("أ\tب\nج\rد") == []


def test_input_is_not_modified():
    text = "مرح\u200bبا"
    before = text[:]
    InvisibleRule().check(text)
    assert text == before
