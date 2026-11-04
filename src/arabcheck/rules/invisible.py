"""Detect explicitly listed invisible and control characters for human review."""

import re
import unicodedata
from bisect import bisect_left, bisect_right
from typing import Dict, List

from .base import BaseRule


class InvisibleRule(BaseRule):
    """Report selected invisible characters without changing the input."""

    name = "invisible"
    description = "يرصد محارف مخفية أو تحكمية محددة لمراجعتها بشرياً."
    severity = "warning"

    REPORTED_CODEPOINTS = {
        0x200B, 0x2060, 0x00AD, 0xFEFF,
        *range(0x202A, 0x202F),
        *range(0x2066, 0x206A),
        *range(0xE0000, 0xE0080),
    }
    IGNORED_C0_C1 = {0x0009, 0x000A, 0x000D}

    def check(self, text: str) -> List[Dict]:
        issues = []
        reported_offsets = []
        whitespace_offsets = []
        visible_chars = []
        original_offsets = []

        for offset, char in enumerate(text):
            codepoint = ord(char)
            category = unicodedata.category(char)
            is_reported = (
                codepoint in self.REPORTED_CODEPOINTS
                or (category == "Cc" and codepoint not in self.IGNORED_C0_C1)
            )
            is_space = char.isspace()
            if is_space:
                whitespace_offsets.append(offset)
            if is_reported:
                reported_offsets.append(offset)
                # Some reportable Cc controls are also whitespace (for
                # example VT, FF, and NEL). Preserve their separator role
                # when building word spans, even though they remain issues.
                if is_space:
                    visible_chars.append(char)
                    original_offsets.append(offset)
            else:
                visible_chars.append(char)
                original_offsets.append(offset)

        # Build word spans without reportable non-whitespace characters.
        # This keeps an invisible character inside a word from splitting it,
        # while preserving whitespace boundaries and avoiding invented
        # positions for invisible-only input.
        visible_text = "".join(visible_chars)
        word_starts = []
        word_ends = []
        for match in re.finditer(r"\S+", visible_text):
            word_starts.append(original_offsets[match.start()])
            word_ends.append(original_offsets[match.end() - 1])

        line_starts = []
        current_offset = 0
        for line in text.split("\n"):
            line_starts.append(current_offset)
            current_offset += len(line) + 1

        def has_whitespace(start: int, stop: int) -> bool:
            """True if any whitespace character lies at offsets [start, stop)."""
            return (
                bisect_left(whitespace_offsets, start)
                < bisect_left(whitespace_offsets, stop)
            )

        # Offsets are collected in increasing order, so no sorting is needed.
        for offset in reported_offsets:
            char = text[offset]
            codepoint = ord(char)

            # A character belongs to a word only when no whitespace separates
            # it from that word. Binary search finds the nearest words instead
            # of scanning all of them for every reported character.
            position = None
            index = bisect_right(word_starts, offset) - 1
            if index >= 0 and offset <= word_ends[index]:
                position = index + 1
            else:
                if index >= 0 and not has_whitespace(
                    word_ends[index] + 1, offset + 1
                ):
                    position = index + 1
                following = index + 1
                if following < len(word_starts) and not has_whitespace(
                    offset, word_starts[following]
                ):
                    position = following + 1

            line_number = bisect_right(line_starts, offset)
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
                "rule": self.name,
                "type": "invisible",
                "severity": self.severity,
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
