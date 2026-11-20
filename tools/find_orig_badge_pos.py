# -*- coding: utf-8 -*-
from PIL import Image
import numpy as np

im = Image.open("archive/debug/tweak/Slide3.PNG").convert("RGB")
arr = np.array(im)
# Find bright pixels in the right half (x > 960)
# '01' text is very bright gold/cream
h, w, _ = arr.shape
right_half = arr[:, w//2:]
# Look for brightness
gray = np.mean(right_half, axis=2)
y_indices, x_indices = np.where(gray > 120)
if len(x_indices) > 0:
    cx = (w // 2 + np.mean(x_indices)) / w * 13.333
    cy = np.mean(y_indices) / h * 7.50
    print(f"Center of bright feature on right half: x={cx:.2f}\", y={cy:.2f}\"")
