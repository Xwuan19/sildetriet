import numpy as np
from PIL import Image

# Load clean frame 6.70
im = Image.open("preview_red/crop_clean_t_6.70.png")
w, h = im.size

# Let's crop Lenin area: x from 980 to 1680, y from 140 to 890
lenin_crop = im.crop((980, 140, 1680, 890))
lenin_crop.save("preview_red/raw_lenin_670.png")
print("Saved raw_lenin_670.png", lenin_crop.size)
