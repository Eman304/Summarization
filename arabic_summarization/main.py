from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Text Summarization API", description="API for Arabic and English text summarization")

# Lazy loading of summarizers
arabic_summarizer = None
english_summarizer = None

def get_arabic_summarizer():
    global arabic_summarizer
    if arabic_summarizer is None:
        from arabic_summarizer import ArabicSummarizer
        arabic_summarizer = ArabicSummarizer()
    return arabic_summarizer

def get_english_summarizer():
    global english_summarizer
    if english_summarizer is None:
        from english_summarizer import EnglishSummarizer
        english_summarizer = EnglishSummarizer()
    return english_summarizer

class SummarizeRequest(BaseModel):
    text: str
    language: str  # "ar" or "en"

@app.post("/summarize")
async def summarize_text(request: SummarizeRequest):
    try:
        if request.language == "ar":
            summarizer = get_arabic_summarizer()
            summary = summarizer.summarize(request.text)
        elif request.language == "en":
            summarizer = get_english_summarizer()
            summary = summarizer.summarize(request.text)
        else:
            raise HTTPException(status_code=400, detail="Unsupported language. Use 'ar' or 'en'")

        return {"summary": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "Text Summarization API", "languages": ["ar", "en"]}

@app.get("/health")
async def health():
    return {"status": "ok"}