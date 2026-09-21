# ArabCheck 🔍

> **أداة خفيفة مفتوحة المصدر لتنظيف وتوحيد وفحص النصوص العربية لمعالجة اللغة والذكاء الاصطناعي.**

[![PyPI - الإصدار](https://img.shields.io/pypi/v/arabcheck)](https://pypi.org/project/arabcheck/)
[![PyPI - إصدار بايثون](https://img.shields.io/pypi/pyversions/arabcheck)](https://pypi.org/project/arabcheck/)
[![CI](https://img.shields.io/github/actions/workflow/status/MOHAMEDKAMALSALLIH/arabcheck/ci.yml?label=CI)](https://github.com/MOHAMEDKAMALSALLIH/arabcheck/actions)
[![نجوم GitHub](https://img.shields.io/github/stars/MOHAMEDKAMALSALLIH/arabcheck)](https://github.com/MOHAMEDKAMALSALLIH/arabcheck/stargazers)
[![الترخيص: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

[English Version →](README.md)

---

## 🎯 لماذا ArabCheck؟

النصوص العربية — خاصة في مجموعات البيانات (Datasets) — تحتوي على كثير من الضوضاء التي تُربك خطوط معالجة اللغة (NLP Pipelines):

- **اختلافات Unicode** — `أ` / `إ` / `آ` / `ا` / `ٱ` كلها شكل من أشكال الألف
- **التشكيل (Tashkeel)** — فتحات، ضمات، شدة، تنوين
- **الكشيدة (Tatweel)** — `ـــــ` تُستخدم للتزيين لكنها تُربك التحليل
- **علامات قرآنية** صغيرة ومدّات ورموز وقف
- **مسافات زائدة** وأسطر فارغة

**ArabCheck** يجعل تنظيف وفحص هذه البيانات بأمر واحد — مع شفافية كاملة وعمليات قابلة للتخصيص.

---

## ✨ الميزات

- 🕌 **إزالة التشكيل الكامل** — حركات + علامات قرآنية + ألف خنجرية
- 🔤 **توحيد الحروف** — الألف والياء والهمزة والتاء المربوطة
- 〰️ **إزالة الكشيدة (Tatweel)** — الأحرف التزيينية الممتدة
- 🧹 **تنظيف شامل** — تنظيم المسافات والأسطر
- 🔍 **فحص نحوي** — كشف أخطاء همزات القطع/الوصل الشائعة
- 📂 **دعم الملفات و stdin**
- 🤖 **مخرجات JSON** — مناسبة للـ CI/CD
- 🧩 **قابل للتوسّع** — إضافة قواعد جديدة بسهولة

---

## 📦 التثبيت

### من PyPI (موصى به)

```bash
pip install arabcheck
```

من المصدر

```bash
git clone https://github.com/MOHAMEDKAMALSALLIH/arabcheck.git
cd arabcheck
pip install -e .
```

المتطلبات: Python 3.8+ — بدون اعتماديات خارجية.

---

🚀 الاستخدام السريع

```bash
arabcheck "النَّصُّ العَرَبِيُّ لِلتَّجْرِبَة" --clean
```

المدخل:

```
النَّصُّ العَرَبِيُّ لِلتَّجْرِبَة
```

المخرج:

```
النص العربي للتجربة
```

---

💡 أمثلة

1. تنظيف النص

```bash
arabcheck "العَرَبِيَّةُ ـــ لُغَةٌ جَمِيلَةٌ" --clean
# → العربية لغة جميلة
```

2. توحيد الحروف

```bash
arabcheck "أحمد إبراهيم آمن" --normalize
# → احمد ابراهيم امن
```

⚠️ تحذير: التوحيد يفقد معلومة لغوية. استخدمه فقط للبحث أو الفهرسة أو تحضير بيانات AI.

3. فحص النص

```bash
arabcheck "الأمر بالأمر" --audit
# ⚠️  احتمال خطأ: 'الأمر' تبدأ بـ 'ال' + همزة قطع.
```

4. مخرجات JSON (للتشغيل الآلي)

```bash
arabcheck "النَّصُّ" --clean --json
```

```json
{
  "input": "النَّصُّ",
  "result": "النص",
  "issues": [],
  "meta": {
    "cleaned": true,
    "normalized": false,
    "audited": false,
    "version": "0.1.0"
  }
}
```

5. قراءة من ملف

```bash
arabcheck --file dataset.txt --clean
```

6. من stdin

```bash
cat article.txt | arabcheck --clean
```

---

🛠️ مرجع الـ CLI

```
usage: arabcheck [-h] [-f FILE] [-c] [-n] [-a] [-j] [-q] [-V] [text]

positional arguments:
  text                  النص المراد معالجته

options:
  -h, --help            عرض المساعدة
  -f, --file FILE       قراءة النص من ملف
  -c, --clean           إزالة التشكيل والكشيدة والمسافات الزائدة
  -n, --normalize       توحيد الحروف (يفقد معلومة لغوية!)
  -a, --audit           فحص أخطاء إملائية شائعة
  -j, --json            إخراج النتيجة بصيغة JSON
  -q, --quiet           لا تطبع النص، فقط الأخطاء
  -V, --version         عرض الإصدار
```

أكواد الخروج (Exit Codes)

الكود المعنى
0 نجاح، لا توجد مشاكل
1 توجد مشاكل إملائية (مع --audit)
2 خطأ في المدخلات

---

🐍 الاستخدام كمكتبة

```python
from arabcheck import ArabCheck

checker = ArabCheck()

# تنظيف
text = checker.clean_text("النَّصُّ العَرَبِيُّ ـــ")
print(text)  # → النص العربي

# توحيد
print(checker.normalize("أحمد إبراهيم"))
# → احمد ابراهيم

# فحص
issues = checker.audit("الأمر بالأمر")
for issue in issues:
    print(issue["message"])
```

---

🧪 الاختبارات

```bash
pip install -e ".[dev]"
pytest
```

22 اختبار يغطون الـ core والـ CLI بالكامل ✅

---

🗺️ خارطة الطريق

☑ إزالة التشكيل والكشيدة
☑ توحيد الحروف
☑ دعم الملفات و stdin
☑ مخرجات JSON
☑ أكواد خروج صحيحة
☑ فحص همزات القطع/الوصل
☐ قواعد فحص موسّعة (تاء مربوطة، تنوين)
☐ تحميل Datasets (CSV, JSONL)
☐ كشف التكرار
☐ إحصائيات جودة النص

---

🤝 المساهمة

المساهمات والاقتراحات وبلاغات الأخطاء مرحّب بها! راجع CONTRIBUTING.md.

---

🏷️ الإصدارات

راجع الإصدارات لسجل النسخ.

---

📄 الترخيص

هذا المشروع مرخّص تحت MIT — راجع LICENSE للتفاصيل.

---

<p align="center">
  صُنع بـ ❤️ لمجتمع NLP العربي
</p>
```

---
