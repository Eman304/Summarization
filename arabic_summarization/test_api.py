#!/usr/bin/env python3
"""
Test script for the Text Summarization API
"""

import requests
import json

def test_api():
    base_url = "http://127.0.0.1:8000"

    # Test health
    print("Testing health endpoint...")
    response = requests.get(f"{base_url}/health")
    print(f"Health: {response.json()}")

    # Test Arabic summarization
    arabic_text = "الذكاء الاصطناعي يغير طريقة تعلمنا وتعليم المعلمين. تستخدم تقنيات الذكاء الاصطناعي في المنصات التعليمية لتوفير تجارب تعلم مخصصة، أتمتة المهام الإدارية، وتحسين مشاركة الطلاب."
    print("\nTesting Arabic summarization...")
    response = requests.post(
        f"{base_url}/summarize",
        json={"text": arabic_text, "language": "ar"}
    )
    if response.status_code == 200:
        print(f"Arabic Summary: {response.json()['summary']}")
    else:
        print(f"Error: {response.text}")

    # Test English summarization
    english_text = "Artificial Intelligence is transforming the education sector in many ways, changing how students learn and how teachers teach. AI technologies are being integrated into educational platforms to provide personalized learning experiences."
    print("\nTesting English summarization...")
    response = requests.post(
        f"{base_url}/summarize",
        json={"text": english_text, "language": "en"}
    )
    if response.status_code == 200:
        print(f"English Summary: {response.json()['summary']}")
    else:
        print(f"Error: {response.text}")

if __name__ == "__main__":
    test_api()