# Progress: YouTube Summarizer (`yt-summaries`)

## What works
-   Core functionality: Downloading audio, transcribing, and generating AI summaries for single videos and recent videos from channels.
-   Local caching for audio, transcripts, summaries (Markdown and HTML), and video metadata.
-   Configurable transcription modes (local Whisper and OpenAI API).
-   Configurable storage modes (local filesystem and Firebase Storage with local caching).
-   Styled, mobile-responsive HTML summaries with embedded video metadata.
-   Command-line argument parsing for YouTube URL and channel URLs.
-   Printing the path to the generated HTML summary file upon completion.
-   Fixed double `.mp3` extension bug during audio download.
-   A web interface to browse and view video summaries, hosted on Firebase.
-   Firebase functions to provide data to the web interface.

## What's left to build
-   Further enhancements to the web interface (e.g., search, filtering, pagination).
-   Error handling improvements in the Firebase functions.
-   Potentially adding more summarization prompts or allowing user-defined prompts via CLI.

## Current status
The core functionality is robust and well-tested. The project is ready for use as a command-line tool, with options for both local and cloud services.

## Known issues
-   None currently identified beyond potential API rate limits or network issues.

## Evolution of project decisions
-   Initial focus on local processing, then expanded to include cloud API options for transcription and storage for flexibility.
-   HTML generation was initially embedded in storage, then refactored into a separate module for better separation of concerns and maintainability.
-   Metadata extraction and inclusion in HTML summaries were added to enhance the utility of the generated output.
-   Command-line argument parsing was implemented for user convenience.
