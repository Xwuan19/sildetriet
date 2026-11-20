from PIL import Image
from collections import deque
import numpy as np

im = Image.open("preview_red/lenin_full_clean_raw.png").convert("RGBA")
arr = np.array(im)
h, w, _ = arr.shape

r = arr[:, :, 0].astype(int)
g = arr[:, :, 1].astype(int)
b = arr[:, :, 2].astype(int)

# Exact profile curve on the left of face/beard:
# y from 160 to 365
profile_x = {
    160: 236, 170: 242, 180: 244, 190: 245, 200: 244,
    210: 246, 220: 245, 230: 240, 235: 238, 240: 240,
    250: 244, 260: 245, 270: 248, 280: 250, 290: 252,
    300: 254, 310: 252, 320: 248, 330: 246, 340: 246,
    350: 254, 360: 265, 370: 285
}

def get_face_boundary(y):
    # interpolate profile_x
    if y < 160:
        return 0
    if y > 370:
        return 0
    keys = sorted(profile_x.keys())
    for i in range(len(keys)-1):
        if keys[i] <= y <= keys[i+1]:
            t = (y - keys[i]) / (keys[i+1] - keys[i])
            return int(profile_x[keys[i]] * (1 - t) + profile_x[keys[i+1]] * t)
    return 245

# Background definition:
# Red flag: r > 70 and (r - g > 55) and (r - b > 50)
is_bg_color = (r > 65) & (r - g > 50) & (r - b > 45)

# BFS flood fill from outer borders
visited = np.zeros((h, w), dtype=bool)
q = deque()

# Add top edge
for x in range(w):
    visited[0, x] = True
    q.append((0, x))

# Add left edge
for y in range(h):
    visited[y, 0] = True
    q.append((y, 0))

# Add right edge (y < 650)
for y in range(650):
    visited[y, w-1] = True
    q.append((y, w-1))

while q:
    cy, cx = q.popleft()
    for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        ny, nx = cy + dy, cx + dx
        if 0 <= ny < h and 0 <= nx < w:
            if not visited[ny, nx]:
                # If inside face zone, block it!
                if 160 <= ny <= 370:
                    fb = get_face_boundary(ny)
                    if nx >= fb:
                        continue # do not enter face
                # Also behind head: between ear and hat rim (y: 170..270, x: 490..620)
                # Behind ear at y=200..260, the red flag starts at x > 530
                # Hat is dark: r < 70 or g > 30
                # So if it's bg color:
                if is_bg_color[ny, nx]:
                    visited[ny, nx] = True
                    q.append((ny, nx))

# Let's inspect the mask!
alpha = np.ones((h, w), dtype=np.uint8) * 255
alpha[visited] = 0

# Also clean any loose specks in top-left
# Anything with x < 200 and y < 400 where alpha is still 255 (the Cyrillic text banner):
# The Cyrillic text banner is in the red flag: x < 230 and y < 450
for y in range(450):
    for x in range(230):
        if y < 160 or x < get_face_boundary(y):
            alpha[y, x] = 0

# Smooth alpha edge
from PIL import ImageFilter
alpha_im = Image.fromarray(alpha).filter(ImageFilter.GaussianBlur(radius=0.7))

cutout_arr = arr.copy()
cutout_arr[:, :, 3] = np.array(alpha_im)

cutout_im = Image.fromarray(cutout_arr)
cutout_im.save("preview_red/lenin_flood_clean.png")
cutout_im.save("assets/lenin_painted_cutout.png")
print("Saved preview_red/lenin_flood_clean.png!")
