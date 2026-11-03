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
        reported_offsets = set()
        visible_chars = []
        original_offsets = []

        for offset, char in enumerate(text):
            codepoint = ord(char)
            category = unicodedata.category(char)
            is_reported = (
                codepoint in self.REPORTED_CODEPOINTS
                or (category == "Cc" and codepoint not in self.IGNORED_C0_C1)
            )
            if is_reported:
                reported_offsets.add(offset)
            else:
                visible_chars.append(char)
                original_offsets.append(offset)

        # Build word spans after omitting reportable characters. This keeps an
        # invisible character inside a word from splitting that word, while
        # ensuring an invisible-only input has no invented word positions.
        visible_text = "".join(visible_chars)
        word_spans = []
        for match in re.finditer(r"\\S+", visible_text):
            word_spans.append((
                original_offsets[match.start()],
                original_offsets[match.end() - 1],
            ))

        lines = text.split("\\n")
        line_starts = []
        current_offset = 0
        for line in lines:
            line_starts.append(current_offset)
            current_offset += len(line) + 1

        for offset in sorted(reported_offsets):
            char = text[offset]
            codepoint = ord(char)

            position = None
            if word_spans:
                for word_number, (start, end) in enumerate(word_spans, start=1):
                    if start <= offset <= end:
                        position = word_number
                        break
                    if start > offset:
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
