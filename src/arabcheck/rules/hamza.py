"""Conservative rule for common hamzat-wasl spelling mistakes."""

import re
import unicodedata
from typing import Dict, List, Optional

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
    # Prefixes that appear before the article "ال".
    DIRECT_PREFIXES = ("وب", "وف", "وك", "فب", "فك", "و", "ف", "ب", "ك")
    # Prepositions ending in lam, where the alif of the article is omitted.
    LAM_PREFIXES = ("ولل", "فلل", "لل")

    @classmethod
    def _clean_word(cls, word: str) -> str:
        normalized = cls.TASHKEEL.sub("", word).replace("ـ", "")
        while normalized and unicodedata.category(normalized[0])[0] in ("P", "S"):
            normalized = normalized[1:]
        while normalized and unicodedata.category(normalized[-1])[0] in ("P", "S"):
            normalized = normalized[:-1]
        return normalized

    @classmethod
    def _resolve_intended(cls, word: str) -> Optional[str]:
        """Return the suggested correct form with its prefix preserved."""
        normalized = cls._clean_word(word)

        if normalized in cls.SUSPICIOUS_FORMS:
            return cls.SUSPICIOUS_FORMS[normalized]

        # E.g. للإستخدام -> للاستخدام, وللإستخدام -> وللاستخدام.
        for prefix in cls.LAM_PREFIXES:
            if normalized.startswith(prefix) and len(normalized) > len(prefix):
                candidate = "ال" + normalized[len(prefix):]
                if candidate in cls.SUSPICIOUS_FORMS:
                    corrected_base = cls.SUSPICIOUS_FORMS[candidate]
                    return prefix + corrected_base[2:]

        # E.g. والإستخدام -> والاستخدام, بالإستخدام -> بالاستخدام.
        for prefix in cls.DIRECT_PREFIXES:
            if normalized.startswith(prefix) and len(normalized) > len(prefix):
                candidate = normalized[len(prefix):]
                if candidate in cls.SUSPICIOUS_FORMS:
                    return prefix + cls.SUSPICIOUS_FORMS[candidate]

        return None

    def check(self, text: str) -> List[Dict]:
        issues = []
        for position, word in enumerate(text.split(), start=1):
            intended = self._resolve_intended(word)
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
