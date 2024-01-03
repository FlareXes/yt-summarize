# Yt-Summarize: YouTube Subtitle Summarizer

This Python script allows you to extract English subtitles from a YouTube video and then generate a summary using an AI-powered language model. The summary is generated based on a predefined prompt and the extracted subtitles.

## Prerequisites

Before using the script, make sure you have the following installed:

- Python 3
- [yt-dlp](https://github.com/yt-dlp/yt-dlp/): A command-line program to download videos from YouTube and other sites
- [requests](https://pypi.org/project/requests/): Python HTTP library for making requests
- A running instance of the [llama2-uncensored](https://hub.docker.com/r/ollama/ollama/) language model API

## Usage

1. Clone the repository:

   ```bash
   git clone https://github.com/FlareXes/yt-summarize.git
   cd yt-summarize
   ```

2. Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the script with a YouTube video URL:

   ```bash
   python3 yt-summarize.py <youtube_video_url>
   ```

   Replace `<youtube_video_url>` with the URL of the YouTube video you want to summarize.

## Configuration

- The script uses a predefined prompt stored in the `prompts.json` file. You can customize or add prompts in this file.

## Notes

- The generated summary is printed to the console.

Feel free to contribute to and enhance this project! If you encounter any issues, please report them in the [issue tracker](https://github.com/FlareXes/yt-summarize/issues).