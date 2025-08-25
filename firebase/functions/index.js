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

      const db = admin.firestore();
      const videoPropertiesCollection = db.collection("video_properties");

      const promises = files.map(async (file) => {
        if (file.name.endsWith(".json")) {
          const videoId = file.name.split("/").pop().replace(".json", "");
          const doc = await videoPropertiesCollection.doc(videoId).get();

          if (doc.exists && doc.data().is_archived) {
            return;
          }

          const stream = file.createReadStream();
          let buffer = "";
          await new Promise((resolve, reject) => {
            stream.on("data", (chunk) => {
              buffer += chunk.toString();
            });
            stream.on("end", () => {
              try {
                const metadata = JSON.parse(buffer);
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
          });
        }
      });

      await Promise.all(promises);

      metadatas.sort((a, b) => {
        //const dateA = new Date(a.upload_date);
        //const dateB = new Date(b.upload_date);
        return b - a;
      });

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

      const db = admin.firestore();
      const videoPropertiesRef = db.collection("video_properties").doc(videoId);
      const doc = await videoPropertiesRef.get();

      let isArchived = false;
      if (doc.exists) {
        isArchived = doc.data().is_archived || false;
      }

      res.status(200).json({ metadata, summary, is_archived: isArchived });
    } catch (error) {
      logger.error("Error getting video:", error);
      res.status(500).send("Internal Server Error");
    }
  });
});

exports.modifyVideo = onRequest((req, res) => {
  cors(req, res, async () => {
    try {
      const videoId = req.query.video_id;
      const action = req.query.action;

      if (!videoId || !action) {
        res.status(400).send("Missing video_id or action parameter");
        return;
      }

      if (action !== "archive" && action !== "unarchive") {
        res.status(400).send("Invalid action parameter");
        return;
      }

      const isArchived = action === "archive";

      const db = admin.firestore();
      const videoPropertiesRef = db.collection("video_properties").doc(videoId);

      await videoPropertiesRef.set({
        is_archived: isArchived,
      }, { merge: true });

      res.status(200).send(`Video ${videoId} has been ${action}d.`);
    } catch (error) {
      logger.error("Error modifying video:", error);
      res.status(500).send("Internal Server Error");
    }
  });
});
