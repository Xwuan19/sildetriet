import subprocess
import imageio_ffmpeg
from pathlib import Path

ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
video = r"C:\Users\ADMIN\Downloads\Mẫu Slide Triết học Mác – Lênin： Quan điểm của chủ nghĩa Mác – Lênin về Nhà nước - Tuyệt Kỹ Powerpoint (1080p, h264).mp4"
out_dir = Path("preview_red/intro_slideshow")
out_dir.mkdir(parents=True, exist_ok=True)

# Extract from 4.5s to 6.5s at 10 fps
subprocess.run([
    ffmpeg, "-y",
    "-ss", "4.5",
    "-i", video,
    "-t", "2.0",
    "-vf", "fps=10",
    str(out_dir / "s_%03d.png")
], check=True)

print("Extracted intro slideshow frames!")
