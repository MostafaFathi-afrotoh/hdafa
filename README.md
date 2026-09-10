# HDAFA — Hyper-Deterministic Atomic Agentic Architecture

> **مصنع برمجيات ذاتي من وكلاء AI متخصصين، مع تحقق حتمي.**

## 🎯 الفكرة

HDAFA معمارية لبناء أنظمة إنتاج برمجي تعتمد على وكلاء ذكاء اصطناعي **متخصصين**، يحوّلون وصفاً نصياً إلى مخرجات موثوقة عبر:

1. **تحليل المتطلبات** → JSON Schema
2. **توليد الكود** → HTML/CSS
3. **التحقق الحتمي** → فحوصات آلية (بدون AI)

**الفرضية الأساسية:**
> الهيكل + التحقق الحتمي = مخرجات أكثر موثوقية.

## 🏗️ المكونات

| الوكيل | الوظيفة | المخرج |
|--------|---------|--------|
| **Requirements Analyzer** | تحليل الوصف | JSON Schema |
| **HTML/CSS Coder** | توليد الكود | صفحة HTML |
| **Validator** | 15 فحصاً حتمياً | تقرير PASS/FAIL |

## 🛠️ التقنيات

- Python 3.12
- Gemini API (gemini-3.5-flash-lite)
- Regex + JSON للتحقق الحتمي
- Google Colab

## 📁 الملفات

| الملف | الوصف |
|-------|-------|
| `agent_pipeline.py` | كود الوكلاء الثلاثة |
| `hdafa_coffee.html` | مثال: صفحة متجر |
| `hdafa_clothing.html` | مثال: متجر ملابس |
| `hdafa_restaurant.html` | مثال: صفحة مطعم |

## 🚀 كيف تشغّله؟

1. افتح Google Colab
2. ثبّت: `pip install google-generativeai`
3. أضف `GEMINI_API_KEY` في Secrets
4. شغّل `agent_pipeline.py`

## 📊 نماذج النتائج

ثلاث صفحات مُنتَجة بواسطة HDAFA:
- **hdafa_coffee.html** — متجر إلكتروني (15/15 فحصاً)
- **hdafa_clothing.html** — متجر ملابس (16/16 فحصاً)
- **hdafa_restaurant.html** — صفحة مطعم (15/15 فحصاً)

افتح أي منها في المتصفح لرؤية النتيجة.

## 📚 الفلسفة

HDAFA يتبنى 6 مبادئ:

1. **الذريّة المفرطة** — كل وكيل له مهمة واحدة
2. **الحتمية الخارجية** — التحقق آلي، وليس رأياً
3. **الوكلاء المؤقتون** — لا حالة مشتركة
4. **التحقق المغلق** — لا شيء يمر بدون فحص
5. **التخصص الديناميكي** — وكيل مخصص لكل مهمة
6. **الفصل الطبقي للذكاء** — نماذج مختلفة لطبقات مختلفة

## 📈 خارطة الطريق

- [x] **المرحلة 1:** 3 وكلاء (Analyzer + Coder + Validator)
- [x] **المرحلة 2:** Zero-Defect Protocol (15 فحصاً)
- [ ] **المرحلة 3:** 5 وكلاء (إضافة JS + Docs)
- [ ] **المرحلة 4:** Message Bus + Strict Contracts
- [ ] **المرحلة 5:** النشر كـ API

## 👤 المؤلف

**Mustafa Fathy AbdelTawab Youssef**

- Microbiology Graduate — Al-Azhar University
- Embedded Systems & Bio-Instrumentation
- Multi-Agent AI Systems

📧 afracosh12@gmail.com
🔗 [LinkedIn](https://linkedin.com/in/mustafa-fathy-abdeltawab-438b09305)

## 📜 الرخصة

MIT License — Copyright (c) 2026 Mustafa Fathy