"""Performance and equivalence tests for InvisibleRule.

The reference function below is the pre-optimization algorithm (repeated
linear scans). The optimized rule must give identical results.
"""

import random
import re
import time
import unicodedata

from arabcheck.rules.invisible import InvisibleRule


def _reference_positions(text):
    """Return (offset, position, line, column) per reported character,
    using the original linear-scan algorithm."""
    reported_offsets = set()
    visible_chars = []
    original_offsets = []

    for offset, char in enumerate(text):
        codepoint = ord(char)
        is_reported = (
            codepoint in InvisibleRule.REPORTED_CODEPOINTS
            or (
                unicodedata.category(char) == "Cc"
                and codepoint not in InvisibleRule.IGNORED_C0_C1
            )
        )
        if is_reported:
            reported_offsets.add(offset)
            if char.isspace():
                visible_chars.append(char)
                original_offsets.append(offset)
        else:
            visible_chars.append(char)
            original_offsets.append(offset)

    visible_text = "".join(visible_chars)
    word_spans = [
        (original_offsets[m.start()], original_offsets[m.end() - 1])
        for m in re.finditer(r"\S+", visible_text)
    ]

    line_starts = []
    current_offset = 0
    for line in text.split("\n"):
        line_starts.append(current_offset)
        current_offset += len(line) + 1

    results = []
    for offset in sorted(reported_offsets):
        position = None
        for word_number, (start, end) in enumerate(word_spans, start=1):
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
        results.append((offset, position, line_number, column))
    return results


def _actual_positions(text):
    return [
        (
            issue["location"]["offset"],
            issue["position"],
            issue["location"]["line"],
            issue["location"]["column"],
        )
        for issue in InvisibleRule().check(text)
    ]


def test_matches_reference_on_random_texts():
    alphabet = [
        "ب", "ت", "ث", " ", " ", "\n", "\t", "\r",
        "\u200b", "\u200b", "\u2060", "\ufeff", "\u202e",
        "\x0b", "\x0c", "\x1f", "\x85", "\U000E0041",
    ]
    rng = random.Random(20261103)
    for _ in range(2000):
        text = "".join(
            rng.choice(alphabet) for _ in range(rng.randint(0, 30))
        )
        assert _actual_positions(text) == _reference_positions(text), repr(text)


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
    for text, expected in cases.items():
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
