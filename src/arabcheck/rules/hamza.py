"""Conservative rule for common hamzat-wasl spelling mistakes."""

import re
import unicodedata
from typing import Dict, List
from .base import BaseRule


class HamzatQatRule(BaseRule):
    """Flag known common mistakes for human review; avoid broad prefix guesses."""

    name = "hamzat_qat"
    description = "يرصد صيغاً شائعة يُحتمل أن همزتها كُتبت خطأ؛ يلزم التحقق البشري."
    severity = "warning"

    SUSPICIOUS_FORMS = {
        "الاستخدام": "الاستخدام", "الاستعمال": "الاستعمال",
        "الاستفادة": "الاستفادة", "الاستمرار": "الاستمرار",
        "الاستقبال": "الاستقبال", "الاستعداد": "الاستعداد",
        "الاستنتاج": "الاستنتاج", "الاستثمار": "الاستثمار",
        "الاختبار": "الاختبار", "الاختيار": "الاختيار",
        "الاختلاف": "الاختلاف", "الاجتماع": "الاجتماع",
        "الاجتماعي": "الاجتماعي", "الاشتراك": "الاشتراك",
        "الاشتغال": "الاشتغال", "الاعتذار": "الاعتذار",
        "الاعتقاد": "الاعتقاد", "الاعتناء": "الاعتناء",
        "الاقتراح": "الاقتراح", "الاقتصاد": "الاقتصاد",
        "الاقتباس": "الاقتباس", "الابتكار": "الابتكار",
        "الارتباط": "الارتباط", "الارتفاع": "الارتفاع",
        "الانتظار": "الانتظار", "الانتقال": "الانتقال",
        "الانتشار": "الانتشار", "الانتباه": "الانتباه",
        "الانتخاب": "الانتخاب", "الامتحان": "الامتحان",
        "الامتناع": "الامتناع",
    }

    TASHKEEL = re.compile(
        "[\\u0610-\\u061A\\u064B-\\u065F\\u0670"
        "\\u06D6-\\u06DC\\u06DF-\\u06E8\\u06EA-\\u06ED]"
    )
    PUNCTUATION = re.compile(r"^[\\W_]+|[\\W_]+$", re.UNICODE)
    PREFIXES = ("وال", "بال", "كال", "فال", "لل", "ال", "و", "ف", "ب", "ك", "ل")

    @classmethod
    def _lookup_form(cls, word: str) -> str:
        normalized = cls.TASHKEEL.sub("", word).replace("ـ", "")
        normalized = cls.PUNCTUATION.sub("", normalized)
        # Match the known base word, optionally after common attached prefixes.
        for prefix in cls.PREFIXES:
            if normalized.startswith(prefix) and len(normalized) > len(prefix):
                candidate = "ال" + normalized[len(prefix):] if prefix in ("و", "ف", "ب", "ك") else normalized[len(prefix):]
                if candidate in cls.SUSPICIOUS_FORMS:
                    return candidate
        return normalized

    def check(self, text: str) -> List[Dict]:
        issues = []
        for position, word in enumerate(text.split(), start=1):
            lookup = self._lookup_form(word)
            intended = self.SUSPICIOUS_FORMS.get(lookup)
            if intended is None:
                continue
            issues.append({
                "rule": self.name,
                "type": self.name,
                "severity": self.severity,
                "word": word,
                "intended": intended,
                "position": position,
                "location": {"word": position},
                "message": (
                    f"احتمال خطأ إملائي: '{word}'؛ الصيغة المقترحة للمراجعة "
                    f"هي '{intended}'. تحذير للمراجعة البشرية، وليس تصحيحاً "
                    "آلياً مؤكداً."
                ),
            })
        return issues
