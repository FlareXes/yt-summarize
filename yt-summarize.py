#!/usr/bin/env python3

import requests
import argparse
import yt_dlp
import json

MODEL = "starling-lm"
API_URL = "http://localhost:11434/api/generate"


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
    data = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "raw": False,
    }

    data = json.dumps(data)
    headers = {"Content-Type": "application/json"}

    response = requests.post(API_URL, data=data, headers=headers)
    json_response = response.json()

    if "response" in json_response:
        print(json_response["response"])
    else:
        print("Error: Response field not found in the JSON response.")


def process(args):
    if args.model is not None:
        global MODEL
        MODEL = args.model

    if args.url is not None:
        global API_URL
        API_URL = args.url

    for link in args.youtube_links:
        print("Extracting English Subtitle...")
        download_subtitle(link)

        print("\nSummarizing...", link)
        summarize(generate_prompt())
        print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="yt-summarizer",
        description="Command line utility to summarize YouTube videos from subtitles.",
        formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=47)
    )

    parser.add_argument("-m", "--model", nargs="?", type=str, help="Model Nane", default=None)
    parser.add_argument("-u", "--url", nargs="?", type=str, help="API URL", default=None)
    parser.add_argument("youtube_links", nargs="+", help="YouTube Video Link")

    args = parser.parse_args()
    process(args)
