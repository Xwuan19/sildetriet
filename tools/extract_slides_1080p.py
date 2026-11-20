import subprocess
from PIL import Image

ffmpeg = r"C:\Users\ADMIN\AppData\Local\Programs\Python\Python315\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v9.0.2.exe"
video = r"C:\Users\ADMIN\Downloads\Mẫu Slide Triết học Mác – Lênin： Quan điểm của chủ nghĩa Mác – Lênin về Nhà nước - Tuyệt Kỹ Powerpoint (1080p, h264).mp4"

# Extract frame at 7.0s at full 1920x1080
out = "preview_red/slide1_full_1080p.png"
cmd = [ffmpeg, "-y", "-ss", "7.0", "-i", video, "-vframes", "1", out]
subprocess.run(cmd, capture_output=True)

# Also extract slide 2 at 8.5s
out2 = "preview_red/slide2_full_1080p.png"
cmd2 = [ffmpeg, "-y", "-ss", "8.5", "-i", video, "-vframes", "1", out2]
subprocess.run(cmd2, capture_output=True)

print("Extracted 7.0s and 8.5s at full 1080p")
