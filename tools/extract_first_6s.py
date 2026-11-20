import subprocess
import imageio_ffmpeg
from pathlib import Path

ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
video = r"C:\Users\ADMIN\Downloads\Mẫu Slide Triết học Mác – Lênin： Quan điểm của chủ nghĩa Mác – Lênin về Nhà nước - Tuyệt Kỹ Powerpoint (1080p, h264).mp4"
out_dir = Path("preview_red/video_first_6s")
out_dir.mkdir(parents=True, exist_ok=True)

# Extract 1 frame every 0.25s from 0 to 6s (24 frames)
subprocess.run([
    ffmpeg, "-y",
    "-ss", "0",
    "-i", video,
    "-t", "6.5",
    "-vf", "fps=4",
    str(out_dir / "f_%03d.png")
], check=True)

print("Extracted first 6.5s at 4fps!")
