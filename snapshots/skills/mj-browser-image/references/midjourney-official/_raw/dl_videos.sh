#!/bin/bash
cd "/c/Users/Administrator/Desktop/碎片之城项目/88_临时/midjourney-official"
mkdir -p assets/videos
while read id; do
  [ -z "$id" ] && continue
  if [ -f "assets/videos/v_${id}.mp4" ]; then echo "SKIP $id"; continue; fi
  echo "=== $id ==="
  timeout 600 python -m yt_dlp --js-runtimes node \
    -f "bv*[height<=720][ext=mp4]+ba[ext=m4a]/b[height<=720]/b" \
    --merge-output-format mp4 \
    -o "assets/videos/v_${id}.%(ext)s" \
    "https://youtu.be/${id}" 2>&1 | grep -E "Merging|ERROR|Downloading 1 format" | head -3
done < /tmp/ytids.txt
echo "ALL_DONE"
ls -lh assets/videos/
