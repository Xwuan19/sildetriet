from PIL import Image
from pathlib import Path

frames_dir = Path("preview_red/trans_analysis_frames")
# Sample 15 frames evenly spaced
for i in range(1, 151, 10):
    f_path = frames_dir / f"frame_{i:04d}.png"
    im = Image.open(f_path).resize((320, 180))
    im.save(f"preview_red/trans_sample_{i:04d}.png")
print("Saved trans samples!")
