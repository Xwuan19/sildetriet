import subprocess
import imageio_ffmpeg

ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
cmd = [
    ffmpeg, "-y",
    "-ss", "5.0",
    "-i", "preview_red/morph_preview.mp4",
    "-t", "3.0",
    "-vf", "fps=3",
    "preview_red/morph_t5_%02d.png"
]
subprocess.run(cmd, check=True)
print("Extracted morph_t5!")
