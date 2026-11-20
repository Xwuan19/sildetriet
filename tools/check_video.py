# -*- coding: utf-8 -*-
import sys
from pathlib import Path

video_path = Path(r"C:\Users\ADMIN\Downloads\Mẫu Slide Triết học Mác – Lênin： Quan điểm của chủ nghĩa Mác – Lênin về Nhà nước - Tuyệt Kỹ Powerpoint (1080p, h264).mp4")
print("Video exists:", video_path.exists())
if video_path.exists():
    print("Size (MB):", round(video_path.stat().st_size / (1024 * 1024), 2))

# check ffmpeg or cv2
import shutil
print("ffmpeg in PATH:", shutil.which("ffmpeg"))

try:
    import cv2
    print("cv2 version:", cv2.__version__)
except ImportError:
    print("cv2 not installed")
