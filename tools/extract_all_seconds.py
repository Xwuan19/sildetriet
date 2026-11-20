import subprocess
import imageio_ffmpeg
from pathlib import Path

ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
video = r"C:\Users\ADMIN\Downloads\Mẫu Slide Triết học Mác – Lênin： Quan điểm của chủ nghĩa Mác – Lênin về Nhà nước - Tuyệt Kỹ Powerpoint (1080p, h264).mp4"
out_dir = Path("preview_red/all_seconds")
out_dir.mkdir(parents=True, exist_ok=True)

subprocess.run([
    ffmpeg, "-y",
    "-i", video,
    "-vf", "fps=1",
    str(out_dir / "sec_%03d.png")
], check=True)
print("Extracted 1 fps across whole video!")
