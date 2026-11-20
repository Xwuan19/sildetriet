# -*- coding: utf-8 -*-
import subprocess
from pathlib import Path
import imageio_ffmpeg

ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
video = Path(r"C:\Users\ADMIN\Downloads\Mẫu Slide Triết học Mác – Lênin： Quan điểm của chủ nghĩa Mác – Lênin về Nhà nước - Tuyệt Kỹ Powerpoint (1080p, h264).mp4")
out_dir = Path("video_analysis/transition_1_2")
out_dir.mkdir(parents=True, exist_ok=True)

# Extract transition 1->2 between 5.5s and 8.0s at 8 fps
cmd = [
    ffmpeg, "-y",
    "-ss", "00:00:05.500",
    "-to", "00:00:08.000",
    "-i", str(video),
    "-vf", "fps=8",
    "-q:v", "2",
    str(out_dir / "t12_%03d.jpg")
]
subprocess.run(cmd, capture_output=True, text=True)

# Extract transition 2->3 between 9.5s and 12.0s at 8 fps
out_dir2 = Path("video_analysis/transition_2_3")
out_dir2.mkdir(parents=True, exist_ok=True)
cmd2 = [
    ffmpeg, "-y",
    "-ss", "00:00:09.500",
    "-to", "00:00:12.000",
    "-i", str(video),
    "-vf", "fps=8",
    "-q:v", "2",
    str(out_dir2 / "t23_%03d.jpg")
]
subprocess.run(cmd2, capture_output=True, text=True)

# Extract ending transition between 54.5s and 57.5s at 8 fps
out_dir3 = Path("video_analysis/transition_end")
out_dir3.mkdir(parents=True, exist_ok=True)
cmd3 = [
    ffmpeg, "-y",
    "-ss", "00:00:54.500",
    "-to", "00:00:57.500",
    "-i", str(video),
    "-vf", "fps=8",
    "-q:v", "2",
    str(out_dir3 / "tend_%03d.jpg")
]
subprocess.run(cmd3, capture_output=True, text=True)

print("Done extracting high-speed transition frames.")
