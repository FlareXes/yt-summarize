#!/usr/bin/env python3

import requests
import yt_dlp
import json
import sys


def get_prompt(prompt_name="detailed"):
    with open("./prompts.json", "r") as f:
        prompt_data = json.load(f)
        prompts = prompt_data.get("prompts")

        for prompt in prompts:
            if prompt["name"] == prompt_name:
                return prompt.get("content")


def generate_prompt():
    with open("/tmp/subtitle.en.vtt", "r") as f:
        subtitle = f.read()
    prompt = get_prompt()
    sep = "\n\n-----------------------\n\n"
    return subtitle + sep + prompt


def download_subtitle(url):
    ydl_opts = {
        "skip_download": True,
        "outtmpl": {"default": "/tmp/subtitle"},
        "writesubtitles": True,
        "writeautomaticsub": True,
        "subtitleslangs": ["en"],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.extract_info(url)


def summarize(prompt):
    # API endpoint
    api_url = "http://localhost:11434/api/generate"

    # Request data
    data = {
        "model": "llama2-uncensored",
        "prompt": prompt,
        "stream": False,
        "raw": False,
    }

    response = requests.post(
        api_url, data=json.dumps(data), headers={"Content-Type": "application/json"}
    )
    json_response = response.json()

    if "response" in json_response:
        print(json_response["response"])
    else:
        print("Error: Response field not found in the JSON response.")


if __name__ == "__main__":
    url = sys.argv[1]

    print("Extracting English Subtitle...")
    download_subtitle(url)

    print("Summarizing Subtitle...")
    summarize(generate_prompt())
