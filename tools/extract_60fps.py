import subprocess
import imageio_ffmpeg
from pathlib import Path
from PIL import Image

ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
video = r"C:\Users\ADMIN\Downloads\Mẫu Slide Triết học Mác – Lênin： Quan điểm của chủ nghĩa Mác – Lênin về Nhà nước - Tuyệt Kỹ Powerpoint (1080p, h264).mp4"

# Let's extract frames at 60 fps (16.67 ms per frame) for the main transitions!
# Transition 1: Slide 1 -> Slide 2 is around 5.5s to 8.5s
out_dir = Path("preview_red/video_60fps_t1")
out_dir.mkdir(parents=True, exist_ok=True)

subprocess.run([
    ffmpeg, "-y",
    "-ss", "5.5",
    "-i", video,
    "-t", "3.0",
    "-vf", "fps=60",
    str(out_dir / "f60_%04d.png")
], check=True)

frames = sorted(list(out_dir.glob("f60_*.png")))
print(f"Extracted {len(frames)} frames at 60fps (16.67 ms per frame)!")
