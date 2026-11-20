import subprocess
import imageio_ffmpeg
from pathlib import Path

ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
video = r"C:\Users\ADMIN\Downloads\Mẫu Slide Triết học Mác – Lênin： Quan điểm của chủ nghĩa Mác – Lênin về Nhà nước - Tuyệt Kỹ Powerpoint (1080p, h264).mp4"
out_dir = Path("preview_red/exact_start_50fps")
out_dir.mkdir(parents=True, exist_ok=True)

# Extract from 5.8s to 7.8s (100 frames at 50fps = 20ms each)
subprocess.run([
    ffmpeg, "-y",
    "-ss", "5.8",
    "-i", video,
    "-t", "2.0",
    "-vf", "fps=50",
    str(out_dir / "frame_%04d.png")
], check=True)

frames = sorted(list(out_dir.glob("frame_*.png")))
print(f"Extracted {len(frames)} frames from 5.8s!")
