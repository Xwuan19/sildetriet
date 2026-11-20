import subprocess
import imageio_ffmpeg

ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
cmd = [
    ffmpeg, "-y",
    "-ss", "5.8",
    "-i", "preview_red/morph_preview.mp4",
    "-t", "1.5",
    "-vf", "fps=4",
    "preview_red/trans12_%02d.png"
]
subprocess.run(cmd, check=True)
print("Extracted trans12!")
