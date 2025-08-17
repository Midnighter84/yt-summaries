document.addEventListener("DOMContentLoaded", () => {
    const videoDetails = document.getElementById("video-details");
    const urlParams = new URLSearchParams(window.location.search);
    const videoId = urlParams.get('video_id');
    const functionUrl = `https://us-central1-yt-summaries-1984.cloudfunctions.net/getVideo?video_id=${videoId}`;

    if (!videoId) {
        videoDetails.innerHTML = "<p>No video ID provided.</p>";
        return;
    }

    const formatDuration = (seconds) => {
        const h = Math.floor(seconds / 3600).toString().padStart(2, '0');
        const m = Math.floor((seconds % 3600) / 60).toString().padStart(2, '0');
        const s = Math.floor(seconds % 60).toString().padStart(2, '0');
        return `${h}:${m}:${s}`;
    };

    fetch(functionUrl)
        .then(response => response.json())
        .then(data => {
            const { metadata, summary } = data;

            let metadataHtml = "";
            if (metadata) {
                metadataHtml += "<div>";
                if (metadata.title) {
                    metadataHtml += `<h1>${metadata.title}</h1>`;
                }
                if (metadata.uploader) {
                    metadataHtml += `<p><strong>Uploader:</strong> ${metadata.uploader}</p>`;
                }
                if (metadata.upload_date) {
                    const dateStr = metadata.upload_date;
                    const year = dateStr.substring(0, 4);
                    const month = dateStr.substring(4, 6);
                    const day = dateStr.substring(6, 8);
                    metadataHtml += `<p><strong>Upload Date:</strong> ${new Date(year, month - 1, day).toLocaleDateString()}</p>`;
                }
                if (metadata.duration) {
                    metadataHtml += `<p><strong>Duration:</strong> ${formatDuration(metadata.duration)}</p>`;
                }
                if (metadata.description) {
                    const desc_lines = metadata.description.split('\n');
                    const formatted_desc = desc_lines.slice(0, 5).join('<br>') + (desc_lines.length > 5 ? '...' : '');
                    metadataHtml += `<p><strong>Description:</strong><br>${formatted_desc}</p>`;
                }
                metadataHtml += "<hr></div>";
            }

            videoDetails.innerHTML = metadataHtml;
            videoDetails.innerHTML += marked.parse(summary);
        })
        .catch(error => {
            console.error("Error fetching video details:", error);
            videoDetails.innerHTML = "<p>Error loading video details. Please try again later.</p>";
        });
});
