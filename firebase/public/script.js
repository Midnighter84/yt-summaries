document.addEventListener("DOMContentLoaded", () => {
    const videoList = document.getElementById("video-list");
    const loader = document.getElementById("loader");
    const functionUrl = "https://us-central1-yt-summaries-1984.cloudfunctions.net/getSummaries";

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
            videoList.style.display = "block";

            if (data.length === 0) {
                videoList.innerHTML = "<p>No summaries found.</p>";
                return;
            }

            data.forEach(video => {
                const link = document.createElement("a");
                link.href = `video.html?video_id=${video.id}`;
                link.className = "video-link";

                const videoItem = document.createElement("div");
                videoItem.className = "video-item";

                const title = document.createElement("h2");
                title.textContent = video.title;

                const channel = document.createElement("p");
                channel.textContent = `Channel: ${video.uploader}`;

                const uploadDate = document.createElement("p");
                const dateStr = video.upload_date;
                const year = dateStr.substring(0, 4);
                const month = dateStr.substring(4, 6);
                const day = dateStr.substring(6, 8);
                uploadDate.textContent = `Uploaded: ${new Date(year, month - 1, day).toLocaleDateString()}`;

                const duration = document.createElement("p");
                duration.textContent = `Duration: ${formatDuration(video.duration)}`;

                videoItem.appendChild(title);
                videoItem.appendChild(channel);
                videoItem.appendChild(uploadDate);
                videoItem.appendChild(duration);

                link.appendChild(videoItem);
                videoList.appendChild(link);
            });
        })
        .catch(error => {
            console.error("Error fetching summaries:", error);
            loader.style.display = "none";
            videoList.innerHTML = "<p>Error loading summaries. Please try again later.</p>";
        });
});
