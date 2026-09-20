"""أنماط regex المجمّعة مسبقاً."""
from __future__ import annotations
import re


class Patterns:
    TASHKEEL = re.compile(
        r"[\u0610-\u061A\u064B-\u065F\u0670"
        r"\u06D6-\u06DC\u06DF-\u06E8\u06EA-\u06ED]"
    )
    TATWEEL = re.compile(r"\u0640")
    WHITESPACE = re.compile(r"\s+")
    HAMZAT_QAT = re.compile(r"^ال[أإآ]")
    ALIF_VARIANTS = re.compile(r"[إأآٱ]")
    YAA_VARIANTS = re.compile(r"[ىي]")
    TAA_MARBUTA = re.compile(r"ة")
    HAMZA_WAW = re.compile(r"ؤ")
    HAMZA_YAA = re.compile(r"ئ")
