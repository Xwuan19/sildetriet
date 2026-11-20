import subprocess
from pathlib import Path
import imageio_ffmpeg
from PIL import Image

ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
video = r"C:\Users\ADMIN\Downloads\Mẫu Slide Triết học Mác – Lênin： Quan điểm của chủ nghĩa Mác – Lênin về Nhà nước - Tuyệt Kỹ Powerpoint (1080p, h264).mp4"
out_dir = Path("preview_red/ref_overview")
out_dir.mkdir(parents=True, exist_ok=True)

# 1 frame per second across 57 seconds
subprocess.run([
    ffmpeg, "-y",
    "-i", video,
    "-vf", "fps=1",
    str(out_dir / "sec_%02d.png")
], check=True)

# Create contact sheets of 10 images each
for chunk_idx in range(6):
    sheet = Image.new("RGB", (5 * 384, 2 * 216))
    for i in range(10):
        sec = chunk_idx * 10 + i
        p = out_dir / f"sec_{sec:02d}.png"
        if p.exists():
            im = Image.open(p).resize((384, 216))
            r = i // 5
            c = i % 5
            sheet.paste(im, (c * 384, r * 216))
    sheet.save(f"preview_red/ref_overview_chunk_{chunk_idx}.png")

print("Created overview chunks!")
