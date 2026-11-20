import subprocess
from PIL import Image

ffmpeg = r"C:\Users\ADMIN\AppData\Local\Programs\Python\Python315\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v9.0.2.exe"
video = r"C:\Users\ADMIN\Downloads\Mẫu Slide Triết học Mác – Lênin： Quan điểm của chủ nghĩa Mác – Lênin về Nhà nước - Tuyệt Kỹ Powerpoint (1080p, h264).mp4"
BOX = (120, 70, 1800, 1015)

for t in [6.60, 6.65, 6.70, 6.75, 6.80, 6.85, 6.90]:
    out = f"preview_red/lenin_clean_t_{t:.2f}.png"
    subprocess.run([ffmpeg, "-y", "-ss", str(t), "-i", video, "-vframes", "1", out], capture_output=True)
    try:
        im = Image.open(out).crop(BOX)
        im.save(f"preview_red/crop_clean_t_{t:.2f}.png")
    except Exception:
        pass

print("Extracted micro frames.")
