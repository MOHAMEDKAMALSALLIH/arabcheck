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
        "الإستخدام": "الاستخدام", "الإستعمال": "الاستعمال",
        "الإستفادة": "الاستفادة", "الإستمرار": "الاستمرار",
        "الإستقبال": "الاستقبال", "الإستعداد": "الاستعداد",
        "الإستنتاج": "الاستنتاج", "الإستثمار": "الاستثمار",
        "الإختبار": "الاختبار", "الإختيار": "الاختيار",
        "الإختلاف": "الاختلاف", "الإجتماع": "الاجتماع",
        "الإجتماعي": "الاجتماعي", "الإشتراك": "الاشتراك",
        "الإشتغال": "الاشتغال", "الإعتذار": "الاعتذار",
        "الإعتقاد": "الاعتقاد", "الإعتناء": "الاعتناء",
        "الإقتراح": "الاقتراح", "الإقتصاد": "الاقتصاد",
        "الإقتباس": "الاقتباس", "الإبتكار": "الابتكار",
        "الإرتباط": "الارتباط", "الإرتفاع": "الارتفاع",
        "الإنتظار": "الانتظار", "الإنتقال": "الانتقال",
        "الإنتشار": "الانتشار", "الإنتباه": "الانتباه",
        "الإنتخاب": "الانتخاب", "الإمتحان": "الامتحان",
        "الإمتناع": "الامتناع",
    }

    TASHKEEL = re.compile(
        r"[\u0610-\u061A\u064B-\u065F\u0670"
        r"\u06D6-\u06DC\u06DF-\u06E8\u06EA-\u06ED]"
    )
    PREFIXES = ("وال", "بال", "كال", "فال", "لل", "و", "ف", "ب", "ك", "ل")

    @classmethod
    def _lookup_form(cls, word: str) -> str:
        normalized = cls.TASHKEEL.sub("", word).replace("ـ", "")
        # Remove punctuation/symbols at the edges, preserving the original word for output.
        while normalized and unicodedata.category(normalized[0])[0] in ("P", "S"):
            normalized = normalized[1:]
        while normalized and unicodedata.category(normalized[-1])[0] in ("P", "S"):
            normalized = normalized[:-1]
        if normalized in cls.SUSPICIOUS_FORMS:
            return normalized
        for prefix in cls.PREFIXES:
            if normalized.startswith(prefix) and len(normalized) > len(prefix):
                candidate = normalized[len(prefix):]
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
