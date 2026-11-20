from PIL import Image
import numpy as np

im = Image.open("preview_red/lenin_full_clean_raw.png").convert("RGB")
arr = np.array(im, dtype=float)
h, w, _ = arr.shape

r = arr[:, :, 0]
g = arr[:, :, 1]
b = arr[:, :, 2]

# Measure "redness" vs neutral/skin tone:
# Red background: r is much higher than g and b
# Specifically: (r - g) > 70 and (r - b) > 70
# But wait! On Lenin's red tie or ruddy cheek:
# On cheek: r ~ 180, g ~ 90, b ~ 70. Here (r - g) is ~90!
# So color alone might affect cheek or tie if threshold is too loose.
# BUT combining polygon bounds with color segmentation will give 100% exact boundary!

print("Testing pixel samples:")
# Background samples (red flag):
print("Red flag at (150, 100):", arr[100, 150])
print("Red flag at (100, 300):", arr[300, 100])
print("Red flag at (650, 250):", arr[250, 650])
print("Red flag at (620, 100):", arr[100, 620])

# Lenin samples:
print("Lenin hat at (400, 50):", arr[50, 400])
print("Lenin forehead at (300, 200):", arr[200, 300])
print("Lenin cheek at (400, 250):", arr[250, 400])
print("Lenin ear at (500, 230):", arr[230, 500])
print("Lenin coat at (400, 600):", arr[600, 400])
