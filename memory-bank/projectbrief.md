# Project Brief: YouTube Summarizer (`yt-summaries`)

## Core Requirements
The primary goal of this project is to provide a tool that can:
1.  Transcribe audio from YouTube videos.
2.  Generate AI-powered summaries of these transcriptions.
3.  Store and cache all generated data (audio, transcripts, summaries, metadata).

## Key Functionality
-   Download YouTube video audio.
-   Transcribe audio using either local Whisper model or OpenAI API.
-   Generate AI summaries using Gemini API with configurable prompts.
-   Cache all processed data locally to avoid redundant work.
-   Provide an abstracted storage layer to support different backends (local filesystem, Firebase Storage).
-   Generate both Markdown and styled, mobile-responsive HTML summaries.
-   Extract and store YouTube video metadata.
-   Accept a YouTube URL or a list of channel URLs as command-line arguments.
-   Print the path to the generated summary file upon completion.

## Project Goals
-   **Efficiency**: Minimize re-processing by leveraging caching.
-   **Flexibility**: Allow users to choose transcription and storage backends.
-   **Readability**: Provide well-formatted and easily accessible summaries.
-   **Maintainability**: Use a modular and extensible architecture.
