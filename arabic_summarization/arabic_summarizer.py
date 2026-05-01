import re
import pandas as pd
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

class ArabicSummarizer:
    def __init__(self):
        self.model_name = "csebuetnlp/mT5_multilingual_XLSum"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(self.model_name)

    def clean_arabic_text(self, text):
        if not text:
            return ""
        text = str(text)

        # إزالة التشكيل
        text = re.sub(r'[\u064B-\u0652]', '', text)

        # توحيد الحروف
        text = re.sub("[إأآا]", "ا", text)
        text = re.sub("ى", "ي", text)
        text = re.sub("ة", "ه", text)

        # إزالة الرموز
        text = re.sub(r'[^\w\s]', '', text)

        # إزالة المسافات الزائدة
        text = re.sub(r'\s+', ' ', text).strip()

        return text

    def summarize(self, text, max_length=120, min_length=20):
        cleaned_text = self.clean_arabic_text(text)
        input_text = "summarize: " + cleaned_text

        inputs = self.tokenizer(
            input_text,
            return_tensors="pt",
            truncation=True,
            max_length=512
        )

        summary_ids = self.model.generate(
            inputs["input_ids"],
            max_length=max_length,
            min_length=min_length,
            num_beams=4,
            length_penalty=2.0,
            early_stopping=True
        )

        summary = self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        return summary