import numpy as np
from PIL import Image, ImageDraw, ImageFilter

im = Image.open("preview_red/banner_crop_raw.png").convert("RGBA")
w, h = im.size
print(f"Banner raw size: {w}x{h}")

# In banner_crop_raw, let's see the contour of the flag banner:
# The flag has a clear silhouette:
# Top edge: curves from left (x=0, y=0) over to top right corner (x=770, y=180)
# Right edge: curves downwards with a wave (x=770 at y=180 down to x=630 at y=480, then flair to x=730 at y=600)
# Bottom wave: curves down to worker's legs
# Bottom: worker's feet at bottom
# Let's inspect the boundary points!
