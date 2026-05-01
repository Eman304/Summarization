from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
import yt_dlp
from moviepy.editor import VideoFileClip
import azure.cognitiveservices.speech as speechsdk
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
import requests
import time
import os
import uvicorn
from dotenv import load_dotenv
import tempfile
import uuid

load_dotenv()

# ============ CONFIGURATION ============
AZURE_SPEECH_KEY = os.getenv("AZURE_SPEECH_KEY")
AZURE_SPEECH_REGION = os.getenv("AZURE_SPEECH_REGION", "francecentral")
AZURE_LANGUAGE_KEY = os.getenv("AZURE_LANGUAGE_KEY")
AZURE_LANGUAGE_ENDPOINT = os.getenv("AZURE_LANGUAGE_ENDPOINT")
TRANSLATOR_KEY = os.getenv("TRANSLATOR_KEY")
TRANSLATOR_ENDPOINT = os.getenv("TRANSLATOR_ENDPOINT", "https://api.cognitive.microsofttranslator.com")
TRANSLATOR_REGION = os.getenv("TRANSLATOR_REGION", "francecentral")

# Create temp directory for processing
TEMP_DIR = tempfile.gettempdir()
JOBS = {}

# ============ MODELS ============
class VideoRequest(BaseModel):
    url: str

class SummaryResponse(BaseModel):
    job_id: str
    status: str
    transcript: Optional[str] = None
    summary_ar: Optional[str] = None
    error: Optional[str] = None

class JobStatusResponse(BaseModel):
    job_id: str
    status: str
    transcript: Optional[str] = None
    summary_ar: Optional[str] = None
    error: Optional[str] = None

# ============ FASTAPI APP ============
app = FastAPI(title="Summarization API", version="1.0.0")

@app.get("/")
async def read_root():
    return {
        "message": "Welcome to Summarization API",
        "endpoints": {
            "POST /summarize": "Submit a video URL for summarization",
            "GET /status/{job_id}": "Check the status of a summarization job"
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "ok"}

# ============ HELPER FUNCTIONS ============
def download_video(url, output_path):
    """Download video from YouTube"""
    ydl_opts = {
        'outtmpl': output_path,
        'format': 'best',
        'quiet': False,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0'
        }
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def extract_audio(video_path, audio_path):
    """Extract audio from video"""
    try:
        video = VideoFileClip(video_path)
        video.audio.write_audiofile(audio_path, fps=16000, codec='pcm_s16le', verbose=False, logger=None)
        video.close()
    except Exception as e:
        raise Exception(f"Failed to extract audio: {str(e)}")

def speech_to_text_long(audio_file):
    """Convert speech to text using Azure Cognitive Services"""
    try:
        speech_config = speechsdk.SpeechConfig(
            subscription=AZURE_SPEECH_KEY,
            region=AZURE_SPEECH_REGION
        )
        speech_config.speech_recognition_language = "ar-EG"
        
        audio_config = speechsdk.audio.AudioConfig(filename=audio_file)
        recognizer = speechsdk.SpeechRecognizer(
            speech_config=speech_config,
            audio_config=audio_config
        )
        
        all_text = []
        done = False
        
        def handle_result(evt):
            if evt.result.text:
                all_text.append(evt.result.text)
        
        def stop(evt):
            nonlocal done
            done = True
        
        recognizer.recognized.connect(handle_result)
        recognizer.session_stopped.connect(stop)
        recognizer.canceled.connect(stop)
        
        recognizer.start_continuous_recognition()
        
        while not done:
            time.sleep(0.5)
        
        recognizer.stop_continuous_recognition()
        
        return " ".join(all_text)
    except Exception as e:
        raise Exception(f"Speech to text failed: {str(e)}")

def split_text(text, max_length=4000):
    """Split text into chunks"""
    words = text.split()
    chunks, current_chunk = [], []
    current_length = 0
    
    for word in words:
        if current_length + len(word) > max_length:
            chunks.append(" ".join(current_chunk))
            current_chunk = []
            current_length = 0
        
        current_chunk.append(word)
        current_length += len(word) + 1
    
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    
    return chunks

def translate_text(text, to_lang="en"):
    """Translate text using Azure Translator"""
    try:
        url = TRANSLATOR_ENDPOINT + f"/translate?api-version=3.0&to={to_lang}"
        
        headers = {
            'Ocp-Apim-Subscription-Key': TRANSLATOR_KEY,
            'Ocp-Apim-Subscription-Region': TRANSLATOR_REGION,
            'Content-type': 'application/json'
        }
        
        body = [{'text': text}]
        
        response = requests.post(url, headers=headers, json=body)
        return response.json()[0]['translations'][0]['text']
    except Exception as e:
        raise Exception(f"Translation failed: {str(e)}")

def translate_long_text(text, to_lang="en", chunk_size=4000):
    """Translate long text by splitting into chunks"""
    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
    final_text = ""
    
    for chunk in chunks:
        final_text += translate_text(chunk, to_lang) + " "
    
    return final_text

def summarize_text(text):
    """Summarize text using Azure Text Analytics"""
    try:
        client = TextAnalyticsClient(
            endpoint=AZURE_LANGUAGE_ENDPOINT,
            credential=AzureKeyCredential(AZURE_LANGUAGE_KEY)
        )
        
        poller = client.begin_extract_summary([text])
        result = poller.result()
        
        summary = ""
        for doc in result:
            for sentence in doc.sentences:
                summary += sentence.text + " "
        
        return summary
    except Exception as e:
        raise Exception(f"Summarization failed: {str(e)}")

def summarize_long_text(text):
    """Summarize long text by splitting into chunks"""
    chunks = split_text(text)
    final_summary = ""
    
    for chunk in chunks:
        final_summary += summarize_text(chunk) + "\n"
    
    return final_summary

# ============ BACKGROUND PROCESSING ============
def process_video(job_id: str, video_url: str):
    """Main processing pipeline"""
    try:
        JOBS[job_id]["status"] = "processing"
        
        # Create unique temp files for this job
        temp_dir = os.path.join(TEMP_DIR, f"summarization_{job_id}")
        os.makedirs(temp_dir, exist_ok=True)
        
        video_path = os.path.join(temp_dir, "video.mp4")
        audio_path = os.path.join(temp_dir, "audio.wav")
        
        # Download video
        JOBS[job_id]["status"] = "downloading"
        download_video(video_url, video_path)
        
        # Extract audio
        JOBS[job_id]["status"] = "extracting_audio"
        extract_audio(video_path, audio_path)
        
        # Speech to text
        JOBS[job_id]["status"] = "transcribing"
        arabic_text = speech_to_text_long(audio_path)
        JOBS[job_id]["transcript"] = arabic_text
        
        # Translate to English
        JOBS[job_id]["status"] = "translating_to_english"
        english_text = translate_long_text(arabic_text, "en")
        
        # Summarize
        JOBS[job_id]["status"] = "summarizing"
        summary_en = summarize_long_text(english_text)
        
        # Translate summary back to Arabic
        JOBS[job_id]["status"] = "translating_summary"
        summary_ar = translate_long_text(summary_en, "ar")
        JOBS[job_id]["summary_ar"] = summary_ar
        
        JOBS[job_id]["status"] = "completed"
        
        # Cleanup temp files
        import shutil
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        
    except Exception as e:
        JOBS[job_id]["status"] = "failed"
        JOBS[job_id]["error"] = str(e)

# ============ API ENDPOINTS ============
@app.post("/summarize", response_model=SummaryResponse)
async def summarize_video(request: VideoRequest, background_tasks: BackgroundTasks):
    """
    Submit a video URL for summarization.
    Returns a job_id to check status later.
    """
    if not all([AZURE_SPEECH_KEY, AZURE_LANGUAGE_KEY, TRANSLATOR_KEY]):
        raise HTTPException(status_code=500, detail="Azure credentials not configured")
    
    job_id = str(uuid.uuid4())
    
    JOBS[job_id] = {
        "status": "pending",
        "transcript": None,
        "summary_ar": None,
        "error": None
    }
    
    background_tasks.add_task(process_video, job_id, request.url)
    
    return SummaryResponse(job_id=job_id, status="pending")

@app.get("/status/{job_id}", response_model=JobStatusResponse)
async def get_status(job_id: str):
    """Check the status of a summarization job"""
    if job_id not in JOBS:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job = JOBS[job_id]
    return JobStatusResponse(
        job_id=job_id,
        status=job["status"],
        transcript=job["transcript"],
        summary_ar=job["summary_ar"],
        error=job["error"]
    )

# ============ RUN ============
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
