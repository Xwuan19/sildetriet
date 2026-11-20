import subprocess
import imageio_ffmpeg

ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
video = r"C:\Users\ADMIN\Downloads\Mẫu Slide Triết học Mác – Lênin： Quan điểm của chủ nghĩa Mác – Lênin về Nhà nước - Tuyệt Kỹ Powerpoint (1080p, h264).mp4"

cmd = [
    ffmpeg, "-y",
    "-ss", "6",
    "-i", video,
    "-t", "20",
    "-vf", "fps=1",
    "preview_red/orig_slide_%02d.png"
]
subprocess.run(cmd, check=True)
print("Extracted orig_slide frames!")
