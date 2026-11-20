import subprocess
import imageio_ffmpeg

ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
cmd = [
    ffmpeg, "-y",
    "-ss", "7.0",
    "-i", "preview_red/morph_preview.mp4",
    "-t", "8.0",
    "-vf", "fps=2",
    "preview_red/trans23_%02d.png"
]
subprocess.run(cmd, check=True)
print("Extracted trans23!")
