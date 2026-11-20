import subprocess
from PIL import Image

ffmpeg = r"C:\Users\ADMIN\AppData\Local\Programs\Python\Python315\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v9.0.2.exe"
video = r"C:\Users\ADMIN\Downloads\Mẫu Slide Triết học Mác – Lênin： Quan điểm của chủ nghĩa Mác – Lênin về Nhà nước - Tuyệt Kỹ Powerpoint (1080p, h264).mp4"
BOX = (120, 70, 1800, 1015)

for t in [0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.5, 2.0]:
    out = f"preview_red/intro_sequence/anim_{t:.1f}.png"
    cmd = [ffmpeg, "-y", "-ss", str(t), "-i", video, "-vframes", "1", out]
    subprocess.run(cmd, capture_output=True)
    try:
        im = Image.open(out).crop(BOX)
        im.save(f"preview_red/intro_sequence/anim_crop_{t:.1f}.png")
    except Exception:
        pass

print("Extracted early animation frames.")
