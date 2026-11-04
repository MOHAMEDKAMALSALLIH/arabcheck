"""Performance and full-behavior equivalence tests for InvisibleRule.

The independent legacy implementation below preserves the pre-optimization
behavior from main. The optimized rule must return identical issue dictionaries.
"""

import random
import re
import time
import unicodedata

from arabcheck.rules.invisible import InvisibleRule


# Independent copies of the constants used by the pre-PR #9 implementation.
_LEGACY_REPORTED_CODEPOINTS = {
    0x200B, 0x2060, 0x00AD, 0xFEFF,
    *range(0x202A, 0x202F),
    *range(0x2066, 0x206A),
    *range(0xE0000, 0xE0080),
}
_LEGACY_IGNORED_C0_C1 = {0x0009, 0x000A, 0x000D}


def _legacy_check(text):
    """Independent copy of the pre-PR #9 InvisibleRule.check implementation."""
    issues = []
    reported_offsets = set()
    visible_chars = []
    original_offsets = []

    for offset, char in enumerate(text):
        codepoint = ord(char)
        category = unicodedata.category(char)
        is_reported = (
            codepoint in _LEGACY_REPORTED_CODEPOINTS
            or (
                category == "Cc"
                and codepoint not in _LEGACY_IGNORED_C0_C1
            )
        )
        if is_reported:
            reported_offsets.add(offset)
            # Preserve the separator role of reportable whitespace controls.
            if char.isspace():
                visible_chars.append(char)
                original_offsets.append(offset)
        else:
            visible_chars.append(char)
            original_offsets.append(offset)

    visible_text = "".join(visible_chars)
    word_spans = []
    for match in re.finditer(r"\S+", visible_text):
        word_spans.append((
            original_offsets[match.start()],
            original_offsets[match.end() - 1],
        ))

    lines = text.split("\n")
    line_starts = []
    current_offset = 0
    for line in lines:
        line_starts.append(current_offset)
        current_offset += len(line) + 1

    for offset in sorted(reported_offsets):
        char = text[offset]
        codepoint = ord(char)

        position = None
        for word_number, (start, end) in enumerate(word_spans, start=1):
            # The character belongs to a word only when no whitespace
            # separates it from that word.
            if start <= offset <= end:
                position = word_number
                break
            if offset < start:
                if not any(c.isspace() for c in text[offset:start]):
                    position = word_number
                break
            if offset > end:
                if not any(c.isspace() for c in text[end + 1:offset + 1]):
                    position = word_number

        line_number = 1
        for candidate, start in enumerate(line_starts, start=1):
            if start > offset:
                break
            line_number = candidate
        column = offset - line_starts[line_number - 1] + 1

        char_label = "U+{:04X}".format(codepoint)
        character_name = unicodedata.name(
            char, "UNNAMED UNICODE CHARACTER"
        )
        if codepoint == 0xFEFF and offset == 0:
            message = (
                "عُثر على علامة BOM في بداية النص؛ قد تكون أثراً لترميز "
                "الملف. يُرجى التحقق بشرياً قبل اتخاذ أي إجراء."
            )
        else:
            message = (
                "عُثر على محرف غير مرئي أو تحكمي {} ({})؛ "
                "يُرجى مراجعته بشرياً. لم يُعدّل النص."
            ).format(char_label, character_name)

        issues.append({
            "rule": "invisible",
            "type": "invisible",
            "severity": "warning",
            "char": char_label,
            "name": character_name,
            "position": position,
            "location": {
                "word": position,
                "line": line_number,
                "column": column,
                "offset": offset,
            },
            "message": message,
        })

    return issues


def _assert_full_equivalence(text, case_id):
    actual = InvisibleRule().check(text)
    expected = _legacy_check(text)
    assert actual == expected, (
        "Mismatch in {} for text={!r}\nactual={!r}\nexpected={!r}".format(
            case_id, text, actual, expected
        )
    )


def test_matches_reference_on_random_texts():
    # Keep this original seed and alphabet unchanged for reproducibility.
    alphabet = [
        "ب", "ت", "ث", " ", " ", "\n", "\t", "\r",
        "\u200b", "\u200b", "\u2060", "\ufeff", "\u202e",
        "\x0b", "\x0c", "\x1f", "\x85", "\U000E0041",
    ]
    rng = random.Random(20261103)
    for case_number in range(2000):
        text = "".join(
            rng.choice(alphabet) for _ in range(rng.randint(0, 30))
        )
        _assert_full_equivalence(text, "original random case #{}".format(
            case_number
        ))


def test_matches_reference_on_random_texts_with_crlf():
    alphabet = [
        "ا", "ب", "ت", "كلمة", "نص", " ", "\n", "\r", "\r\n",
        "\u200b", "\u200c", "\u200d", "\u200e", "\u200f", "\ufeff",
    ]
    rng = random.Random(42)
    for case_number in range(500):
        text = "".join(
            rng.choice(alphabet) for _ in range(rng.randint(0, 120))
        )
        _assert_full_equivalence(text, "CRLF random case #{}".format(
            case_number
        ))


def test_matches_reference_on_explicit_edge_cases():
    cases = [
        ("empty", ""),
        ("bom_second_line_start", "\n\ufeffنص"),
        ("invisibles_around_newline", "أ\u200b\n\u200cب"),
        ("both_text_edges_reported", "\u200bنص\u200b"),
        ("consecutive_empty_lines", "\n\n\u200b\n\n"),
        ("mixed_consecutive_invisibles", "\u200b\u200c\u200d"),
        ("reported_chars_separated_by_excluded_zwnj", "\u200b\u200c\u200b"),
        # The legacy split("\n") logic counts CR as part of the previous line.
        ("crlf_line_break", "سطر1\r\n\u200bسطر2"),
        ("diacritics_with_invisible", "كَلِمَةٌ\u200b"),
        ("leading_bom_special_message", "\ufeffنص"),
    ]
    for case_number, (case_id, text) in enumerate(cases):
        _assert_full_equivalence(
            text, "explicit case #{} ({})".format(case_number, case_id)
        )


def test_word_assignment_rules_are_preserved():
    cases = {
        "ab \u200b cd": [None],   # isolated between whitespace
        "ab\u200b cd": [1],       # attached to the end of a word
        "ab \u200bcd": [2],       # attached to the start of a word
        "\u200b": [None],         # invisible-only input
        "ab\x0ccd": [None],       # whitespace-like control separates words
        "\u200bab": [1],
        "ab\u200b": [1],
        "a\u200b\u200bb": [1, 1],  # several invisibles inside one word
    }
    for case_number, (text, expected) in enumerate(cases.items()):
        _assert_full_equivalence(
            text, "word assignment case #{}".format(case_number)
        )
        positions = [issue["position"] for issue in InvisibleRule().check(text)]
        assert positions == expected, repr(text)


def test_stress_many_words_and_invisible_characters():
    words = [
        "كل\u200bمة" if index % 4 == 0 else "كلمة" for index in range(20000)
    ]
    text = " ".join(words)

    started = time.perf_counter()
    issues = InvisibleRule().check(text)
    elapsed = time.perf_counter() - started

    assert len(issues) == 5000
    assert elapsed < 2.0, "InvisibleRule.check took {:.2f}s".format(elapsed)


def test_stress_many_lines():
    text = "\n".join(["سطر\u200b"] * 20000)

    started = time.perf_counter()
    issues = InvisibleRule().check(text)
    elapsed = time.perf_counter() - started

    assert len(issues) == 20000
    assert issues[-1]["location"]["line"] == 20000
    assert elapsed < 2.0, "InvisibleRule.check took {:.2f}s".format(elapsed)
