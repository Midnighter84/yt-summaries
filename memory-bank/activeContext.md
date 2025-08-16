# Active Context: YouTube Summarizer (`yt-summaries`)

## Current work focus
The current focus is on enhancing the `yt-summaries` project by:
-   Implementing a Firebase Storage backend with local caching.
-   Refactoring HTML generation into a dedicated module.
-   Adding command-line argument parsing for YouTube URLs.
-   Ensuring mobile responsiveness and improved styling for HTML summaries.
-   Extracting and displaying video metadata in HTML summaries.
-   Fixing the double `.mp3` file extension bug during audio download.

## Recent changes
-   Added functionality to process the most recent videos from a list of YouTube channels.
-   Implemented `process_channels` and `get_channel_videos` methods in `core.py`.
-   Updated `main.py` to accept `--channels` and `--videos-per-channel` command-line arguments.
-   Introduced `storage_interface.py` for storage abstraction.
-   Refactored `storage.py` into `LocalStorage` and `FirebaseStorage` classes.
-   Moved HTML generation logic from `storage.py` to `html_generator.py`.
-   Updated `core.py` to use the new storage interface and HTML generator.
-   Modified `main.py` to accept YouTube URLs as command-line arguments and to configure storage/transcription modes.
-   Added `firebase-admin` to `requirements.txt`.
-   Updated `README.md` to reflect all new features, usage, and configuration.
-   Implemented metadata extraction and display in HTML summaries.
-   Added viewport meta tag and CSS for mobile responsiveness and improved readability in HTML summaries.
-   Fixed the `yt-dlp` `outtmpl` issue causing double `.mp3` extensions.

## Next steps
-   Update the rest of the memory bank to reflect the new channel processing functionality.
-   Verify the full functionality of the application with both local and Firebase storage modes.
-   Test transcription modes (local and cloud) thoroughly.
-   Ensure all caching mechanisms work as expected.
-   Confirm that HTML summaries are correctly generated, styled, and include metadata.

## Active decisions and considerations
-   The user will handle Firebase project setup and API key configuration.
-   The user will manage the Python virtual environment and dependency installation.
-   Prioritizing robust core functionality and modularity for future extensions.

## Learnings and project insights
-   The importance of clear storage abstraction for future extensibility.
-   The benefits of separating concerns (e.g., HTML generation from storage).
-   Careful handling of `yt-dlp` output templates to avoid file naming issues.
-   The need for comprehensive documentation (README and Memory Bank) for complex projects.
