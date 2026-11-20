import subprocess
import imageio_ffmpeg

ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
cmd = [
    ffmpeg, "-y",
    "-i", "preview_red/morph_preview.mp4",
    "-vf", "fps=1",
    "-vframes", "10",
    "preview_red/vframe_%02d.png"
]
subprocess.run(cmd, check=True)
print("Extracted frames!")
