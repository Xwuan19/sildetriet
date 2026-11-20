import subprocess
import imageio_ffmpeg
from pathlib import Path

ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
video = r"C:\Users\ADMIN\Downloads\Mẫu Slide Triết học Mác – Lênin： Quan điểm của chủ nghĩa Mác – Lênin về Nhà nước - Tuyệt Kỹ Powerpoint (1080p, h264).mp4"
out_dir = Path("preview_red/trans_analysis_frames")
out_dir.mkdir(parents=True, exist_ok=True)

# Extract from t=3.8s to t=8.8s at 30 fps (150 frames)
subprocess.run([
    ffmpeg, "-y",
    "-ss", "3.8",
    "-i", video,
    "-t", "5.0",
    "-vf", "fps=30",
    str(out_dir / "frame_%04d.png")
], check=True)
print("Extracted 150 transition frames!")
