from abc import ABC, abstractmethod
from pathlib import Path

class StorageInterface(ABC):
    @abstractmethod
    def get_audio_path(self, video_id: str) -> Path:
        pass

    @abstractmethod
    def get_transcript_path(self, video_id: str) -> Path:
        pass

    @abstractmethod
    def get_summary_path(self, video_id: str) -> Path:
        pass

    @abstractmethod
    def get_summary_html_path(self, video_id: str) -> Path:
        pass

    @abstractmethod
    def get_metadata_path(self, video_id: str) -> Path:
        pass

    @abstractmethod
    def audio_exists(self, video_id: str) -> bool:
        pass

    @abstractmethod
    def transcript_exists(self, video_id: str) -> bool:
        pass

    @abstractmethod
    def summary_exists(self, video_id: str) -> bool:
        pass

    @abstractmethod
    def metadata_exists(self, video_id: str) -> bool:
        pass

    @abstractmethod
    def save_transcript(self, video_id: str, transcript: str):
        pass

    @abstractmethod
    def load_transcript(self, video_id: str) -> str:
        pass

    @abstractmethod
    def save_metadata(self, video_id: str, metadata: dict):
        pass

    @abstractmethod
    def load_metadata(self, video_id: str) -> dict:
        pass

    @abstractmethod
    def save_summary(self, video_id: str, summary: str):
        pass

    @abstractmethod
    def load_summary(self, video_id: str) -> str:
        pass

    @abstractmethod
    def save_summary_html(self, video_id: str, html_content: str):
        pass
