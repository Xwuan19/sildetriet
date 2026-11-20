# -*- coding: utf-8 -*-
import subprocess
from pathlib import Path
import imageio_ffmpeg

ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
video = Path(r"C:\Users\ADMIN\Downloads\Mẫu Slide Triết học Mác – Lênin： Quan điểm của chủ nghĩa Mác – Lênin về Nhà nước - Tuyệt Kỹ Powerpoint (1080p, h264).mp4")

cmd_info = [ffmpeg, "-i", str(video)]
res = subprocess.run(cmd_info, capture_output=True, text=True, errors="replace")
for line in res.stderr.splitlines():
    if "Duration" in line or "Stream #" in line:
        print(line)
