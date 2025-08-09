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

    def save_summary_html(self, video_id: str, summary_md: str, metadata: dict):
        html_path = self.get_summary_html_path(video_id)
        
        # Format metadata for display
        metadata_html = ""
        if metadata:
            metadata_html += "<div>"
            if metadata.get('title'):
                metadata_html += f"<h1>{metadata['title']}</h1>"
            if metadata.get('uploader'):
                metadata_html += f"<p><strong>Uploader:</strong> {metadata['uploader']}</p>"
            if metadata.get('upload_date'):
                # Format date from YYYYMMDD to YYYY-MM-DD
                upload_date = metadata['upload_date']
                formatted_date = f"{upload_date[:4]}-{upload_date[4:6]}-{upload_date[6:]}"
                metadata_html += f"<p><strong>Upload Date:</strong> {formatted_date}</p>"
            if metadata.get('duration'):
                minutes = metadata['duration'] // 60
                seconds = metadata['duration'] % 60
                metadata_html += f"<p><strong>Duration:</strong> {minutes}m {seconds}s</p>"
            if metadata.get('description'):
                # Simple newline to <br> conversion for description
                desc_lines = metadata['description'].split('\n')
                formatted_desc = "<br>".join(desc_lines[:5]) + ("..." if len(desc_lines) > 5 else "") # Limit description to 5 lines
                metadata_html += f"<p><strong>Description:</strong><br>{formatted_desc}</p>"
            metadata_html += "<hr></div>"

        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Summary for {video_id}</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <style>
        body {{
            font-family: 'Arial', sans-serif;
            line-height: 1.6;
            color: #333;
            margin: 0;
            padding: 20px;
            background-color: #f4f4f4;
        }}
        #content {{
            max-width: 800px;
            margin: 20px auto;
            padding: 30px;
            background-color: #fff;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }}
        h1, h2, h3, h4, h5, h6 {{
            color: #0056b3;
        }}
        pre {{
            background-color: #eee;
            padding: 10px;
            border-radius: 5px;
            overflow-x: auto;
        }}
        code {{
            font-family: 'Courier New', Courier, monospace;
            background-color: #eee;
            padding: 2px 4px;
            border-radius: 3px;
        }}
    </style>
</head>
<body>
    <div id="content">
        {metadata_html}
    </div>
    <script>
        document.getElementById('content').innerHTML +=
            marked.parse(`{summary_md.replace('`', '\\`')}`);
    </script>
</body>
</html>
"""
        with open(html_path, "w") as f:
            f.write(html_content)
