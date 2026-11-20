import numpy as np
from PIL import Image

poster = Image.open("preview_red/crop_poster_worker.png").convert("RGBA")
w, h = poster.size
arr = np.array(poster)

# Let's inspect the boundary of the poster:
# The poster has a flag shape. The background around the flag is the stage red cloth.
# Inside the flag: the color has texture (dots/fabric grain) and lighter orange-red tone.
# The worker has white shirt (RGB ~240, 240, 245), blue shadows (RGB ~40, 50, 70).
# The bottom right has a tiny white subscribe box at y > h - 40, x > w - 180.
# Let's remove the tiny subscribe button corner by filling it with the worker's trouser color or making it transparent.

# Let's clean the tiny subscribe box at the bottom right
# Bottom right corner:
for y in range(h - 50, h):
    for x in range(w - 180, w):
        if arr[y, x, 0] > 200 and arr[y, x, 1] > 200 and arr[y, x, 2] > 200: # white button
            arr[y, x] = [139, 12, 16, 255] # match red background

clean_poster = Image.fromarray(arr)
clean_poster.save("preview_red/poster_cleaned_stage.png")
print("Saved poster_cleaned_stage.png")
