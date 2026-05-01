#!/usr/bin/env python3
"""
Simple test script to interact with the Summarization API
"""

import requests
import time
import sys
from typing import Optional

BASE_URL = "http://localhost:8000"

def submit_video(video_url: str) -> Optional[str]:
    """Submit a video for summarization and return job_id"""
    print(f"📤 Submitting video: {video_url}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/summarize",
            json={"url": video_url}
        )
        
        if response.status_code == 200:
            data = response.json()
            job_id = data["job_id"]
            print(f"✅ Job submitted! Job ID: {job_id}")
            return job_id
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.text)
            return None
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return None

def check_status(job_id: str) -> Optional[dict]:
    """Check the status of a job"""
    try:
        response = requests.get(f"{BASE_URL}/status/{job_id}")
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ Error: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return None

def print_status(data: dict):
    """Pretty print status"""
    job_id = data["job_id"]
    status = data["status"]
    
    status_emoji = {
        "pending": "⏳",
        "downloading": "📥",
        "extracting_audio": "🎧",
        "transcribing": "🗣️",
        "translating_to_english": "🌍",
        "summarizing": "✍️",
        "translating_summary": "🔁",
        "completed": "✅",
        "failed": "❌"
    }
    
    emoji = status_emoji.get(status, "❓")
    print(f"{emoji} Status: {status}")
    
    if data.get("error"):
        print(f"❌ Error: {data['error']}")
    
    if data.get("transcript"):
        print(f"\n📝 Transcript (first 500 chars):\n{data['transcript'][:500]}...")
    
    if data.get("summary_ar"):
        print(f"\n📌 Summary:\n{data['summary_ar']}")

def wait_for_completion(job_id: str, check_interval: int = 10, max_wait: int = 3600):
    """Wait for a job to complete with polling"""
    print(f"\n⏳ Waiting for job to complete (checking every {check_interval}s)...")
    print("(You can close this window and check status later using the job_id)\n")
    
    elapsed = 0
    
    while elapsed < max_wait:
        data = check_status(job_id)
        
        if data:
            print_status(data)
            
            if data["status"] == "completed":
                print("\n🎉 Job completed successfully!")
                return True
            elif data["status"] == "failed":
                print("\n❌ Job failed!")
                return False
        
        print(f"\n⏳ Waiting... ({elapsed}s elapsed)\n")
        time.sleep(check_interval)
        elapsed += check_interval
    
    print(f"\n⏱️ Timeout after {max_wait}s. You can check status later with job_id: {job_id}")
    return False

def main():
    """Main function"""
    print("🎬 Summarization API Test Client\n")
    
    # Check if server is running
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ API server is running!\n")
        else:
            print("❌ API server is not responding properly")
            return
    except Exception as e:
        print(f"❌ Cannot connect to API server at {BASE_URL}")
        print(f"Make sure the server is running: python main.py")
        return
    
    # Get video URL from user
    if len(sys.argv) > 1:
        video_url = sys.argv[1]
    else:
        video_url = input("Enter YouTube video URL: ").strip()
    
    if not video_url:
        print("❌ No URL provided")
        return
    
    # Submit video
    job_id = submit_video(video_url)
    
    if job_id:
        # Wait for completion
        wait_for_completion(job_id)

if __name__ == "__main__":
    main()
