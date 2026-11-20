import numpy as np
from PIL import Image

im = Image.open("assets/soviet_worker_flag_clean.png").convert("RGBA")
arr = np.array(im)
h, w, _ = arr.shape

# The very bottom edge: let's make the bottom 40 pixels smoothly fade to alpha or straight cut
# Worker legs are at the bottom
# Let's clean the small jagged edge at the bottom-right and bottom-left:
for y in range(h - 40, h):
    # fade bottom alpha slightly
    fade = (h - 1 - y) / 40.0
    arr[y, :, 3] = (arr[y, :, 3].astype(float) * fade).astype(np.uint8)

clean = Image.fromarray(arr)
clean.save("assets/soviet_worker_flag_clean.png")
print("Perfected bottom fade on worker flag!")
