# -*- coding: utf-8 -*-
import subprocess

ffmpeg = r"C:\Users\ADMIN\AppData\Local\Programs\Python\Python315\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v9.0.2.exe"

# Extract transition 1 (Slide 1 -> Slide 2): at 3.5s, 4.0s, 4.5s
# Extract transition 2 (Slide 2 -> Slide 3): at 8.5s, 9.0s, 9.5s
timestamps = [1.0, 3.8, 4.2, 4.8, 6.5, 8.8, 9.2, 9.8, 12.0]
for i, t in enumerate(timestamps):
    out = f"preview_red/morph_test_frame_{i+1:02d}.jpg"
    cmd = [ffmpeg, "-y", "-ss", str(t), "-i", "preview_red/morph_preview.mp4", "-vframes", "1", "-vf", "scale=960:540", out]
    subprocess.run(cmd, capture_output=True)
print("Extracted test frames!")
