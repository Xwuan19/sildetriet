import numpy as np
from PIL import Image

im = Image.open("assets/soviet_worker_flag_clean.png").convert("RGBA")
arr = np.array(im)
h, w, _ = arr.shape

# Clean the white patch on the left (x: 0 to 180, y: 550 to h):
# That white patch is from outside background
for y in range(450, h):
    for x in range(0, 180):
        # if it's the bright white outside the worker's pole
        if x < 150 and y > 530:
            arr[y, x, 3] = 0

# Clean the bottom-right subscribe box remnant (y > 560, x > 400):
for y in range(560, h):
    for x in range(400, w):
        if arr[y, x, 0] > 180 and arr[y, x, 1] > 180 and arr[y, x, 2] > 180:
            arr[y, x, 3] = 0
        if y > 600 and x > 380:
            arr[y, x, 3] = 0

# Also clean the tiny top-left notch
for y in range(0, 50):
    for x in range(0, 60):
        if arr[y, x, 0] > 200 and arr[y, x, 1] > 200:
            arr[y, x, 3] = 0

clean = Image.fromarray(arr)
# Crop to non-zero alpha bounding box
bbox = clean.getbbox()
if bbox:
    clean = clean.crop(bbox)

clean.save("assets/soviet_worker_flag_clean.png")
print("Cleaned poster bbox:", clean.size)
