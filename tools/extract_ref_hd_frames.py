import subprocess
import imageio_ffmpeg
from pathlib import Path

ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
video = r"C:\Users\ADMIN\Downloads\Mẫu Slide Triết học Mác – Lênin： Quan điểm của chủ nghĩa Mác – Lênin về Nhà nước - Tuyệt Kỹ Powerpoint (1080p, h264).mp4"
out_dir = Path("preview_red/ref_frames_hd")
out_dir.mkdir(parents=True, exist_ok=True)

# Extract from t=5.0s to t=9.5s at 30 fps (4.5s * 30 = 135 frames)
cmd = [
    ffmpeg, "-y",
    "-ss", "5.0",
    "-i", video,
    "-t", "4.5",
    "-vf", "fps=30",
    str(out_dir / "f_%04d.png")
]
subprocess.run(cmd, check=True)
print("Extracted HD frames successfully!")
