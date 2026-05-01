# 🚀 خطوات النشر على Railway

دليل خطوة بخطوة لنشر API التلخيص على منصة Railway

## المتطلبات ✅

- ✓ حساب GitHub
- ✓ حساب Railway
- ✓ مفاتيح Azure Services
- ✓ المستودع مدفوع على GitHub

---

## الخطوة 1️⃣: إعداد مستودع GitHub

### 1.1 انسخ الملفات إلى مستودع جديد

```bash
# انشئ مستودع جديد على GitHub
# ثم انسخ الملفات التالية:
- main.py
- requirements.txt
- .env.example
- .gitignore
- Dockerfile
- docker-compose.yml
- Procfile
- railway.json
- README.md
- DEPLOYMENT.md
- test_api.py
```

### 1.2 ادفع الملفات
```bash
git add .
git commit -m "Initial commit: Summarization API"
git push origin main
```

**⚠️ تحذير:** لا تدفع ملف `.env` - قم بإضافته إلى `.gitignore`

---

## الخطوة 2️⃣: إنشاء حساب Railway

1. اذهب إلى [railway.app](https://railway.app)
2. اضغط **Sign Up** أو **Sign In**
3. اختر **GitHub** للمصادقة بسهولة
4. اسمح لـ Railway بالوصول إلى حسابك على GitHub

---

## الخطوة 3️⃣: إنشاء مشروع جديد

### في لوحة تحكم Railway:

1. اضغط **+ New Project**
2. اختر **Deploy from GitHub repo**
3. ابحث عن مستودعك الخاص بالـ API
4. اختر **import** (استيراد)

Railway سيبدأ البناء والنشر تلقائياً ✨

---

## الخطوة 4️⃣: إضافة متغيرات البيئة

في لوحة تحكم Railway:

1. اذهب إلى تبويب **Variables**
2. أضف المتغيرات التالية:

```env
AZURE_SPEECH_KEY=your_azure_speech_key_here
AZURE_SPEECH_REGION=francecentral
AZURE_LANGUAGE_KEY=your_azure_text_analytics_key
AZURE_LANGUAGE_ENDPOINT=https://your-resource.cognitiveservices.azure.com/
TRANSLATOR_KEY=your_azure_translator_key
TRANSLATOR_REGION=francecentral
PORT=8000
```

### كيفية الحصول على هذه المفاتيح:

#### 🔑 Azure Speech Key
```
Azure Portal → Speech Services → Keys and Endpoint
```

#### 🔑 Azure Language Key
```
Azure Portal → Text Analytics → Keys and Endpoint
```

#### 🔑 Azure Translator Key
```
Azure Portal → Translator Service → Keys and Endpoint
```

---

## الخطوة 5️⃣: التحقق من النشر

### في لوحة تحكم Railway:

1. اذهب إلى تبويب **Logs** لمشاهدة السجلات
2. ابحث عن:
   ```
   INFO:     Uvicorn running on http://0.0.0.0:8000
   ```

### الحصول على رابط الخادم:

1. في **Railway Dashboard**
2. اضغط على **Generate Domain**
3. سيظهر رابطك:
   ```
   https://your-project-name.up.railway.app
   ```

---

## الخطوة 6️⃣: اختبار الـ API

### اختبر الصحة:
```bash
curl https://your-project-name.up.railway.app/health
```

### جرب الـ API:
```bash
curl -X POST "https://your-project-name.up.railway.app/summarize" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://youtu.be/YOUR_VIDEO_ID"}'
```

### عرض الوثائق التفاعلية:
```
https://your-project-name.up.railway.app/docs
```

---

## الخطوة 7️⃣: النشر المستمر (CI/CD)

Railway ينشر تلقائياً عند دفع تغييرات إلى GitHub:

```bash
# عندما تقوم بـ push
git push origin main

# Railway يكتشف التغيير تلقائياً ويعيد البناء والنشر ✨
```

يمكنك مشاهدة حالة الـ Build في **Deployments** tab

---

## استكشاف الأخطاء 🔧

### خطأ: Build Failed

**الحل:**
1. اذهب إلى **Logs**
2. ابحث عن الخطأ الفعلي
3. تأكد من أن كل الملفات موجودة بشكل صحيح
4. تحقق من `requirements.txt`

### خطأ: Application Error / Server Error

**الحل:**
1. تأكد من جميع متغيرات البيئة مضافة بشكل صحيح
2. جرب: `curl https://your-domain/health`
3. اقرأ الـ logs في Railway

### خطأ: "Azure credentials not configured"

**الحل:**
```
عد إلى الخطوة 4️⃣ وتأكد من إضافة جميع المفاتيح بشكل صحيح
```

### المعالجة بطيئة جداً

**الحل:**
- قد تحتاج لترقية خطة Railway
- Summarization يأخذ وقت (اعتماداً على طول الفيديو)
- جرب مقطع فيديو أقصر في الاختبار

---

## الخطوات التالية 🎯

### تحسينات مقترحة:

1. **إضافة مصادقة API**
   ```python
   from fastapi.security import HTTPBearer
   security = HTTPBearer()
   ```

2. **إضافة قاعدة بيانات**
   ```python
   # حفظ النتائج في PostgreSQL أو MongoDB
   ```

3. **تحديد المعدل (Rate Limiting)**
   ```python
   from slowapi import Limiter
   ```

4. **التكامل مع Sentry للأخطاء**
   ```python
   import sentry_sdk
   ```

5. **إضافة WebSocket للتحديثات الحية**
   ```python
   @app.websocket("/ws/status/{job_id}")
   ```

---

## الدعم 💬

### المشاكل الشائعة:

| المشكلة | الحل |
|--------|------|
| Timeout | استخدم timeout أطول، أو جرب مقطع أقصر |
| Out of Memory | Railway قد يحتاج خطة أعلى |
| Azure Errors | تحقق من مفاتيح Azure |

### الموارد المفيدة:

- [Railway Docs](https://docs.railway.app/)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Azure Services Docs](https://learn.microsoft.com/en-us/azure/)

---

## ✅ القائمة النهائية

- [ ] مستودع GitHub جاهز
- [ ] حساب Railway مُنشأ
- [ ] المتغيرات البيئية مضافة
- [ ] البناء نجح بدون أخطاء
- [ ] الـ API مستجيب
- [ ] الفيديو يجري معالجته بنجاح

**مبروك! 🎉 تطبيقك الآن مباشر على الإنترنت!**
