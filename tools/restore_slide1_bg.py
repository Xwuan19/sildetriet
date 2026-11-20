from PIL import Image, ImageDraw
import numpy as np

im = Image.open("preview_red/ref_slide1_clean.png")
w, h = im.size

# In slide 1, let's see what the background looks like without the text:
# Wait! Let's check if we can reconstruct the clean background of Slide 1!
# Remember in crop_clean_t_6.70.png:
# In crop_clean_t_6.70.png, the title text on the left was ALREADY GONE!
# Let's inspect crop_clean_t_6.70.png!
im_clean = Image.open("preview_red/crop_clean_t_6.70.png")
im_clean.save("preview_red/test_bg_clean_670.png")

# In this clean frame, let's look at y=0 to 880:
# The left is rich deep red background, the right is the painted Lenin on red flag!
# Let's inspect the bottom 65px (y=880 to 945):
# We can smoothly extend the gradient from y=870 down to y=945!

arr = np.array(im_clean)
# For each column x, interpolate from y=875 to 945:
# At y=875, get pixel color
col_sample = arr[875:880, :, :].mean(axis=0).astype(np.uint8)
for y in range(880, h):
    fade = (y - 880) / (h - 880)
    # Blend towards deep wine red (0x22, 0x04, 0x08)
    target = np.array([34, 4, 8], dtype=float)
    arr[y, :, :] = (col_sample * (1.0 - fade * 0.6) + target * (fade * 0.6)).astype(np.uint8)

im_restored = Image.fromarray(arr)
im_restored.save("preview_red/slide1_bg_restored.png")
print("Saved slide1_bg_restored.png")
