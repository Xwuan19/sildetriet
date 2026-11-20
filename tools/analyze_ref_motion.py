from pathlib import Path
from PIL import Image
import numpy as np

frames_dir = Path("preview_red/ref_frames_hd")
frames = sorted(list(frames_dir.glob("f_*.png")))

print(f"Total frames: {len(frames)}")

# Let's inspect frame differences to pinpoint the exact transition window:
diffs = []
for i in range(len(frames) - 1):
    im1 = np.array(Image.open(frames[i]).resize((160, 90)))
    im2 = np.array(Image.open(frames[i+1]).resize((160, 90)))
    d = np.mean(np.abs(im1.astype(float) - im2.astype(float)))
    diffs.append((i+1, d))

# Find the frames where difference is significant (motion is happening)
active_frames = [f for f, d in diffs if d > 0.5]
if active_frames:
    print(f"Motion starts at frame {active_frames[0]} (t = {5.0 + active_frames[0]/30:.2f}s)")
    print(f"Motion ends at frame {active_frames[-1]} (t = {5.0 + active_frames[-1]/30:.2f}s)")
    print(f"Total transition duration: {(active_frames[-1] - active_frames[0])/30:.2f} seconds")

# Print top 10 motion frames
sorted_diffs = sorted(diffs, key=lambda x: x[1], reverse=True)[:10]
print("Top motion frames:", sorted_diffs)
