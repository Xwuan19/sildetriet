# -*- coding: utf-8 -*-
import json
import subprocess
import sys
from pathlib import Path
import imageio_ffmpeg

ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
video = Path(r"C:\Users\ADMIN\Downloads\Mẫu Slide Triết học Mác – Lênin： Quan điểm của chủ nghĩa Mác – Lênin về Nhà nước - Tuyệt Kỹ Powerpoint (1080p, h264).mp4")

out_dir = Path("video_analysis/frames")
out_dir.mkdir(parents=True, exist_ok=True)

# Run ffmpeg to get video info
cmd_info = [ffmpeg, "-i", str(video)]
res = subprocess.run(cmd_info, capture_output=True, text=True, errors="replace")
print("Video Info:\n", res.stderr[:1000])

# Extract frames at 1 fps (1 frame per second) or 2 fps (0.5s per frame)
# User specifically requested: "hãy tách từng frame 0.5frame/1 giây hoặc nhiều frame hơn nữa"
# 1 frame every 0.5s = 2 fps! Let's do 2 fps (1 frame per 0.5 second) or 1 fps if video is long.
# Let's check duration first.
