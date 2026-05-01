# Video Summarization API

API محترفة لتلخيص مقاطع فيديو YouTube باستخدام FastAPI و Azure Services.

## المميزات ✨

- 📥 تحميل مقاطع فيديو من YouTube تلقائياً
- 🎧 استخراج الصوت من الفيديو
- 🧠 تحويل الكلام العربي إلى نص باستخدام Azure Speech-to-Text
- 🌍 ترجمة النص إلى الإنجليزية
- ✍️ تلخيص النص الطويل باستخدام Azure Text Analytics
- 🔁 ترجمة الملخص مرة أخرى إلى العربية
- ⚙️ معالجة خلفية بدون حجب الـ API
- 📊 نظام تتبع حالة الوظائف

## المتطلبات 📋

- Python 3.8+
- حسابات Azure:
  - Azure Speech Services (للتحويل من كلام إلى نص)
  - Azure Text Analytics (للتلخيص)
  - Azure Translator (للترجمة)

## التثبيت المحلي 🖥️

### 1. استنساخ المستودع
```bash
git clone <your-repo-url>
cd summerization
```

### 2. إنشاء بيئة افتراضية
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. تثبيت المتطلبات
```bash
pip install -r requirements.txt
```

### 4. إعداد متغيرات البيئة
```bash
# انسخ الملف النموذجي
cp .env.example .env

# عدّل .env وأضف مفاتيح Azure الخاصة بك
# AZURE_SPEECH_KEY=your_key_here
# AZURE_LANGUAGE_KEY=your_key_here
# TRANSLATOR_KEY=your_key_here
```

### 5. تشغيل الخادم محلياً
```bash
python main.py
```

الخادم سيعمل على: `http://localhost:8000`

## استخدام الـ API 🚀

### الوثائق التفاعلية
بعد تشغيل الخادم، زر:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### مثال على الاستخدام

#### 1. إرسال فيديو للتلخيص
```bash
curl -X POST "http://localhost:8000/summarize" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://youtu.be/YOUR_VIDEO_ID"}'
```

**الرد:**
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "pending"
}
```

#### 2. التحقق من حالة الوظيفة
```bash
curl "http://localhost:8000/status/550e8400-e29b-41d4-a716-446655440000"
```

**الرد (أثناء المعالجة):**
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "transcribing",
  "transcript": null,
  "summary_ar": null,
  "error": null
}
```

**الرد (بعد الانتهاء):**
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "completed",
  "transcript": "النص المفرغ من الفيديو...",
  "summary_ar": "ملخص الفيديو بالعربية...",
  "error": null
}
```

### حالات المعالجة 📊

| الحالة | الوصف |
|--------|-------|
| `pending` | في انتظار البدء |
| `downloading` | جاري تحميل الفيديو |
| `extracting_audio` | جاري استخراج الصوت |
| `transcribing` | جاري تحويل الكلام إلى نص |
| `translating_to_english` | جاري الترجمة للإنجليزية |
| `summarizing` | جاري تلخيص النص |
| `translating_summary` | جاري ترجمة الملخص |
| `completed` | انتهت المعالجة بنجاح ✅ |
| `failed` | حدث خطأ ❌ |

## النشر على Railway 🚀

### الخطوة 1: إعداد حسابك على Railway
1. اذهب إلى [railway.app](https://railway.app)
2. سجل الدخول أو أنشئ حساب جديد
3. اربط حسابك على GitHub

### الخطوة 2: إنشاء مشروع جديد
1. اضغط على "Create New Project"
2. اختر "Deploy from GitHub repo"
3. اختر المستودع الخاص بك

### الخطوة 3: إضافة متغيرات البيئة
1. في لوحة تحكم Railway، اذهب إلى "Variables"
2. أضف المتغيرات التالية:
   ```
   AZURE_SPEECH_KEY=your_key_here
   AZURE_SPEECH_REGION=francecentral
   AZURE_LANGUAGE_KEY=your_key_here
   AZURE_LANGUAGE_ENDPOINT=https://your-resource.cognitiveservices.azure.com/
   TRANSLATOR_KEY=your_key_here
   TRANSLATOR_REGION=francecentral
   ```

### الخطوة 4: النشر التلقائي
- Railway سينشر تلقائياً كلما تدفع تغييرات إلى GitHub
- يمكنك مراقبة الـ logs في لوحة التحكم

### الخطوة 5: الوصول إلى الـ API
```bash
# استبدل YOUR_RAILWAY_URL برابط تطبيقك على Railway
curl -X POST "https://YOUR_RAILWAY_URL/summarize" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://youtu.be/YOUR_VIDEO_ID"}'
```

## الحصول على مفاتيح Azure 🔑

### Azure Speech Services
1. اذهب إلى [Azure Portal](https://portal.azure.com)
2. انشئ "Speech Services" resource
3. انسخ:
   - Subscription Key
   - Region (مثال: `francecentral`)

### Azure Text Analytics
1. انشئ "Text Analytics" resource
2. انسخ:
   - Key
   - Endpoint

### Azure Translator
1. انشئ "Translator" resource
2. انسخ:
   - Subscription Key
   - Region

## الهيكل المشروع 📁

```
summerization/
├── main.py                 # FastAPI Application
├── requirements.txt        # Python Dependencies
├── .env.example           # متغيرات البيئة النموذجية
├── .env                   # متغيرات البيئة الفعلية (لا تنشرها)
├── .gitignore            # ملفات يتم تجاهلها
├── Procfile              # Railway Deployment Config
├── README.md             # هذا الملف
├── transcript.txt        # التفريغ المحفوظ
└── summary.txt          # الملخص المحفوظ
```

## استكشاف الأخطاء 🔧

### "Azure credentials not configured"
تأكد من أنك أضفت جميع متغيرات البيئة المطلوبة في `.env` أو في Railway

### فشل تحميل الفيديو
- تأكد من أن رابط YouTube صحيح
- جرب مقطع فيديو عام (ليس محمياً بكلمة سر)

### خطأ في تحويل الكلام إلى نص
- تأكد من أن الصوت واضح
- جرب مقطع فيديو أقصر

## الحدود والملاحظات ⚠️

- مدة المعالجة تعتمد على طول الفيديو
- قد تستغرق عملية التفريغ وقتاً طويلاً للفيديوهات الطويلة
- تأكد من أن خطتك على Azure تدعم الاستخدام المطلوب

## المساهمة 🤝

لا تتردد في فتح Issues أو Pull Requests!

## الترخيص 📄

MIT License

---

**لاستفسارات أو دعم:** [أرسل رسالة](mailto:your-email@example.com)
