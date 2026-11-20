from PIL import Image
import numpy as np

im1 = Image.open("preview_red/ref_slide1_clean.png")
im2 = Image.open("preview_red/ref_slide2_clean.png")

# Let's crop the background on the right (x=1000 to 1680, y=70 to 400)
bg1 = im1.crop((1000, 70, 1680, 400))
bg2 = im2.crop((1000, 70, 1680, 400))

# Compare them
arr1 = np.array(bg1, dtype=float)
arr2 = np.array(bg2, dtype=float)

diff = np.abs(arr1 - arr2)
print("Mean absolute difference on top-right between Slide 1 and Slide 2:", np.mean(diff))
