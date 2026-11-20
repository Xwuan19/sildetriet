import subprocess

ffmpeg = r"C:\Users\ADMIN\AppData\Local\Programs\Python\Python315\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v9.0.2.exe"
video = r"C:\Users\ADMIN\Downloads\Mẫu Slide Triết học Mác – Lênin： Quan điểm của chủ nghĩa Mác – Lênin về Nhà nước - Tuyệt Kỹ Powerpoint (1080p, h264).mp4"

for sec in [5.0, 5.5, 6.0, 6.2]:
    out = f"preview_red/slide1_t{sec:.1f}.png"
    cmd = [ffmpeg, "-y", "-ss", str(sec), "-i", video, "-vframes", "1", out]
    subprocess.run(cmd, capture_output=True)

print("Extracted 5.0 to 6.2")
