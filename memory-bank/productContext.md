# Product Context: YouTube Summarizer (`yt-summaries`)

## Why this project exists
This project addresses the need for quickly extracting key information from long YouTube videos without watching the entire content. It's particularly useful for educational content, long interviews, or presentations where users need to grasp the main points efficiently.

## Problems it solves
- **Time-saving**: Reduces the time spent consuming video content.
- **Information overload**: Helps in quickly sifting through vast amounts of video data.
- **Accessibility**: Provides text-based summaries for those who prefer reading or have auditory processing challenges.
- **Research efficiency**: Facilitates faster research by providing concise summaries of relevant videos.

## How it should work
The user provides a YouTube URL or a list of channel URLs. The system then:
1.  If channel URLs are provided, it fetches the most recent videos from each channel.
2.  For each video, it downloads the audio.
3.  Transcribes the audio to text.
4.  Generates an AI summary based on the transcription and a configurable prompt.
5.  Saves the audio, transcription, summary (markdown and HTML), and video metadata locally.
6.  Optionally, uploads the data to Firebase Storage for persistent, cloud-based access.
7.  Prints the local path to the generated HTML summary file.
8.  Provides a web interface hosted on Firebase to browse all summaries and view individual summary pages.

## User experience goals
-   **Simplicity**: Easy to use with command-line arguments for single videos or channels, and an intuitive web interface.
-   **Speed**: Leverages caching to provide quick results for previously processed videos.
-   **Clarity**: Summaries should be concise, accurate, and easy to read.
-   **Flexibility**: Users should be able to choose between local and cloud transcription/storage options.
