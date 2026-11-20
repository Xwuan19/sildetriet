import subprocess
from PIL import Image

ffmpeg = r"C:\Users\ADMIN\AppData\Local\Programs\Python\Python315\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v9.0.2.exe"
video = r"C:\Users\ADMIN\Downloads\Mẫu Slide Triết học Mác – Lênin： Quan điểm của chủ nghĩa Mác – Lênin về Nhà nước - Tuyệt Kỹ Powerpoint (1080p, h264).mp4"
BOX = (120, 70, 1800, 1015)

# Let's sample every 3 seconds throughout the video (from 0 to 60s)
for sec in range(2, 60, 4):
    out = f"preview_red/slide_t{sec:02d}.png"
    cmd = [ffmpeg, "-y", "-ss", str(sec), "-i", video, "-vframes", "1", out]
    subprocess.run(cmd, capture_output=True)
    try:
        im = Image.open(out)
        crop = im.crop(BOX)
        crop.save(f"preview_red/crop_t{sec:02d}.png")
    except Exception as e:
        pass

print("Sampled and cropped slides across video.")
