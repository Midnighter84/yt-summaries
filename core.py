import os
import re
from pathlib import Path
import yt_dlp
import whisper
import google.generativeai as genai
import openai
from storage import Storage

class YouTubeSummarizer:
    def __init__(self, storage: Storage, gemini_api_key: str, transcription_mode: str = 'local', openai_api_key: str = None):
        self.storage = storage
        self.transcription_mode = transcription_mode

        genai.configure(api_key=gemini_api_key)
        self.genai_model = genai.GenerativeModel('gemini-2.5-pro')

        if self.transcription_mode == 'local':
            self.whisper_model = whisper.load_model("base")
        elif self.transcription_mode == 'cloud':
            if not openai_api_key:
                raise ValueError("OpenAI API key is required for cloud transcription mode.")
            self.openai_client = openai.OpenAI(api_key=openai_api_key)
        else:
            raise ValueError(f"Invalid transcription mode: {self.transcription_mode}")

    def get_video_id(self, youtube_url: str) -> str:
        video_id_match = re.search(r"(?<=v=)[^&#]+", youtube_url)
        if not video_id_match:
            raise ValueError("Invalid YouTube URL")
        return video_id_match.group(0)

    def download_audio(self, youtube_url: str) -> Path:
        video_id = self.get_video_id(youtube_url)
        audio_path = self.storage.get_audio_path(video_id)

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': str(audio_path),
            'quiet': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            if not self.storage.metadata_exists(video_id):
                print(f"Downloading metadata for video {video_id}...")
                info_dict = ydl.extract_info(youtube_url, download=False)
                metadata = {
                    'title': info_dict.get('title'),
                    'uploader': info_dict.get('uploader'),
                    'upload_date': info_dict.get('upload_date'),
                    'description': info_dict.get('description'),
                    'duration': info_dict.get('duration'),
                }
                self.storage.save_metadata(video_id, metadata)
            else:
                print(f"Metadata for video {video_id} found in cache.")

            if not self.storage.audio_exists(video_id):
                print(f"Downloading audio for video {video_id}...")
                ydl.download([youtube_url])
            else:
                print(f"Audio for video {video_id} found in cache.")

        return audio_path

    def transcribe_audio(self, video_id: str, audio_path: Path) -> str:
        if self.storage.transcript_exists(video_id):
            print(f"Transcript for video {video_id} found in cache.")
            return self.storage.load_transcript(video_id)

        print(f"Transcribing audio for video {video_id} using {self.transcription_mode} mode...")
        if self.transcription_mode == 'local':
            result = self.whisper_model.transcribe(str(audio_path))
            transcript = result["text"]
        else: # cloud
            with open(audio_path, "rb") as audio_file:
                result = self.openai_client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file
                )
                transcript = result.text

        self.storage.save_transcript(video_id, transcript)
        return transcript

    def summarize_transcript(self, video_id: str, transcript: str, prompt: str) -> str:
        print(f"Generating summary for video {video_id}...")
        full_prompt = f"{prompt}\n\n{transcript}"
        summary = self.genai_model.generate_content(full_prompt).text
        self.storage.save_summary(video_id, summary)
        
        metadata = self.storage.load_metadata(video_id)
        self.storage.save_summary_html(video_id, summary, metadata)
        
        return summary

    def process_video(self, youtube_url: str, prompt: str) -> str:
        video_id = self.get_video_id(youtube_url)
        
        if self.storage.summary_exists(video_id):
            print(f"Summary for video {video_id} found in cache.")
            return self.storage.load_summary(video_id)

        audio_path = self.download_audio(youtube_url)
        transcript = self.transcribe_audio(video_id, audio_path)
        summary = self.summarize_transcript(video_id, transcript, prompt)
        return summary
