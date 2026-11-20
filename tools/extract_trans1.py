# -*- coding: utf-8 -*-
import subprocess

ffmpeg = r"C:\Users\ADMIN\AppData\Local\Programs\Python\Python315\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v9.0.2.exe"

# Extract transition 1: from 4.0s to 6.2s, 5 fps (one frame every 0.2s)
cmd = [
    ffmpeg, "-y", "-ss", "4.0", "-to", "6.2",
    "-i", "preview_red/morph_preview.mp4",
    "-vf", "fps=5,scale=960:540",
    "preview_red/trans1_%02d.jpg"
]
subprocess.run(cmd, check=True)
print("Extracted trans1 frames!")
