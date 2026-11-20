import numpy as np
from PIL import Image, ImageFilter
from collections import deque

im = Image.open("preview_red/poster_cleaned_stage.png").convert("RGBA")
arr = np.array(im)
h, w, _ = arr.shape

bg_mask = np.zeros((h, w), dtype=bool)
q = deque()

def is_bg(y, x):
    p = arr[y, x]
    return p[1] < 22 and (p[0] > 70)

for x in range(w):
    if is_bg(0, x):
        bg_mask[0, x] = True
        q.append((0, x))
for y in range(h):
    if is_bg(y, w - 1):
        bg_mask[y, w - 1] = True
        q.append((y, w - 1))
    if is_bg(y, 0) and y < 150:
        bg_mask[y, 0] = True
        q.append((y, 0))

while q:
    cy, cx = q.popleft()
    for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        ny, nx = cy + dy, cx + dx
        if 0 <= ny < h and 0 <= nx < w:
            if not bg_mask[ny, nx] and is_bg(ny, nx):
                bg_mask[ny, nx] = True
                q.append((ny, nx))

alpha_im = Image.fromarray(np.where(bg_mask, 0, 255).astype(np.uint8))
alpha_smooth = alpha_im.filter(ImageFilter.GaussianBlur(radius=0.7))

arr[:, :, 3] = np.array(alpha_smooth)
cutout = Image.fromarray(arr)
cutout.save("assets/soviet_worker_flag_clean.png")
print("Saved assets/soviet_worker_flag_clean.png!")
