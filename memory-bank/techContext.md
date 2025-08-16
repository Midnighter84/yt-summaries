# Tech Context: YouTube Summarizer (`yt-summaries`)

## Technologies Used
-   **Python**: Primary programming language.
-   **`yt-dlp`**: For downloading YouTube video audio and extracting metadata.
-   **`whisper` (OpenAI)**: For local audio transcription.
-   **OpenAI API**: For cloud-based audio transcription (Whisper API).
-   **Gemini API (Google)**: For AI-powered summarization.
-   **`firebase-admin`**: For interacting with Firebase Storage.
-   **`argparse`**: For command-line argument parsing.
-   **`marked.js`**: JavaScript library used in the generated HTML for client-side Markdown rendering.

## Development Setup
-   **Virtual Environments**: Recommended for managing Python dependencies (`venv` or `conda`).
-   **API Keys**: Requires `GEMINI_API_KEY` and optionally `OPENAI_API_KEY` (for cloud transcription) to be set as environment variables or directly in `main.py`.
-   **Firebase Credentials**: For Firebase storage, a service account key JSON file path and bucket name are required.

## Technical Constraints
-   **API Rate Limits**: Dependent on Google Gemini and OpenAI API quotas.
-   **Local Whisper Model Size**: The "base" model is used for local transcription, which is relatively small. Larger models offer better accuracy but require more disk space and processing power.
-   **`yt-dlp` Compatibility**: Relies on `yt-dlp` to keep up with YouTube's changes.
-   **Firebase Storage Limits**: Subject to Firebase Storage quotas and pricing.

## Dependencies
See `requirements.txt` for a full list of Python dependencies.

## Tool Usage Patterns
-   **`pip`**: For installing Python packages.
-   **`python3`**: For running the main script.
-   **Environment Variables**: Used for sensitive API keys.
