import subprocess

ffmpeg = r"C:\Users\ADMIN\AppData\Local\Programs\Python\Python315\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v9.0.2.exe"
video = r"C:\Users\ADMIN\Downloads\Mẫu Slide Triết học Mác – Lênin： Quan điểm của chủ nghĩa Mác – Lênin về Nhà nước - Tuyệt Kỹ Powerpoint (1080p, h264).mp4"

# Let's extract frames at 0.5s, 1.0s, 1.5s, 2.0s, 2.5s, 3.0s, 3.5s, 4.0s, 4.5s at full 1920x1080
for t in [0.5, 1.5, 2.5, 3.5, 4.5]:
    out = f"preview_red/tut_frame_{t:.1f}.png"
    cmd = [ffmpeg, "-y", "-ss", str(t), "-i", video, "-vframes", "1", out]
    subprocess.run(cmd, capture_output=True)

print("Extracted tutorial frames at full 1080p.")
