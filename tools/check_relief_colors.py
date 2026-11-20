import numpy as np
from PIL import Image

im = Image.open("preview_red/banner_crop_raw.png")
arr = np.array(im)
h, w, _ = arr.shape

# The sculpted banner consists of:
# 1. The red flag background of the banner (texture/fabric)
# 2. The white/cream sculpted heads of Karl Marx, Friedrich Engels, and Vladimir Lenin!
# 3. The white uniform of the revolutionary worker holding the flag staff!
# Look at where the worker is:
# Worker in white: x: 0 to 450, y: 350 to 700!
# Sculpted heads: x: 300 to 750, y: 80 to 450!
print("Marx relief head color (cream/white):", arr[200, 420])
print("Engels relief head color (cream/white):", arr[220, 560])
print("Lenin relief head color (cream/white):", arr[250, 700])
