import subprocess
import imageio_ffmpeg
from pathlib import Path

ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
video = r"C:\Users\ADMIN\Downloads\Mẫu Slide Triết học Mác – Lênin： Quan điểm của chủ nghĩa Mác – Lênin về Nhà nước - Tuyệt Kỹ Powerpoint (1080p, h264).mp4"
out_dir = Path("preview_red/edit_mode_1080p")
out_dir.mkdir(parents=True, exist_ok=True)

for sec in [1.5, 2.5, 3.5, 4.2]:
    subprocess.run([
        ffmpeg, "-y",
        "-ss", str(sec),
        "-i", video,
        "-vframes", "1",
        str(out_dir / f"edit_{sec}.png")
    ], check=True)

print("Extracted edit mode 1080p frames!")
