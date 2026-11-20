from PIL import Image
import numpy as np

# Crop center canvas: roughly x from 550 to 1750, y from 250 to 900
for t in [1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55]:
    im = Image.open(f"preview_red/all_seconds/sec_{t:03d}.png")
    canvas = im.crop((550, 250, 1750, 900))
    canvas.save(f"preview_red/canvas_sec_{t:03d}.png")
print("Saved canvas samples!")
