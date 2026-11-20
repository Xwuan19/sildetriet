from PIL import Image
from collections import deque
import numpy as np

im = Image.open("preview_red/lenin_full_clean_raw.png").convert("RGBA")
arr = np.array(im)
h, w, _ = arr.shape

r = arr[:, :, 0].astype(int)
g = arr[:, :, 1].astype(int)
b = arr[:, :, 2].astype(int)

# In the red background:
# r is high, g and b are low.
# Let's inspect the redness condition:
# (r - g) > 60 and (r - b) > 60 and r > 70
# Let's check if any part of Lenin has this:
# Lenin's red tie: tie is at x: 380 to 450, y: 530 to 650.
# Tie is inside the coat! It is NOT connected to the outer border!
# What about Lenin's cheek?
# Cheek is at x: 350 to 450, y: 220 to 280. Surrounded by beard, nose, brow.
# What about the Cyrillic letters banner? The banner is part of the background we want to remove!
# So if we flood fill from the borders:
# Border seeds:
# All pixels along y=0 (top edge)
# All pixels along x=0 from y=0 to y=650 (left edge)
# All pixels along x=w-1 from y=0 to y=600 (right edge)

is_bg_color = (r > 70) & (r - g > 55) & (r - b > 50)
print(f"Total bg color candidates: {np.sum(is_bg_color)}")

# Breadth-first search flood fill from borders:
visited = np.zeros((h, w), dtype=bool)
q = deque()

# Add top edge
for x in range(w):
    if is_bg_color[0, x]:
        visited[0, x] = True
        q.append((0, x))

# Add left edge (y < 650)
for y in range(650):
    if is_bg_color[y, 0] and not visited[y, 0]:
        visited[y, 0] = True
        q.append((y, 0))

# Add right edge (y < 600)
for y in range(600):
    if is_bg_color[y, w-1] and not visited[y, w-1]:
        visited[y, w-1] = True
        q.append((y, w-1))

while q:
    cy, cx = q.popleft()
    for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        ny, nx = cy + dy, cx + dx
        if 0 <= ny < h and 0 <= nx < w:
            if not visited[ny, nx]:
                # If it's red background color:
                if is_bg_color[ny, nx]:
                    visited[ny, nx] = True
                    q.append((ny, nx))

print(f"Flood filled bg pixels: {np.sum(visited)}")

# Create alpha mask: 0 where visited (background), 255 where Lenin!
alpha = np.ones((h, w), dtype=np.uint8) * 255
alpha[visited] = 0

cutout_arr = arr.copy()
cutout_arr[:, :, 3] = alpha

cutout_im = Image.fromarray(cutout_arr)
cutout_im.save("preview_red/lenin_flood_test.png")
print("Saved preview_red/lenin_flood_test.png!")
