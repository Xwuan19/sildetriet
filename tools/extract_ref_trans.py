import subprocess
import imageio_ffmpeg

ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
video = r"C:\Users\ADMIN\Downloads\Mẫu Slide Triết học Mác – Lênin： Quan điểm của chủ nghĩa Mác – Lênin về Nhà nước - Tuyệt Kỹ Powerpoint (1080p, h264).mp4"

cmd = [
    ffmpeg, "-y",
    "-ss", "4.0",
    "-i", video,
    "-t", "12.0",
    "-vf", "fps=2",
    "preview_red/ref_trans_%03d.png"
]
subprocess.run(cmd, check=True)
print("Extracted ref_trans!")
