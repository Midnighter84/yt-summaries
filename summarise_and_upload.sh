video_key="$1"
echo $video_key
python main.py https://www.youtube.com/watch?v=$video_key
cp data/summaries/$video_key.html firebase/public/
cd firebase && firebase deploy && cd ..