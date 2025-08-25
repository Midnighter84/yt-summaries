document.addEventListener("DOMContentLoaded", () => {
    const videoDetails = document.getElementById("video-details");
    const loader = document.getElementById("loader");
    const archiveButtons = document.getElementById("archive-buttons");
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
            loader.style.display = "none";
            videoDetails.style.display = "block";

            const { metadata, summary, is_archived } = data;

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

            let current_is_archived = is_archived;
            const archiveButton = document.createElement("button");
            archiveButton.textContent = current_is_archived ? "Unarchive" : "Archive";
            archiveButton.addEventListener("click", () => {
                const action = current_is_archived ? "unarchive" : "archive";
                const modifyUrl = `https://us-central1-yt-summaries-1984.cloudfunctions.net/modifyVideo?video_id=${videoId}&action=${action}`;
                fetch(modifyUrl)
                    .then(() => {
                        current_is_archived = !current_is_archived;
                        archiveButton.textContent = current_is_archived ? "Unarchive" : "Archive";
                    })
                    .catch(error => {
                        console.error("Error modifying video:", error);
                    });
            });
            archiveButtons.appendChild(archiveButton);

            const backButton = document.createElement("button");
            backButton.textContent = "Back to all videos";
            backButton.addEventListener("click", () => {
                window.location.href = "index.html";
            });
            archiveButtons.appendChild(backButton);
        })
        .catch(error => {
            console.error("Error fetching video details:", error);
            loader.style.display = "none";
            videoDetails.innerHTML = "<p>Could not load video.</p>";
            videoDetails.style.display = "block";

            let current_is_archived = false;
            const archiveButton = document.createElement("button");
            archiveButton.textContent = "Archive";
            archiveButton.addEventListener("click", () => {
                const action = current_is_archived ? "unarchive" : "archive";
                const modifyUrl = `https://us-central1-yt-summaries-1984.cloudfunctions.net/modifyVideo?video_id=${videoId}&action=${action}`;
                fetch(modifyUrl)
                    .then(() => {
                        current_is_archived = !current_is_archived;
                        archiveButton.textContent = current_is_archived ? "Unarchive" : "Archive";
                    })
                    .catch(error => {
                        console.error("Error modifying video:", error);
                    });
            });
            archiveButtons.appendChild(archiveButton);

            const backButton = document.createElement("button");
            backButton.textContent = "Back to all videos";
            backButton.addEventListener("click", () => {
                window.location.href = "index.html";
            });
            archiveButtons.appendChild(backButton);
        });
});
