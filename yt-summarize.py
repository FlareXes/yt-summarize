#!/usr/bin/env python3

import requests
import yt_dlp
import json
import sys

def download_subtitle(url):
    ydl_opts = {
        "skip_download": True,
        "outtmpl": {"default": "subtitle"},
        "writesubtitles": True,
        "writeautomaticsub": True,
        "subtitleslangs": ["en"],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.extract_info(url)

def get_prompt():
    with open("./subtitle.en.vtt", "r") as f:
        subtitle = f.read()

    prompt = """
---------

Can you provide a comprehensive summary of the given transcribe? The summary should cover all the key points and main ideas presented in the original text, while also condensing the information into a concise and easy-to-understand format. Please ensure that the summary includes relevant details and examples that support the main ideas, while avoiding any unnecessary information or repetition. The length of the summary should be appropriate for the length and complexity of the original text, providing a clear and accurate overview without omitting any important information.
And, Can you determine from the provided transcription whether the video is a practical demonstration or not?
"""
    return subtitle + prompt

def summarize(prompt):
    # API endpoint
    api_url = "http://localhost:11434/api/generate"

    # Request data
    data = {"model": "llama2-uncensored", "prompt": prompt, "stream": False, "raw": False}

    # Send POST request
    response = requests.post(
        api_url, data=json.dumps(data), headers={"Content-Type": "application/json"}
    )

    # Parse JSON response
    json_response = response.json()

    # Print the "response" field
    if "response" in json_response:
        print(json_response["response"])

    else:
        print("Error: Response field not found in the JSON response.")

if __name__ == "__main__":
    url = sys.argv[1]

    print("Extracting English Subtitle...")
    download_subtitle(url)
    
    print("Summarizing Subtitle...")
    summarize(get_prompt())
