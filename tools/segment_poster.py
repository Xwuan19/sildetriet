import numpy as np
from PIL import Image

# Let's inspect the edge of the flag in crop_poster_worker.png:
# The flag has a clear drop shadow or dark edge on the top and right!
im = Image.open("preview_red/poster_cleaned_stage.png")
arr = np.array(im)

# Let's see: on the left edge (x=0 to 15):
# Top edge (y=0 to 100):
# Notice in frame 80 of the video, how was this poster placed on the slide?
# In frame 80, the poster IS a cutout shape placed on top of the red curtain background!
# Notice the drop shadow around the top edge of the flag!
# Let's trace the boundary of the flag and worker so it is a transparent cutout PNG!

# Let's save a visual representation with contour:
from PIL import ImageDraw

# The flag outline:
# Top left: (0, 0) to (50, 0)
# Top curved edge: starts around (50, 0) up to (100, 15) then peaks around (500, 50) and curves down to (740, 220)
# Right curved edge: from (740, 220) curves down to (500, 480) then out to (560, 560)
# Let's write an automated segmenter or color-based floodfill/edge detector
print("Poster shape:", arr.shape)
