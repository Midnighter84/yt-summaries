def generate_summary_html(video_id: str, summary_md: str, metadata: dict) -> str:
    """
    Generates an HTML string for the video summary, including metadata and markdown rendering.
    """
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
    return html_content
