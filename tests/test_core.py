import pytest
from arabcheck import ArabCheck


@pytest.fixture
def checker():
    return ArabCheck()


def test_strip_tashkeel(checker):
    assert checker.strip_tashkeel("النَّصُّ") == "النص"


def test_strip_tatweel(checker):
    assert checker.strip_tatweel("عـــربي") == "عربي"


def test_clean_text(checker):
    assert checker.clean_text("العَرَبِيَّةُ ـــ   لُغَةٌ") == "العربية لغة"


def test_normalize_alif(checker):
    assert checker.normalize("أحمد إبراهيم آمن") == "احمد ابراهيم امن"


def test_normalize_yaa(checker):
    assert checker.normalize("مصطفى") == "مصطفي"


def test_normalize_taa_marbuta_default(checker):
    assert "ة" in checker.normalize("مدرسة")


def test_normalize_taa_marbuta_enabled(checker):
    assert checker.normalize("مدرسة", taa_marbuta=True) == "مدرسه"


def test_audit_detects_common_spelling_issue(checker):
    issues = checker.audit("الإستخدام")
    assert len(issues) == 1
    assert issues[0]["type"] == "hamzat_qat"
    assert issues[0]["word"] == "الإستخدام"
    assert issues[0]["severity"] == "warning"
    assert issues[0]["intended"] == "الاستخدام"


def test_audit_ignores_valid_words(checker):
    assert checker.audit("الأمر الإنسان الأحمد الكتاب") == []


def test_process_combined(checker):
    result = checker.process("الإستخدام ـــ النَّص", clean=True, audit=True)
    assert result["result"] == "الاستخدام النص"
    assert len(result["issues"]) == 1
