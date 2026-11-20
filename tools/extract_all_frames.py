# -*- coding: utf-8 -*-
import subprocess
from pathlib import Path
import imageio_ffmpeg

ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
video = Path(r"C:\Users\ADMIN\Downloads\Mẫu Slide Triết học Mác – Lênin： Quan điểm của chủ nghĩa Mác – Lênin về Nhà nước - Tuyệt Kỹ Powerpoint (1080p, h264).mp4")
out_dir = Path("video_analysis/frames")
out_dir.mkdir(parents=True, exist_ok=True)

# Extract 2 frames per second (1 frame every 0.5s)
cmd = [
    ffmpeg, "-y",
    "-i", str(video),
    "-vf", "fps=2",
    "-q:v", "2",
    str(out_dir / "frame_%04d.jpg")
]
print("Extracting frames...")
res = subprocess.run(cmd, capture_output=True, text=True)
frames = list(out_dir.glob("frame_*.jpg"))
print(f"Extracted {len(frames)} frames to {out_dir}")
