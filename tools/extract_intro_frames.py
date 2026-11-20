import subprocess
import imageio_ffmpeg
from pathlib import Path

ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
video = r"C:\Users\ADMIN\Downloads\Mẫu Slide Triết học Mác – Lênin： Quan điểm của chủ nghĩa Mác – Lênin về Nhà nước - Tuyệt Kỹ Powerpoint (1080p, h264).mp4"
out_dir = Path("preview_red/intro_frames")
out_dir.mkdir(parents=True, exist_ok=True)

# Extract 0.0s to 10.0s at 10 fps (100 frames)
subprocess.run([
    ffmpeg, "-y",
    "-ss", "0.0",
    "-i", video,
    "-t", "10.0",
    "-vf", "fps=10",
    str(out_dir / "f_%03d.png")
], check=True)
print("Extracted 100 intro frames!")
