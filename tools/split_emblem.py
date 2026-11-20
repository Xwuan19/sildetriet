from PIL import Image
import numpy as np

im = Image.open("assets/soviet_gold_emblem.png")
w, h = im.size
print(f"Emblem size: {w}x{h}")

# Let's inspect alpha channel
alpha = np.array(im)[:, :, 3]
print(f"Non-zero alpha pixels: {np.sum(alpha > 0)}")

# Let's separate the star alone and hammer-sickle alone:
# In the image (350x270):
# Hammer & sickle is on the left: x: 0 to 180
# Star is on the right: x: 180 to 350
crop_hs = im.crop((30, 20, 180, 180))
crop_hs.save("assets/emblem_hammer_sickle.png")

crop_star = im.crop((190, 10, 340, 180))
crop_star.save("assets/emblem_gold_star.png")

print("Saved assets/emblem_hammer_sickle.png and assets/emblem_gold_star.png")
