# Yt-Summarize

Yt-Summarize is a command-line utility for summarizing YouTube videos based on their English subtitles. It utilizes a self-hosted language model for text summarization.

## Prerequisites

- Python 3
- [yt-dlp](https://github.com/yt-dlp/yt-dlp): YouTube downloader library
- [requests](https://docs.python-requests.org/en/latest/): HTTP library
- Running LLM model url, for easy setup check-out [Ollama](https://ollama.ai/)
- Ensure the required dependencies are installed using:

  ```bash
  pip install -r requirements.txt
  ```

## Usage

```bash
python yt_summarizer.py [-h] [-m MODEL] [-u URL] [--prompt-name PROMPT_NAME] [--subtitle-dir SUBTITLE_DIR] youtube_links [youtube_links ...]
```

### Options:

- `-m, --model`: Specify the language model to be used for summarization.
- `-u, --url`: Specify the API URL for the language model.
- `--prompt-name`: Specify the prompt name as defined in the prompts.json file.
- `--subtitle-dir`: Specify the directory to save the extracted subtitles.

### Arguments:

- `youtube_links`: One or more YouTube video URLs for summarization.

> :round_pushpin: **Note:** You can edit `yt-summarize.py` global variables to make changes permanent.

## How It Works

1. Extract English subtitles from the provided YouTube video links.
2. Clean and process the subtitles to remove unnecessary information.
3. Generate a prompt for the summarization model by combining cleaned subtitles and a predefined prompt from prompts.json.
4. Send the prompt to the specified language model API for summarization.
5. Display the summarized text.

## Summary Prompts
- **PROMPT_JSON_LOC**: Location of the `prompts.json` file. The file should contain a list of prompts with names and corresponding content.
- You can add your custom prompts in `prompt.json` with unique name and id. Then you can use it with `--prompt-name` option.

## Example

```bash
python yt_summarizer.py "https://www.youtube.com/watch?v=example_video_id"
```

This command will use default specification to summarize the provided YouTube video.


```bash
python yt_summarizer.py -m my_custom_model -u http://custom-api-url.com --prompt-name basic "https://www.youtube.com/watch?v=example_video_id"
```

This command will use the specified model, API URL, and prompt to summarize the provided YouTube video.

## Desktop Integration
For easy access of script in Linux, Windows & MacOS, check out [setup documentation](https://github.com/FlareXes/yt-summarize/wiki/Setup).

## Contribute

Feel free to contribute to and enhance this project! If you encounter any issues, please report them in the [issue tracker](https://github.com/FlareXes/yt-summarize/issues).

## License

This project by [FlareXes](https://github.com/FlareXes) is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.