# Text Summarization API

API لتلخيص النصوص باللغتين العربية والإنجليزية باستخدام نماذج الذكاء الاصطناعي.

## التثبيت

1. قم بتثبيت المتطلبات الأساسية:
```bash
pip install fastapi uvicorn pydantic
```

2. قم بتثبيت مكتبات التعلم الآلي (قد يستغرق وقتاً):
```bash
pip install transformers torch nltk pandas scikit-learn rouge-score bert-score
```

## التشغيل

```bash
uvicorn main:app --reload
```

سيتم تشغيل الـ API على `http://127.0.0.1:8000`

## الاستخدام

### تلخيص نص عربي
```bash
curl -X POST "http://127.0.0.1:8000/summarize" \
     -H "Content-Type: application/json" \
     -d '{"text": "النص العربي هنا", "language": "ar"}'
```

### تلخيص نص إنجليزي
```bash
curl -X POST "http://127.0.0.1:8000/summarize" \
     -H "Content-Type: application/json" \
     -d '{"text": "English text here", "language": "en"}'
```

## الواجهات

- `GET /` - معلومات عن الـ API
- `GET /health` - فحص حالة الـ API
- `POST /summarize` - تلخيص النص

## النماذج المستخدمة

- **العربية**: mT5_multilingual_XLSum
- **الإنجليزية**: BART-large-CNN

## ملاحظات

- النماذج يتم تحميلها عند الاستخدام الأول (lazy loading)
- قد يستغرق التلخيص الأول وقتاً بسبب تحميل النموذج
- تأكد من تثبيت جميع المتطلبات قبل الاستخدام