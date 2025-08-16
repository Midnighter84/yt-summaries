import os
import argparse
from core import YouTubeSummarizer
from storage import LocalStorage, FirebaseStorage

def main():
    parser = argparse.ArgumentParser(description="Transcribe and summarize YouTube videos.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--youtube_url", help="The URL of the YouTube video to process.")
    group.add_argument("--channels", nargs='+', help="A list of YouTube channel IDs to process.")
    parser.add_argument("--videos-per-channel", type=int, default=1, help="Number of recent videos to process per channel.")
    args = parser.parse_args()

    # --- Configuration ---
    # Choose transcription mode: 'local' or 'cloud'
    TRANSCRIPTION_MODE = 'local' 
    # Choose storage mode: 'local' or 'firebase'
    STORAGE_MODE = 'local'

    # TODO: Set your Gemini API key here.
    # You can get a key from https://aistudio.google.com/app/apikey
    gemini_api_key = os.environ.get("GEMINI_API_KEY", "")
    if not gemini_api_key or gemini_api_key == "YOUR_API_KEY_HERE":
        print("Error: GEMINI_API_KEY environment variable not set.")
        print("Please set the GEMINI_API_KEY environment variable or replace 'YOUR_API_KEY_HERE' in main.py.")
        return

    # TODO: Set your OpenAI API key here if using cloud transcription.
    openai_api_key = os.environ.get("OPENAI_API_KEY", "")
    if TRANSCRIPTION_MODE == 'cloud' and (not openai_api_key or openai_api_key == "YOUR_API_KEY_HERE"):
        print("Error: OPENAI_API_KEY environment variable not set for cloud transcription mode.")
        print("Please set the OPENAI_API_KEY environment variable or replace 'YOUR_API_KEY_HERE' in main.py.")
        return

    # --- Storage Initialization ---
    if STORAGE_MODE == 'local':
        storage = LocalStorage()
    elif STORAGE_MODE == 'firebase':
        # TODO: Configure Firebase
        FIREBASE_CRED_PATH = "firebase-credentials.json"
        FIREBASE_BUCKET_NAME = "gs://yt-summaries-1984.firebasestorage.app"
        local_cache = LocalStorage()
        storage = FirebaseStorage(local_storage=local_cache, cred_path=FIREBASE_CRED_PATH, bucket_name=FIREBASE_BUCKET_NAME)
    else:
        raise ValueError(f"Invalid STORAGE_MODE: {STORAGE_MODE}")

    summarizer = YouTubeSummarizer(
        storage=storage,
        gemini_api_key=gemini_api_key,
        transcription_mode=TRANSCRIPTION_MODE,
        openai_api_key=openai_api_key
    )

    prompt = "Provide a one-paragraph summary and a list of key takeaways from the following transcript. Please do this in the original language of the transcript."

    print(args)
    try:
        if args.youtube_url:
            summary_file_path = summarizer.process_video(args.youtube_url, prompt)
            print(f"Summary saved to: {summary_file_path}")
        elif args.channels:
            summarizer.process_channels(args.channels, args.videos_per_channel, prompt)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
