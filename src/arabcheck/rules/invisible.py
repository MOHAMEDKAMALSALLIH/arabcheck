"""Detect explicitly listed invisible and control characters for human review."""

import re
import unicodedata
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
        word_spans = list(re.finditer(r"\S+", text))
        lines = text.split("\n")
        line_starts = []
        current_offset = 0
        for line in lines:
            line_starts.append(current_offset)
            current_offset += len(line) + 1

        for offset, char in enumerate(text):
            codepoint = ord(char)
            category = unicodedata.category(char)
            if not (
                codepoint in self.REPORTED_CODEPOINTS
                or (category == "Cc" and codepoint not in self.IGNORED_C0_C1)
            ):
                continue

            # Every reported character is non-whitespace, so it belongs to a
            # token matched by \S+, even when the token contains no letters.
            position = 1
            for word_number, span in enumerate(word_spans, start=1):
                if span.start() <= offset < span.end():
                    position = word_number
                    break
                if span.start() > offset:
                    position = max(1, word_number - 1)
                    break
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
