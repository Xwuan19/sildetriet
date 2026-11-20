# Inspect what the video is showing between 0s and 6s
import subprocess

ffmpeg = r"C:\Users\ADMIN\AppData\Local\Programs\Python\Python315\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v9.0.2.exe"
video = r"C:\Users\ADMIN\Downloads\Mẫu Slide Triết học Mác – Lênin： Quan điểm của chủ nghĩa Mác – Lênin về Nhà nước - Tuyệt Kỹ Powerpoint (1080p, h264).mp4"

for sec in [0.5, 1.5, 2.5, 3.5, 4.5, 5.5]:
    out = f"preview_red/intro_sequence/time_{sec:.1f}.jpg"
    cmd = [ffmpeg, "-y", "-ss", str(sec), "-i", video, "-vframes", "1", "-vf", "scale=960:540", out]
    subprocess.run(cmd, capture_output=True)
print("Extracted key time frames.")
