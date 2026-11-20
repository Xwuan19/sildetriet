# -*- coding: utf-8 -*-
import subprocess

cmd = [
    "ffmpeg", "-y", "-i", "preview_red/test_3d_morph.mp4",
    "-vf", "fps=3,scale=640:-1,tile=3x3",
    "preview_red/test_3d_frames.jpg"
]
res = subprocess.run(cmd, capture_output=True, text=True)
print("FFmpeg done:", res.returncode)
