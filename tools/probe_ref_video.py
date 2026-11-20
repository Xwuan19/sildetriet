import subprocess
import json
import imageio_ffmpeg

ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
video = r"C:\Users\ADMIN\Downloads\Mẫu Slide Triết học Mác – Lênin： Quan điểm của chủ nghĩa Mác – Lênin về Nhà nước - Tuyệt Kỹ Powerpoint (1080p, h264).mp4"

# Use ffprobe or ffmpeg to get video info
cmd = [ffmpeg, "-i", video]
res = subprocess.run(cmd, stderr=subprocess.PIPE, text=True, encoding="utf-8", errors="ignore")
print(res.stderr)
