"""Example: Preprocess Arabic text for AI/NLP training pipelines.

This script shows how ArabCheck fits into a typical NLP preprocessing
workflow — from raw text to model-ready input.

Run:
    python examples/preprocess_for_ai.py
"""

from arabcheck import ArabCheck


# Raw text samples (as they often appear in scraped/web data)
RAW_SAMPLES = [
    "الإِعْلَامُ العَرَبِيُّ يَتَطَوَّرُ بِسُرْعَةٍ كَبِيرَةٍ",
    "تِقْنِيَةُ الذَّكَاءِ الاصْطِنَاعِيِّ تُسَاعِدُ فِي فَهْمِ النُّصُوصِ",
    "مَــرحبــاً بِكُم فِي عَالَمِ مُعَالَجَةِ اللُّغَةِ",
    "البَاحِثُونَ يَحتَاجُونَ إِلَى بَيَانَاتٍ نَظِيفَةٍ",
]


def preprocess_for_ai(text: str, checker: ArabCheck) -> str:
    """Full preprocessing pipeline for AI/NLP input.

    Pipeline:
        1. Remove diacritics (tashkeel)
        2. Remove tatweel (kashida)
        3. Normalize whitespace
        4. Normalize character variants (for model consistency)

    Args:
        text: Raw Arabic text.
        checker: ArabCheck instance (reused for efficiency).

    Returns:
        Preprocessed text ready for tokenization.
    """
    # Step 1-3: clean
    text = checker.clean_text(text)

    # Step 4: normalize for consistency
    text = checker.normalize(text)

    return text


def show_pipeline(texts: list[str]) -> None:
    """Print the pipeline transformation for each text."""
    checker = ArabCheck()

    for i, raw in enumerate(texts, start=1):
        cleaned = preprocess_for_ai(raw, checker)

        print(f"\n─── Sample {i} " + "─" * 40)
        print(f"  📥 Raw      : {raw}")
        print(f"  📤 Cleaned  : {cleaned}")
        print(f"  📊 Length   : {len(raw)} → {len(cleaned)} chars")


def make_training_pairs(texts: list[str]) -> list[dict]:
    """Convert raw texts into records ready for model training.

    Returns:
        List of dicts with 'input' (raw) and 'target' (cleaned).
    """
    checker = ArabCheck()
    pairs = []

    for raw in texts:
        pairs.append({
            "input": raw,
            "target": preprocess_for_ai(raw, checker),
        })

    return pairs


if __name__ == "__main__":
    print("=" * 60)
    print("🤖 ArabCheck — AI Preprocessing Example")
    print("=" * 60)

    # Show pipeline steps
    print("\n🔬 Preprocessing pipeline:")
    show_pipeline(RAW_SAMPLES)

    # Prepare training data
    print("\n" + "=" * 60)
    print("📦 Building training pairs...")
    print("=" * 60)

    pairs = make_training_pairs(RAW_SAMPLES)

    for i, pair in enumerate(pairs, start=1):
        print(f"\n  Pair {i}:")
        print(f"    input  = {pair['input']}")
        print(f"    target = {pair['target']}")

    print("\n" + "=" * 60)
    print(f"✅ Ready! Generated {len(pairs)} training pairs.")
    print("=" * 60)
