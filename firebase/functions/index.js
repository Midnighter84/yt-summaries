const {onRequest} = require("firebase-functions/v2/https");
const logger = require("firebase-functions/logger");
const admin = require("firebase-admin");
const cors = require("cors")({origin: true});

admin.initializeApp();

exports.getSummaries = onRequest((req, res) => {
  cors(req, res, async () => {
    try {
      const bucket = admin.storage().bucket();
      const [files] = await bucket.getFiles({prefix: "video-metadata/"});
      const metadatas = [];

      logger.info(`Found ${files.length} files in video-metadata/`);

      const promises = files.map((file) => {
        return new Promise((resolve, reject) => {
          if (file.name.endsWith(".json")) {
            const stream = file.createReadStream();
            let buffer = "";
            stream.on("data", (chunk) => {
              buffer += chunk.toString();
            });
            stream.on("end", () => {
              try {
                const metadata = JSON.parse(buffer);
                const videoId = file.name.split("/").pop().replace(".json", "");
                metadata.id = videoId;
                metadatas.push(metadata);
                resolve();
              } catch (e) {
                logger.error(`Error parsing JSON from ${file.name}`, e);
                reject(e);
              }
            });
            stream.on("error", (err) => {
              logger.error(`Error reading file ${file.name}`, err);
              reject(err);
            });
          } else {
            resolve();
          }
        });
      });

      await Promise.all(promises);

      logger.info(`Successfully processed ${metadatas.length} metadata files.`);
      res.status(200).json(metadatas);
    } catch (error) {
      logger.error("Error getting summaries:", error);
      res.status(500).send("Internal Server Error");
    }
  });
});

exports.getVideo = onRequest((req, res) => {
  cors(req, res, async () => {
    try {
      const videoId = req.query.video_id;
      if (!videoId) {
        res.status(400).send("Missing video_id parameter");
        return;
      }

      const bucket = admin.storage().bucket();

      const metadataFile = bucket.file(`video-metadata/${videoId}.json`);
      const summaryFile = bucket.file(`summaries/${videoId}.md`);

      const [metadataExists] = await metadataFile.exists();
      const [summaryExists] = await summaryFile.exists();

      if (!metadataExists) {
        res.status(404).send("Video metadata not found");
        return;
      }

      if (!summaryExists) {
        res.status(404).send("Video summary not found");
        return;
      }

      const metadataBuffer = await metadataFile.download();
      const summaryBuffer = await summaryFile.download();

      const metadata = JSON.parse(metadataBuffer.toString());
      const summary = summaryBuffer.toString();

      res.status(200).json({ metadata, summary });
    } catch (error) {
      logger.error("Error getting video:", error);
      res.status(500).send("Internal Server Error");
    }
  });
});
