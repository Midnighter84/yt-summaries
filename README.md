# YouTube Video Summarizer

This project transcribes YouTube videos and generates AI-powered summaries of the transcripts.

## Features

- **YouTube Audio Downloader**: Downloads the audio from a YouTube video using `yt-dlp`, and extracts key metadata (title, uploader, date, description, duration). (Includes a fix for the double file extension bug).
- **Audio Transcription**: Transcribes audio using either a local Whisper model or the OpenAI API.
- **AI-Powered Summarization**: Generates a summary of the transcription using the Gemini API, saving it as both a Markdown file and a styled, mobile-responsive HTML file that includes video metadata for easy and readable viewing.
- **Caching**: Caches audio files, transcriptions, and summaries (both Markdown and HTML) to avoid re-processing the same video.
- **Configurable Prompts**: Allows using custom prompts for the summarization.
- **Abstracted Storage**: Supports both local filesystem and Firebase Storage for storing and caching all data, including audio, transcripts, summaries, and metadata.

## Project Structure

- `main.py`: The main entry point for running the summarizer.
- `core.py`: Contains the core logic for downloading, transcribing, and summarizing.
- `storage_interface.py`: Defines the interface for storage implementations.
- `storage.py`: Contains `LocalStorage` and `FirebaseStorage` implementations.
- `html_generator.py`: Contains the logic for generating the styled HTML summary pages.
- `data/`: The default directory for storing cached files, including:
    - `audio/`: Downloaded audio files.
    - `transcripts/`: Transcribed text.
    - `summaries/`: Generated markdown and HTML summaries.
    - `video-metadata/`: Extracted video metadata in JSON format.

## Usage

1.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Configure API Keys:**
    - **Gemini API Key**: Set the `GEMINI_API_KEY` environment variable or modify the placeholder in `main.py`.
    - **OpenAI API Key**: If using the `cloud` transcription mode, set the `OPENAI_API_KEY` environment variable or modify the placeholder in `main.py`.

3.  **Configure Transcription and Storage Modes:**
    - Open `main.py` and set the `TRANSCRIPTION_MODE` variable to either `'local'` or `'cloud'`.
    - Set the `STORAGE_MODE` variable to either `'local'` or `'firebase'`.
    - If using `'firebase'`, provide your Firebase credentials and bucket name in `main.py`.

4.  **Run the script:**
    ```bash
    python3 main.py
    ```

5.  **Customize:**
    - You can change the `youtube_url` and the summarization `prompt` in `main.py`.
