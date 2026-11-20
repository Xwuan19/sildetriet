import numpy as np
from PIL import Image
from collections import deque

# Load test mask
mask_im = Image.open("preview_red/test_mask.png")
mask = np.array(mask_im) > 0  # True for foreground candidate
h, w = mask.shape

# Let's clean up:
# On the top right (x > 520, y < 420), everything outside the cap/neck is background!
# Let's define the cap/head right boundary:
# Let's inspect where the cap is on the right
# At y=50, cap ends around x=580
# At y=150, cap ends around x=620
# At y=250, ear/neck is around x=530
# At y=350, collar/coat is around x=560
# At y=450, coat is around x=660

# Let's do a connected component flood fill from (0, 0)
bg = np.zeros((h, w), dtype=bool)
# Start queue from borders that are definitely background
q = deque()
for x in range(w):
    if not mask[0, x]:
        bg[0, x] = True
        q.append((0, x))
for y in range(h):
    if not mask[y, 0]:
        bg[y, 0] = True
        q.append((y, 0))

# Also in top-right corner (0, w-1):
if not bg[0, w-1]:
    bg[0, w-1] = True
    q.append((0, w-1))

# Let's refine mask: background pixels can only connect if not mask
# To prevent leaks through tiny holes, let's dilate the mask slightly first, or flood fill
while q:
    y, x = q.popleft()
    for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        ny, nx = y + dy, x + dx
        if 0 <= ny < h and 0 <= nx < w:
            if not bg[ny, nx] and not mask[ny, nx]:
                bg[ny, nx] = True
                q.append((ny, nx))

fg = ~bg
fg_im = Image.fromarray((fg * 255).astype(np.uint8))
fg_im.save("preview_red/test_flood_fg.png")
print("Saved test_flood_fg.png")
