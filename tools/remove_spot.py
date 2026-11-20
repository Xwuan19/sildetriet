from PIL import Image
import numpy as np

im = Image.open("preview_red/master_stage_bg_1080p.png")
arr = np.array(im)

# Spot is near x: 20 to 60, y: 720 to 770
# Let's inspect where pixels have high brightness (R>150, G>150, B>150)
spot = (arr[700:800, 10:80, 0] > 150) & (arr[700:800, 10:80, 1] > 150) & (arr[700:800, 10:80, 2] > 150)
print(f"White spot pixel count: {np.sum(spot)}")

# Replace those pixels with nearby dark red background
clean_patch = arr[650:700, 10:80, :]
for y in range(700, 800):
    for x in range(10, 80):
        if arr[y, x, 0] > 150 and arr[y, x, 1] > 150 and arr[y, x, 2] > 150:
            arr[y, x, :] = arr[y - 60, x, :]

im_clean = Image.fromarray(arr)
im_clean.save("assets/master_stage_bg.png")
im_clean.save("preview_red/master_stage_bg_1080p_clean.png")
print("Saved clean master_stage_bg.png!")
