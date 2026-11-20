from pathlib import Path
from PIL import Image
import numpy as np

sec_dir = Path("preview_red/all_seconds")
secs = sorted(list(sec_dir.glob("sec_*.png")))

print("Detecting slide transitions...")
for i in range(len(secs) - 1):
    im1 = np.array(Image.open(secs[i]).resize((80, 45)))
    im2 = np.array(Image.open(secs[i+1]).resize((80, 45)))
    diff = np.mean(np.abs(im1.astype(float) - im2.astype(float)))
    if diff > 10.0:
        print(f"Transition between sec_{i+1:03d}.png and sec_{i+2:03d}.png (diff = {diff:.2f})")
