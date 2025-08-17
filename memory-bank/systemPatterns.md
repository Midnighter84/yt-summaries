# System Patterns: YouTube Summarizer (`yt-summaries`)

## System Architecture
The system follows a modular architecture, separating concerns into distinct components:
-   **Core Logic (`core.py`)**: Orchestrates the overall process, including video ID extraction, audio download, transcription, and summarization. It acts as the central coordinator.
-   **Storage Abstraction (`storage_interface.py`, `storage.py`)**: Provides a flexible layer for data persistence. `StorageInterface` defines the contract, while `LocalStorage` handles local file operations and `FirebaseStorage` handles cloud storage with local caching.
-   **HTML Generation (`html_generator.py`)**: Encapsulates the logic for creating styled HTML summaries from markdown content and video metadata.
-   **Main Entry Point (`main.py`)**: Handles command-line arguments, configuration (API keys, transcription mode, storage mode), and initializes the core components.
-   **Front-end (`firebase/public`)**: A static web page that provides a user interface for browsing and viewing summaries. It is built with HTML, CSS, and JavaScript.
-   **Firebase Functions (`firebase/functions`)**: A set of serverless functions that provide data to the front-end.
    -   `getSummaries`: Returns a list of all video metadata.
    -   `getVideo`: Returns the metadata and summary for a single video.

## Key Technical Decisions
-   **Caching**: Local filesystem is used as a primary cache for all processed data (audio, transcripts, summaries, metadata) to minimize redundant work and API calls.
-   **Pluggable Storage**: The use of a `StorageInterface` allows for easy swapping or extension of storage backends without altering the core logic.
-   **Modular Design**: Separation of concerns into `core`, `storage`, and `html_generator` modules promotes maintainability and testability.
-   **Command-Line Interface**: `argparse` is used for simple and direct user interaction. It supports processing a single video URL or fetching recent videos from multiple channels.

## Design Patterns in Use
-   **Strategy Pattern**: Implemented through the `StorageInterface` and its concrete `LocalStorage` and `FirebaseStorage` implementations, allowing the application to choose storage behavior at runtime.
-   **Facade Pattern**: The `YouTubeSummarizer` class acts as a facade, providing a simplified interface to the complex underlying operations (downloading, transcribing, summarizing, and storing).

## Component Relationships
-   `main.py` depends on `core.py` and `storage.py`.
-   `core.py` depends on `storage_interface.py` and `html_generator.py`.
-   `storage.py` depends on `storage_interface.py` and `firebase_admin` (for `FirebaseStorage`).

## Critical Implementation Paths
-   **`process_video` in `core.py`**: This method defines the main workflow for a single video:
    1.  Check for existing summary in cache.
    2.  Download audio and metadata (with caching).
    3.  Transcribe audio (with caching, local or cloud).
    4.  Generate AI summary.
    5.  Save markdown summary.
    6.  Generate and save HTML summary.
    7.  Return HTML summary file path.
-   **`process_channels` in `core.py`**: This method orchestrates the processing of multiple channels:
    1.  Iterates through a list of channel URLs.
    2.  For each channel, calls `get_channel_videos` to fetch the latest video URLs using `yt-dlp`.
    3.  For each video URL, calls `process_video` to handle the summarization workflow.
