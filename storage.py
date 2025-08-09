import os
import json
from pathlib import Path

class Storage:
    def __init__(self, base_dir: str = "data"):
        self.base_dir = Path(base_dir)
        self.audio_dir = self.base_dir / "audio"
        self.transcripts_dir = self.base_dir / "transcripts"
        self.summaries_dir = self.base_dir / "summaries"
        self.metadata_dir = self.base_dir / "video-metadata"
        self._create_dirs()

    def _create_dirs(self):
        self.audio_dir.mkdir(parents=True, exist_ok=True)
        self.transcripts_dir.mkdir(parents=True, exist_ok=True)
        self.summaries_dir.mkdir(parents=True, exist_ok=True)
        self.metadata_dir.mkdir(parents=True, exist_ok=True)

    def get_audio_path(self, video_id: str) -> Path:
        return self.audio_dir / f"{video_id}.mp3"

    def get_transcript_path(self, video_id: str) -> Path:
        return self.transcripts_dir / f"{video_id}.txt"

    def get_summary_path(self, video_id: str) -> Path:
        return self.summaries_dir / f"{video_id}.md"

    def get_summary_html_path(self, video_id: str) -> Path:
        return self.summaries_dir / f"{video_id}.html"

    def get_metadata_path(self, video_id: str) -> Path:
        return self.metadata_dir / f"{video_id}.json"

    def audio_exists(self, video_id: str) -> bool:
        return self.get_audio_path(video_id).exists()

    def transcript_exists(self, video_id: str) -> bool:
        return self.get_transcript_path(video_id).exists()

    def summary_exists(self, video_id: str) -> bool:
        return self.get_summary_path(video_id).exists()

    def metadata_exists(self, video_id: str) -> bool:
        return self.get_metadata_path(video_id).exists()

    def save_transcript(self, video_id: str, transcript: str):
        with open(self.get_transcript_path(video_id), "w") as f:
            f.write(transcript)

    def load_transcript(self, video_id: str) -> str:
        with open(self.get_transcript_path(video_id), "r") as f:
            return f.read()

    def save_metadata(self, video_id: str, metadata: dict):
        with open(self.get_metadata_path(video_id), "w") as f:
            json.dump(metadata, f, indent=4)

    def load_metadata(self, video_id: str) -> dict:
        with open(self.get_metadata_path(video_id), "r") as f:
            return json.load(f)

    def save_summary(self, video_id: str, summary: str):
        with open(self.get_summary_path(video_id), "w") as f:
            f.write(summary)

    def load_summary(self, video_id: str) -> str:
        with open(self.get_summary_path(video_id), "r") as f:
            return f.read()

    def save_summary_html(self, video_id: str, html_content: str):
        html_path = self.get_summary_html_path(video_id)
        with open(html_path, "w") as f:
            f.write(html_content)
