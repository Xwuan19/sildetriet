import numpy as np
from PIL import Image

im2 = Image.open("preview_red/slideppt_media/image2.png").convert("RGB")
w, h = im2.size
print(f"im2 size: {w}x{h}")

# The text and badges are located in x: 920 to 1600, y: 80 to 920
# Let's see: on the right side behind the text:
# At y: 80 to 220, x: 920 to 1500: "Nội Dung Trình Bày"
# The background behind "Nội Dung Trình Bày" is pure dark crimson red with subtle smooth gradient!
# At y: 220 to 920: the wax badges (x: 920 to 1020) and text (x: 1020 to 1550)
# Behind the text is Lenin's red chest/coat.
# Can we inpaint it cleanly, OR does our own stage background + Lenin cutout tinted red look even cleaner?
