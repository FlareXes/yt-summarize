#!/usr/bin/env python3


import re
import os
import re
import json
import yt_dlp
import requests
import argparse
from itertools import groupby
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

MODEL = "starling-lm"
API_URL = "http://localhost:11434/api/generate"
SUBTITLE_OUTPUT_DIR = "/tmp/subtitle"

# Options: `basic`, `basic-2`, `detailed`
PROMPT_NAME = "detailed"
PROMPT_JSON_LOC = "./prompts.json"


def download_subtitle(url, subtitle_filename):
    ydl_opts = {
        "skip_download": True,
        "outtmpl": {"default": subtitle_filename},
        "writesubtitles": True,
        "writeautomaticsub": True,
        "subtitleslangs": ["en"],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.extract_info(url)


def clean_subtitles(subtitle_text):
    # Remove subtitles enclosed in <c> tags
    subtitle_text = re.sub(r".*<c>.*</c>.*", "", subtitle_text)

    # Remove timestamps, alignments, positions, and other tags
    subtitle_text = re.sub(
        r"<.*?>|\d{2}:\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}:\d{2}\.\d{3}|align:[^ ]*|position:[^ ].",
        "",
        subtitle_text,
    )

    # Remove extra spaces and newlines
    subtitle_text = re.sub(r"(\n\s*){2,}", "\n", subtitle_text)

    # Remove consecutive duplicate lines
    subtitle_text = [key for key, group in groupby(subtitle_text.split("\n"))]

    return " ".join(map(str, subtitle_text))


def get_prompt():
    with open(PROMPT_JSON_LOC, "r") as f:
        prompt_data = json.load(f)
        prompts = prompt_data.get("prompts")

        for prompt in prompts:
            if prompt["name"] == PROMPT_NAME:
                return prompt.get("content")


def generate_prompt(subtitle_filename):
    try:
        with open(f"{subtitle_filename}.en.vtt", "r") as f:
            subtitle = clean_subtitles(f.read())
    except FileNotFoundError as e:
        print(e)
        exit(1)

    prompt = get_prompt()

    sep = "\n\n-----------------------\n\n"
    return subtitle + sep + prompt


def summarize(prompt):
    data = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "raw": False,
    }

    data = json.dumps(data)
    headers = {"Content-Type": "application/json"}

    response = requests.post(API_URL, data=data, headers=headers, verify=False, timeout=10)
    json_response = response.json()

    if "response" in json_response:
        print(json_response["response"])
    else:
        print("Error: Response field not found in the JSON response.")


def process(args):
    global MODEL, API_URL, PROMPT_NAME, SUBTITLE_OUTPUT_DIR

    if args.model is not None:
        MODEL = args.model

    if args.url is not None:
        API_URL = args.url

    if args.prompt_name is not None:
        PROMPT_NAME = args.prompt_name

    if args.subtitle_dir is not None:
        SUBTITLE_OUTPUT_DIR = args.subtitle_dir

    if not os.path.exists(SUBTITLE_OUTPUT_DIR):
        os.mkdir(SUBTITLE_OUTPUT_DIR)

    for link in args.youtube_links:
        pattern = re.compile(r"(?:https?://)?(?:www\.)?(?:youtube\.com/.*?\bv=|youtu\.be/|youtube\.com/embed/)([a-zA-Z0-9_-]{11})\b")
        match = pattern.search(link)
        if match:
            yt_id = match.group(1)
            subtitle_filename = os.path.join(SUBTITLE_OUTPUT_DIR, f"subtitle-{yt_id}")

            print("Extracting English Subtitle...")
            download_subtitle(link, subtitle_filename)

            print("\nSummarizing...", link)
            summarize(generate_prompt(subtitle_filename))

            print()
        else:
            print("Error: Invalid YouTube URL")
            exit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="yt-summarizer",
        description="Command line utility to summarize YouTube videos from subtitles.",
        formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=47),
    )

    parser.add_argument("-m", "--model", nargs="?", type=str, help="Model Nane", default=None)
    parser.add_argument("-u", "--url", nargs="?", type=str, help="API URL", default=None)
    parser.add_argument("--prompt-name", nargs="?", type=str, help="Prompt Name Specified In Prompt Json File", default=None)
    parser.add_argument("--subtitle-dir", nargs="?", type=str, help="Subtitles Ouput Directory", default=None)
    parser.add_argument("youtube_links", nargs="+", help="YouTube Video Link")

    args = parser.parse_args()
    process(args)
