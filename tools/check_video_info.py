import subprocess
import imageio_ffmpeg

ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
video = r"C:\Users\ADMIN\Downloads\Mẫu Slide Triết học Mác – Lênin： Quan điểm của chủ nghĩa Mác – Lênin về Nhà nước - Tuyệt Kỹ Powerpoint (1080p, h264).mp4"

res = subprocess.run([ffmpeg, "-i", video], stderr=subprocess.PIPE, text=True)
for line in res.stderr.splitlines():
    if "Duration" in line or "Stream #0" in line:
        print(line)
