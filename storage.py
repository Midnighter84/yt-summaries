import os
import json
from pathlib import Path
import firebase_admin
from firebase_admin import credentials, storage as firebase_storage
from storage_interface import StorageInterface

class LocalStorage(StorageInterface):
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
        with open(self.get_summary_html_path(video_id), "w") as f:
            f.write(html_content)

class FirebaseStorage(StorageInterface):
    def __init__(self, local_storage: LocalStorage, cred_path: str, bucket_name: str):
        self.local_storage = local_storage
        # TODO: Set up Firebase credentials
        if not firebase_admin._apps:
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred, {'storageBucket': bucket_name})
        self.bucket = firebase_storage.bucket()

    def _get_blob(self, path: str):
        return self.bucket.blob(path)

    def _download_if_not_exists(self, video_id: str, remote_path: str, local_path: Path):
        if not local_path.exists():
            blob = self._get_blob(remote_path)
            if blob.exists():
                blob.download_to_filename(local_path)

    def get_audio_path(self, video_id: str) -> Path:
        return self.local_storage.get_audio_path(video_id)

    def get_transcript_path(self, video_id: str) -> Path:
        return self.local_storage.get_transcript_path(video_id)

    def get_summary_path(self, video_id: str) -> Path:
        return self.local_storage.get_summary_path(video_id)

    def get_summary_html_path(self, video_id: str) -> Path:
        return self.local_storage.get_summary_html_path(video_id)

    def get_metadata_path(self, video_id: str) -> Path:
        return self.local_storage.get_metadata_path(video_id)

    def audio_exists(self, video_id: str) -> bool:
        local_path = self.get_audio_path(video_id)
        if local_path.exists():
            return True
        blob = self._get_blob(f"audio/{video_id}.mp3")
        return blob.exists()

    def transcript_exists(self, video_id: str) -> bool:
        local_path = self.get_transcript_path(video_id)
        if local_path.exists():
            return True
        blob = self._get_blob(f"transcripts/{video_id}.txt")
        return blob.exists()

    def summary_exists(self, video_id: str) -> bool:
        local_path = self.get_summary_path(video_id)
        if local_path.exists():
            return True
        blob = self._get_blob(f"summaries/{video_id}.md")
        return blob.exists()

    def metadata_exists(self, video_id: str) -> bool:
        local_path = self.get_metadata_path(video_id)
        if local_path.exists():
            return True
        blob = self._get_blob(f"video-metadata/{video_id}.json")
        return blob.exists()

    def save_transcript(self, video_id: str, transcript: str):
        self.local_storage.save_transcript(video_id, transcript)
        blob = self._get_blob(f"transcripts/{video_id}.txt")
        blob.upload_from_string(transcript)

    def load_transcript(self, video_id: str) -> str:
        local_path = self.get_transcript_path(video_id)
        self._download_if_not_exists(video_id, f"transcripts/{video_id}.txt", local_path)
        return self.local_storage.load_transcript(video_id)

    def save_metadata(self, video_id: str, metadata: dict):
        self.local_storage.save_metadata(video_id, metadata)
        blob = self._get_blob(f"video-metadata/{video_id}.json")
        blob.upload_from_string(json.dumps(metadata, indent=4))

    def load_metadata(self, video_id: str) -> dict:
        local_path = self.get_metadata_path(video_id)
        self._download_if_not_exists(video_id, f"video-metadata/{video_id}.json", local_path)
        return self.local_storage.load_metadata(video_id)

    def save_summary(self, video_id: str, summary: str):
        self.local_storage.save_summary(video_id, summary)
        blob = self._get_blob(f"summaries/{video_id}.md")
        blob.upload_from_string(summary)

    def load_summary(self, video_id: str) -> str:
        local_path = self.get_summary_path(video_id)
        self._download_if_not_exists(video_id, f"summaries/{video_id}.md", local_path)
        return self.local_storage.load_summary(video_id)

    def save_summary_html(self, video_id: str, html_content: str):
        self.local_storage.save_summary_html(video_id, html_content)
        blob = self._get_blob(f"summaries/{video_id}.html")
        blob.upload_from_string(html_content, content_type='text/html')
