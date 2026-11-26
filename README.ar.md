# ArabCheck 🔍

> أداة Python خفيفة ومفتوحة المصدر لتنظيف النصوص العربية وتوحيدها وفحص جودتها ضمن سير عمل الذكاء الاصطناعي ومعالجة اللغة الطبيعية.

[English Version →](README.md)

[![PyPI - الإصدار](https://img.shields.io/pypi/v/arabcheck)](https://pypi.org/project/arabcheck/)
[![PyPI - إصدار بايثون](https://img.shields.io/pypi/pyversions/arabcheck)](https://pypi.org/project/arabcheck/)
[![CI](https://img.shields.io/github/actions/workflow/status/MOHAMEDKAMALSALLIH/arabcheck/ci.yml?label=CI)](https://github.com/MOHAMEDKAMALSALLIH/arabcheck/actions)
[![نجوم GitHub](https://img.shields.io/github/stars/MOHAMEDKAMALSALLIH/arabcheck)](https://github.com/MOHAMEDKAMALSALLIH/arabcheck/stargazers)
[![الترخيص: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

---

## لماذا ArabCheck؟

قد تحتوي النصوص العربية، خصوصاً مجموعات البيانات، على مشكلات تؤثر في تجهيزها لمعالجة اللغة الطبيعية:

- اختلافات Unicode واختلاف صور الحروف.
- التشكيل والعلامات القرآنية والكشيدة.
- المحارف المخفية ومحارف التحكم.
- المسافات الزائدة وتفاوت التنسيق.

يوفر ArabCheck أدوات لتنظيف النص وتوحيده، إلى جانب فحوصات تعتمد على قواعد. نتائج الفحص تنبّه إلى حالات تحتاج مراجعة بشرية؛ ولا تعيد كتابة النص تلقائياً.

## الميزات

- **إزالة التشكيل** — الحركات والعلامات القرآنية المدعومة.
- **إزالة الكشيدة** — أحرف المدّ الزخرفية.
- **تنظيف النص** — تنظيم المسافات البيضاء.
- **توحيد الحروف** — صور الألف والياء والهمزة، والتاء المربوطة اختيارياً.
- **كشف المحارف الخفية** — بعض محارف المسافة الصفرية والاتجاه ثنائي الاتجاه (Bidi) ومحارف التحكم غير المرئية.
- **الفحص بالقواعد** — القواعد المتاحة حالياً: `hamzat_qat` و`invisible`.
- **دعم الملفات وstdin**.
- **مخرجات JSON** للتشغيل الآلي.
- **قابلية التوسع** عبر واجهة قواعد موحدة.

## التثبيت

من PyPI:

```bash
pip install arabcheck
```

من المصدر:

```bash
git clone https://github.com/MOHAMEDKAMALSALLIH/arabcheck.git
cd arabcheck
pip install -e .
```

المتطلبات: Python 3.8 أو أحدث، ولا توجد اعتماديات تشغيل خارجية.

**ملاحظة حول الإصدار:** الإصدار المتاح حالياً على PyPI هو ArabCheck 0.1.1. أما الأمر `arabcheck scan` وقاعدة `invisible` المعيارية الموضحان أدناه فهما ضمن نسخة التطوير 0.2.0 التي لم تُنشر بعد على PyPI. لاستخدامهما قبل نشر الحزمة 0.2.0، ثبّت المشروع من المصدر باتباع التعليمات أعلاه.

## الاستخدام السريع

```bash
arabcheck "النَّصُّ العَرَبِيُّ لِلتَّجْرِبَة" --clean
```

الناتج:

```text
النص العربي للتجربة
```

## أمثلة الاستخدام

### 1. تنظيف النص

```bash
arabcheck "العَرَبِيَّةُ ـــ لُغَةٌ جَمِيلَةٌ" --clean
# العربية لغة جميلة
```

### 2. توحيد الحروف

```bash
arabcheck "أحمد إبراهيم آمن" --normalize
# احمد ابراهيم امن
```

**تنبيه:** توحيد الحروف قد يفقد معلومات لغوية؛ استخدمه فقط عندما يكون هذا الفقد مناسباً لغرض البحث أو الفهرسة أو تجهيز البيانات.

### 3. تشغيل محرك الفحص

عند عدم تمرير `--rules`، يشغّل الأمر `arabcheck scan` القاعدتين المسجلتين افتراضياً: `hamzat_qat` و`invisible`.

```bash
arabcheck scan "الإستخدام"
```

لتحديد قاعدة الهمزة وحدها:

```bash
arabcheck scan "الإستخدام" --rules hamzat_qat
```

ولاختبار قاعدة `invisible`، يجب أن يحتوي النص على محرف مخفي فعلي. المثال التالي خاص بـ Bash ويُدرج محرف U+200B ZERO WIDTH SPACE:

```bash
# Bash
arabcheck scan $'نص\u200bمخفي' --rules invisible
```

ترصد قاعدة `hamzat_qat` مجموعة محددة من الصيغ المشتبه فيها، وتصدر تحذيرات للمراجعة البشرية. التحذير ليس تصحيحاً مؤكداً؛ فمثلاً تقترح القاعدة صيغة بديلة لكلمة `الإستخدام`.

أما قاعدة `invisible` فترصد محارف مخفية أو تحكمية محددة، منها U+200B ZERO WIDTH SPACE وU+FEFF BOM. لا تحذف القاعدة هذه المحارف ولا تعدّل النص. وجود نتيجة واحدة أو أكثر يجعل أمر الفحص يعيد رمز الخروج `1`.

ملف UTF-8 المحفوظ مع BOM يبدأ بالمحرف U+FEFF. ترصد قاعدة `invisible` علامة BOM الموجودة في بداية الملف، ويعيد الأمر `arabcheck scan --file file.txt` رمز الخروج `1` إذا كانت هي المشكلة الوحيدة المكتشفة.

### 4. مخرجات JSON

شغّل الأمر:

```bash
arabcheck scan "الإستخدام" --rules hamzat_qat --json
```

تتضمن وثيقة JSON الحقول `input` و`issues` و`meta`. المثال التالي توضيحي ومختصر لبنية نتيجة قاعدة الهمزة؛ أما القيم والرسائل الدقيقة فتنتجها القاعدة عند التشغيل:

```json
{
  "input": "الإستخدام",
  "issues": [
    {
      "rule": "hamzat_qat",
      "type": "hamzat_qat",
      "severity": "warning",
      "word": "الإستخدام",
      "intended": "الاستخدام",
      "position": 1,
      "location": {"word": 1},
      "message": "..."
    }
  ],
  "meta": {
    "rules": ["hamzat_qat"],
    "version": "0.2.0"
  }
}
```

تتضمن نتيجة قاعدة `invisible` أيضاً رمز المحرف واسمه في Unicode وتفاصيل موقعه: `word` و`line` و`column` و`offset`. وقد تكون قيمة `position` و`location.word` هي `null` عندما لا يرتبط المحرف بكلمة.

### 5. الفحص القديم ومحرك Scanner الجديد

ما زال الخيار القديم `--audit` متاحاً في الأمر الرئيسي:

```bash
arabcheck "الإستخدام" --audit
```

وهو يستدعي واجهة `ArabCheck.audit()` القديمة التي تستخدم قاعدة `hamzat_qat`. أما الأمر الأحدث `arabcheck scan` فيستخدم واجهة `Scanner` المعيارية ويشغّل القواعد المسجلة (`hamzat_qat` و`invisible` افتراضياً). استخدم `scan` عندما تريد اختيار القواعد المعيارية بواسطة `--rules`؛ فهو، بخلاف الفحص القديم، يستطيع أيضاً رصد المحارف الخفية.

### 6. القراءة من ملف أو stdin

```bash
arabcheck --file dataset.txt --clean
cat article.txt | arabcheck --clean
```

ويدعم أمر الفحص أيضاً القراءة من ملف أو stdin:

```bash
arabcheck scan --file dataset.txt
cat article.txt | arabcheck scan
```

## مرجع أوامر CLI

### الأمر الرئيسي

```text
arabcheck [-h] [-f FILE] [-c] [-n] [-a] [-j] [-q] [-V] [text]
```

| الخيار | الوصف |
|---|---|
| `-h, --help` | عرض المساعدة |
| `-f, --file FILE` | القراءة من ملف UTF-8 |
| `-c, --clean` | إزالة التشكيل والكشيدة والمسافات الزائدة |
| `-n, --normalize` | توحيد صور الحروف المدعومة |
| `-a, --audit` | تشغيل الفحص الإملائي القديم |
| `-j, --json` | إخراج JSON |
| `-q, --quiet` | إخفاء النص المعالَج |
| `-V, --version` | عرض إصدار الحزمة |

### أمر scan

```text
arabcheck scan [-h] [-f FILE] [--rules RULES] [-j] [-q] [text]
```

| الخيار | الوصف |
|---|---|
| `-h, --help` | عرض المساعدة |
| `-f, --file FILE` | القراءة من ملف UTF-8 |
| `--rules RULES` | أسماء القواعد مفصولة بفواصل |
| `-j, --json` | إخراج JSON |
| `-q, --quiet` | إخفاء النص الأصلي |

### رموز الخروج

| الرمز | المعنى |
|:---:|---|
| `0` | لم تُرصد مشكلات |
| `1` | رُصدت مشكلة واحدة أو أكثر |
| `2` | مدخلات أو وسائط غير صحيحة |

## الاستخدام كمكتبة Python

استخدم دوال `ArabCheck` القديمة لتنظيف النص وتوحيده وإجراء الفحص القديم:

```python
from arabcheck import ArabCheck

checker = ArabCheck()

cleaned = checker.clean_text("النَّصُّ العَرَبِيُّ ـــ")
print(cleaned)  # النص العربي

normalized = checker.normalize("أحمد إبراهيم")
print(normalized)  # احمد ابراهيم

issues = checker.audit("الإستخدام")
for issue in issues:
    print(issue["message"])
```

أما محرك الفحص المعياري فيُستدعى من وحدته. وتستقبل `Scanner` حالياً كائنات قواعد، وليس أسماء القواعد كنصوص:

```python
from arabcheck.scanner import Scanner
from arabcheck.rules.hamza import HamzatQatRule
from arabcheck.rules.invisible import InvisibleRule

scanner = Scanner(rules=[HamzatQatRule(), InvisibleRule()])
issues = scanner.scan("نص للإستخدام")
for issue in issues:
    print(issue["rule"], issue["message"])
```

## الأمثلة

توجد سكربتات عملية في مجلد [`examples/`](examples/):

- [`clean_dataset.py`](examples/clean_dataset.py) — تنظيف مجموعة بيانات عربية.
- [`preprocess_for_ai.py`](examples/preprocess_for_ai.py) — تجهيز النصوص لسير عمل الذكاء الاصطناعي.

لتشغيلها من المجلد الرئيسي للمشروع:

```bash
python examples/clean_dataset.py
python examples/preprocess_for_ai.py
```

## الاختبارات

ثبّت اعتماديات التطوير ثم شغّل الاختبارات:

```bash
pip install -e ".[dev]"
pytest
```

## خارطة الطريق

المشروع قيد التطوير. وتشمل المراحل السبع الأصلية قواعد إضافية لجودة النص العربي، والإصلاح الاختياري الآمن، وفحص مجموعات البيانات، وكشف التكرار، وإحصائيات جودة النص. راجع [`ROADMAP.md`](ROADMAP.md) لمعرفة حالة التنفيذ والخطة الكاملة.

## المساهمة

المساهمات والاقتراحات وبلاغات الأخطاء مرحّب بها. راجع [`CONTRIBUTING.md`](CONTRIBUTING.md).

## الإصدارات

راجع [إصدارات GitHub](https://github.com/MOHAMEDKAMALSALLIH/arabcheck/releases) و[صفحة PyPI](https://pypi.org/project/arabcheck/).

## الترخيص

MIT — راجع [`LICENSE`](LICENSE).
