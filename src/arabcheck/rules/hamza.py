"""Rule for detecting possible hamzat qat issues."""

from typing import List, Dict

from arabcheck.patterns import Patterns
from .base import BaseRule


class HamzatQatRule(BaseRule):
    """Detect words starting with 'ال' followed by hamzat qat."""

    name = "hamzat_qat"
    description = "احتمال وجود همزة قطع بعد أل التعريف."
    severity = "warning"

    def __init__(self) -> None:
        self.patterns = Patterns()

    def check(self, text: str) -> List[Dict]:
        issues = []

        for position, word in enumerate(text.split(), start=1):
            if self.patterns.HAMZAT_QAT.match(word):
                intended = word.replace("الإ", "الا", 1)
                issues.append({
                    "rule": self.name,
                    "severity": self.severity,
                    "word": word,
                    "intended": intended,
                    "position": position,
                    "message": (
                        f"احتمال خطأ (تحذير للمراجعة البشرية): الكلمة '{word}' تبدو كمصدر يبدأ بهمزة وصل '{intended}'، هذه القاعدة تعتمد على تقريب نمطي وليست حلاً صرفياً كاملاً."
                    ),
                })

        return issues
