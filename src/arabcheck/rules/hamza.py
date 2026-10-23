"""Conservative rule for common hamzat-wasl spelling mistakes."""

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

    def check(self, text: str) -> List[Dict]:
        issues = []
        for position, word in enumerate(text.split(), start=1):
            intended = self.SUSPICIOUS_FORMS.get(word)
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
                    f"احتمال خطأ إملائي: '{word}'؛ الصيغة الشائعة الصحيحة "
                    f"هي '{intended}'. تحذير للمراجعة البشرية، وليس تصحيحاً "
                    "آلياً مؤكداً."
                ),
            })
        return issues
