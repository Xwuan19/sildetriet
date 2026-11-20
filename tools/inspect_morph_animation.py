# -*- coding: utf-8 -*-
"""Extract frames and create contact sheet of PowerPoint's exported morph video."""
import subprocess
from pathlib import Path
from PIL import Image

FFMPEG = r"C:\Users\ADMIN\AppData\Local\Programs\Python\Python315\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v9.0.2.exe"
ROOT = Path(__file__).resolve().parent.parent
MP4 = ROOT / "preview_red" / "morph_preview.mp4"
FRAMES_DIR = ROOT / "preview_red" / "morph_frames"
FRAMES_DIR.mkdir(parents=True, exist_ok=True)

# Clean old frames
for f in FRAMES_DIR.glob("*.jpg"):
    f.unlink()

# Extract 1 frame per second across the 15s video
cmd = [
    FFMPEG, "-y",
    "-i", str(MP4),
    "-vf", "fps=1",
    str(FRAMES_DIR / "frame_%04d.jpg")
]
subprocess.run(cmd, check=True)

frames = sorted(FRAMES_DIR.glob("*.jpg"))
print(f"Extracted {len(frames)} frames.")

# Create a contact sheet (4 columns)
cols = 4
rows = (len(frames) + cols - 1) // cols
w, h = 480, 270 # 16:9 thumbnail
sheet = Image.new("RGB", (cols * w, rows * h), (20, 20, 20))

for idx, fpath in enumerate(frames):
    img = Image.open(fpath).resize((w, h), Image.Resampling.LANCZOS)
    c = idx % cols
    r = idx // cols
    sheet.paste(img, (c * w, r * h))

out_sheet = ROOT / "preview_red" / "morph_animation_sheet.jpg"
sheet.save(out_sheet, quality=90)
print(f"Saved contact sheet: {out_sheet}")
