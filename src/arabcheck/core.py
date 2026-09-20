"""النواة الرئيسية لـ ArabCheck."""
from __future__ import annotations
from .patterns import Patterns


class ArabCheck:
    def __init__(self) -> None:
        self.patterns = Patterns()

    def strip_tashkeel(self, text: str) -> str:
        return self.patterns.TASHKEEL.sub("", text)

    def strip_tatweel(self, text: str) -> str:
        return self.patterns.TATWEEL.sub("", text)

    def clean_text(self, text: str) -> str:
        text = self.strip_tashkeel(text)
        text = self.strip_tatweel(text)
        return self.patterns.WHITESPACE.sub(" ", text).strip()

    def normalize(self, text: str, *, taa_marbuta: bool = False) -> str:
        text = self.patterns.ALIF_VARIANTS.sub("ا", text)
        text = self.patterns.YAA_VARIANTS.sub("ي", text)
        text = self.patterns.HAMZA_WAW.sub("و", text)
        text = self.patterns.HAMZA_YAA.sub("ي", text)
        if taa_marbuta:
            text = self.patterns.TAA_MARBUTA.sub("ه", text)
        return text

    def audit(self, text: str) -> list:
        issues = []
        for i, word in enumerate(text.split(), start=1):
            if self.patterns.HAMZAT_QAT.match(word):
                issues.append({
                    "type": "hamzat_qat",
                    "word": word,
                    "position": i,
                    "message": f"احتمال خطأ: '{word}' تبدأ بـ 'ال' + همزة قطع.",
                })
        return issues

    def process(self, text, *, clean=False, normalize=False, audit=False):
        issues = self.audit(text) if audit else []
        result = text
        if normalize:
            result = self.normalize(result)
        if clean:
            result = self.clean_text(result)
        return {"input": text, "result": result, "issues": issues}
