"""Example: Clean an entire Arabic text dataset.

This script demonstrates how to use ArabCheck to preprocess a large
collection of Arabic texts for NLP training pipelines.

Run:
    python examples/clean_dataset.py
"""

from arabcheck import ArabCheck


# Sample dataset — replace with your own data source
SAMPLE_DATASET = [
    "العَرَبِيَّةُ لُغَةٌ جَمِيلَةٌ وَغَنِيَّةٌ",
    "مَــرحبــاً بِكُم فِي العَالَمِ العَرَبِيِّ",
    "الذَّكَاءُ الاصْطِنَاعِيُّ يُغَيِّرُ العَالَمَ",
    "النَّصُّ العَرَبِيُّ يَحتَاجُ إِلَى مُعَالَجَةٍ خَاصَّةٍ",
]


def preprocess_dataset(texts: list[str]) -> list[str]:
    """Clean and normalize a list of Arabic texts.

    Args:
        texts: List of raw Arabic texts.

    Returns:
        List of cleaned texts ready for NLP training.
    """
    checker = ArabCheck()
    cleaned = []

    for raw in texts:
        # Step 1: Remove diacritics, tatweel, normalize whitespace
        text = checker.clean_text(raw)

        # Step 2: Normalize character variants (for NLP consistency)
        # NOTE: This loses some linguistic info — use with care
        text = checker.normalize(text)

        cleaned.append(text)

    return cleaned


def audit_dataset(texts: list[str]) -> None:
    """Print all spelling issues found in the dataset."""
    checker = ArabCheck()

    print("\n🔍 Auditing dataset...")
    total_issues = 0

    for i, text in enumerate(texts, start=1):
        issues = checker.audit(text)
        if issues:
            print(f"\n  Line {i}: {text}")
            for issue in issues:
                print(f"    ⚠️  {issue['message']}")
            total_issues += len(issues)

    if total_issues == 0:
        print("  ✅ No issues found!")
    else:
        print(f"\n  📊 Total issues: {total_issues}")


if __name__ == "__main__":
    print("=" * 60)
    print("📚 ArabCheck — Dataset Cleaning Example")
    print("=" * 60)

    # Show original
    print("\n📥 Original dataset:")
    for text in SAMPLE_DATASET:
        print(f"  • {text}")

    # Audit
    audit_dataset(SAMPLE_DATASET)

    # Clean
    print("\n" + "=" * 60)
    print("🧹 Cleaning dataset...")
    print("=" * 60)

    cleaned = preprocess_dataset(SAMPLE_DATASET)

    print("\n📤 Cleaned dataset:")
    for text in cleaned:
        print(f"  • {text}")

    print("\n" + "=" * 60)
    print(f"✅ Done! Cleaned {len(cleaned)} texts.")
    print("=" * 60)
