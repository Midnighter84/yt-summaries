import os
from core import YouTubeSummarizer
from storage import LocalStorage, FirebaseStorage

def main():
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
        FIREBASE_CRED_PATH = "path/to/your/firebase-credentials.json"
        FIREBASE_BUCKET_NAME = "your-firebase-bucket-name"
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

    # Example usage:
    youtube_url = "https://www.youtube.com/watch?v=jmtvmbeBUnk"
    prompt = "Provide a one-paragraph summary and a list of key takeaways from the following transcript. Please do this in the original language of the transcript."

    try:
        summary = summarizer.process_video(youtube_url, prompt)
        print("Summary:")
        print(summary)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
