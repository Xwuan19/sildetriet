# -*- coding: utf-8 -*-
import sys
from pathlib import Path
from PIL import Image
import numpy as np

frames_dir = Path("video_analysis/frames")
frames = sorted(frames_dir.glob("frame_*.jpg"))

# Compute difference between consecutive frames to detect transitions
diffs = []
prev = None

for i, f in enumerate(frames):
    im = Image.open(f).convert("L").resize((320, 180))
    arr = np.array(im, dtype=float)
    if prev is not None:
        diff = np.mean(np.abs(arr - prev))
        diffs.append((i, diff, f.name))
    prev = arr

# Find peaks in diffs (scene changes / active morph transitions)
print("Top 20 frame differences (transitions):")
diffs_sorted = sorted(diffs, key=lambda x: x[1], reverse=True)
for idx, diff, name in diffs_sorted[:20]:
    t = idx * 0.5
    print(f"Frame {idx} ({name}) at ~{t:.1f}s: diff={diff:.2f}")
