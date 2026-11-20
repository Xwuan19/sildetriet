import numpy as np
from PIL import Image

# 1. Extract and clean the Gold Hammer & Sickle + 3D Star
im_emblem = Image.open("preview_red/crop_emblem_pair.png").convert("RGBA")
arr = np.array(im_emblem)

# The background is crimson red: R is high (130-190), G is very low (<20), B is very low (<20)
# The gold is yellow/gold: R is high (>180), G is high (>150), B is low to medium (<100)
# Let's inspect RGB distribution
r = arr[:, :, 0]
g = arr[:, :, 1]
b = arr[:, :, 2]

# Gold pixels have high green compared to red background:
# In crimson red background: g is mostly 0 to 15!
# In gold emblem: g is 100 to 255!
# For edge pixels (anti-aliasing between gold and red):
# We can compute alpha based on green channel and saturation
mask = g > 25
# Smooth alpha:
alpha = np.clip((g.astype(float) - 15) / 50.0, 0, 1) * 255
# For pixels where red is dominant and green is very low, alpha = 0
alpha[g < 15] = 0
# For strong gold:
alpha[g > 65] = 255

arr[:, :, 3] = alpha.astype(np.uint8)
clean_emblem = Image.fromarray(arr)
clean_emblem.save("assets/soviet_gold_emblem_pair_clean.png")
print("Saved assets/soviet_gold_emblem_pair_clean.png")
