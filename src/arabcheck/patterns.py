"""أنماط regex المجمّعة مسبقاً."""
from __future__ import annotations

import re


class Patterns:
    """أنماط regex لأداء أفضل (compiled once)."""

    # التشكيل: حركات + علامات قرآنية + ألف خنجرية
    TASHKEEL = re.compile(
        "[\u0610-\u061A\u064B-\u065F\u0670"
        "\u06D6-\u06DC\u06DF-\u06E8\u06EA-\u06ED]"
    )

    TATWEEL = re.compile("\u0640")
    WHITESPACE = re.compile(r"\s+")

    # همزة قطع بعد "ال" التعريف (أخطاء شائعة في مصادر وأفعال خماسية وسداسية)
    # This targets specific structural prefixes that should have hamzat wasl,
    # avoiding false positives on correct words like الأمر, الإنسان.
    # Matches words starting with: الإست، الإخت، الإجت، الإنت، الإشت، الإفت، الإنف، الإكت
    HAMZAT_QAT_SUSPICIOUS = re.compile(r"^الإ(ست|خت|جت|نت|شت|فت|نف|كت)")

    # للتوحيد — كل واحد منفصل عشان يبقى واضح
    ALIF_VARIANTS = re.compile(r"[إأآٱ]")
    YAA_VARIANTS = re.compile(r"[ىي]")
    TAA_MARBUTA = re.compile(r"ة")
    HAMZA_WAW = re.compile(r"ؤ")
    HAMZA_YAA = re.compile(r"ئ")
