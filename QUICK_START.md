# 🎬 دليل البدء السريع - Summarization API

## ✨ ما تم إنشاؤه

لقد قمت بتحويل كودك إلى API احترافية جاهزة للنشر مع الملفات التالية:

### 📄 الملفات الرئيسية

| الملف | الوصف |
|------|--------|
| `main.py` | تطبيق FastAPI الرئيسي |
| `requirements.txt` | المكتبات المطلوبة |
| `.env.example` | قالب متغيرات البيئة |
| `.gitignore` | الملفات المستثناة من Git |

### 🐳 ملفات Docker

| الملف | الوصف |
|------|--------|
| `Dockerfile` | صورة Docker للتطبيق |
| `docker-compose.yml` | تكوين Docker Compose |

### 📚 ملفات النشر

| الملف | الوصف |
|------|--------|
| `Procfile` | تكوين Railway |
| `railway.json` | إعدادات Railway الإضافية |

### 📖 الوثائق

| الملف | الوصف |
|------|--------|
| `DEPLOYMENT.md` | شرح شامل عن الاستخدام |
| `RAILWAY_DEPLOYMENT.md` | خطوات النشر على Railway بالعربية |
| `QUICK_START.md` | هذا الملف |

### 🧪 الاختبار

| الملف | الوصف |
|------|--------|
| `test_api.py` | سكريبت لاختبار API محليًا |

---

## 🚀 البدء السريع

### للتشغيل المحلي:

```bash
# 1. إنشاء بيئة افتراضية
python -m venv venv
venv\Scripts\activate  # Windows

# 2. تثبيت المتطلبات
pip install -r requirements.txt

# 3. إعداد متغيرات البيئة
cp .env.example .env
# عدّل .env وأضف مفاتيح Azure

# 4. تشغيل الخادم
python main.py

# الخادم سيعمل على: http://localhost:8000
```

### الوثائق التفاعلية:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### اختبار الـ API:

```bash
# في نافذة طرفية جديدة
python test_api.py "https://youtu.be/YOUR_VIDEO_ID"
```

---

## 🌐 النشر على Railway

اتبع الخطوات في `RAILWAY_DEPLOYMENT.md` (بالعربية):

**ملخص سريع:**
1. ادفع الكود إلى GitHub
2. انشئ مشروع جديد في Railway
3. اربط مستودع GitHub
4. أضف متغيرات البيئة (مفاتيح Azure)
5. Railway سينشر تلقائياً

---

## 📝 نقاط مهمة

### الأمان 🔒
- **لا تدفع ملف `.env`** - أضفناه لـ `.gitignore`
- أضف المفاتيح حصراً في بيئة الإنتاج (Railway)

### الأداء ⚡
- المعالجة تتم في الخلفية (Background Tasks)
- API لا تحجب أثناء المعالجة
- استخدم `job_id` للتحقق من الحالة

### المعالجة 🔄
معرّفات الحالات المتاحة:
- `pending` - في الانتظار
- `downloading` - تحميل الفيديو
- `extracting_audio` - استخراج الصوت
- `transcribing` - التفريغ
- `translating_to_english` - الترجمة
- `summarizing` - التلخيص
- `translating_summary` - ترجمة الملخص
- `completed` - انتهت بنجاح ✅
- `failed` - حدث خطأ ❌

---

## 🔑 مفاتيح Azure المطلوبة

يجب أن تحصل على 3 مفاتيح من Azure:

1. **Speech Services** - للتحويل من كلام إلى نص
2. **Text Analytics** - للتلخيص
3. **Translator** - للترجمة

### الحصول على المفاتيح:
1. اذهب إلى [Azure Portal](https://portal.azure.com)
2. انشئ موارد جديدة لكل خدمة
3. انسخ المفاتيح والـ endpoints
4. ضعها في `.env` أو في Railway

---

## 📊 مثال على الاستخدام

### 1. إرسال طلب تلخيص:
```json
POST /summarize
{
  "url": "https://youtu.be/MIRUTjjD5lg"
}

Response:
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "pending"
}
```

### 2. التحقق من الحالة:
```json
GET /status/550e8400-e29b-41d4-a716-446655440000

Response (أثناء المعالجة):
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "transcribing",
  "transcript": null,
  "summary_ar": null,
  "error": null
}

Response (بعد الانتهاء):
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "completed",
  "transcript": "النص المفرغ...",
  "summary_ar": "ملخص الفيديو...",
  "error": null
}
```

---

## 🆘 استكشاف الأخطاء

### API لا تستجيب
```bash
# تحقق من أن الخادم يعمل
curl http://localhost:8000/health

# جرب التشغيل مجدداً
python main.py
```

### خطأ "Azure credentials not configured"
```
تحقق من أن جميع مفاتيح Azure موجودة في .env
```

### فشل معالجة الفيديو
- راجع logs في Railway
- جرب مقطع فيديو أقصر
- تأكد من أن الصوت واضح

---

## 📚 قراءات إضافية

- 📖 [DEPLOYMENT.md](DEPLOYMENT.md) - شرح تفصيلي
- 🚀 [RAILWAY_DEPLOYMENT.md](RAILWAY_DEPLOYMENT.md) - خطوات Railway
- 💻 [FastAPI Docs](https://fastapi.tiangolo.com/)
- ☁️ [Azure Services](https://learn.microsoft.com/en-us/azure/)

---

## ✅ قائمة التحقق

- [ ] تثبيت المتطلبات
- [ ] إعداد مفاتيح Azure
- [ ] تشغيل محلي ناجح
- [ ] اختبار الـ API
- [ ] دفع إلى GitHub
- [ ] إنشاء مشروع Railway
- [ ] إضافة متغيرات البيئة
- [ ] النشر الناجح ✨

---

## 🎉 مبروك!

API الخاصة بك جاهزة! تابع `RAILWAY_DEPLOYMENT.md` للنشر الفوري.

**لأي استفسار، راجع الوثائق أو الـ logs في Railway**
