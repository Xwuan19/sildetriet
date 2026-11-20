import subprocess

ffmpeg = r"C:\Users\ADMIN\AppData\Local\Programs\Python\Python315\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v9.0.2.exe"
video = r"C:\Users\ADMIN\Downloads\Mẫu Slide Triết học Mác – Lênin： Quan điểm của chủ nghĩa Mác – Lênin về Nhà nước - Tuyệt Kỹ Powerpoint (1080p, h264).mp4"

# Check 0.0s to 5.0s in steps of 0.25s
for t in [0.0, 0.25, 0.75, 1.0, 2.0, 3.0, 4.0]:
    out = f"preview_red/frame_sec_{t:.2f}.png"
    subprocess.run([ffmpeg, "-y", "-ss", str(t), "-i", video, "-vframes", "1", out], capture_output=True)

print("Extracted sec frames.")
