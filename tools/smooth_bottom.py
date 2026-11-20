from PIL import Image, ImageFilter
import numpy as np

im = Image.open("assets/master_stage_bg.png").convert("RGB")
arr = np.array(im)
h, w, _ = arr.shape

# The bottom area y from 860 to 945:
# In the coat area (x=980 to 1250), it had a slight vertical smear.
# Let's replace the bottom 70px of the coat with a smooth dark charcoal shadow:
# Coat color at y=855 is around [45, 45, 48].
for y in range(860, h):
    factor = (y - 860) / (h - 860)
    for x in range(980, 1250):
        c = arr[855, x, :]
        arr[y, x, :] = (c * (1.0 - factor * 0.7) + np.array([20, 18, 22]) * (factor * 0.7)).astype(np.uint8)

# Now apply a horizontal blur just on the strip y=860..945
strip = Image.fromarray(arr[860:h, :, :])
strip_blur = strip.filter(ImageFilter.BoxBlur(radius=3))
arr[860:h, :, :] = np.array(strip_blur)

im_final = Image.fromarray(arr)
im_final.save("assets/master_stage_bg.png")
im_final.save("preview_red/master_stage_bg_clean2.png")
print("Saved clean2!")
