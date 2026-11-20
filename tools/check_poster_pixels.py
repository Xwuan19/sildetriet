import numpy as np
from PIL import Image

# Let's inspect pixel values along lines to precisely find the edge of the flag:
im = Image.open("preview_red/poster_cleaned_stage.png").convert("RGB")
arr = np.array(im)
h, w, _ = arr.shape

# Let's sample the background outside the flag:
# At (700, 50): background red (R~145, G~10, B~15)
# Inside the flag at (650, 150): R~180, G~45, B~25
# Notice inside the flag, G is > 30 and R is brighter!
# Outside the flag (on the red curtain): G is < 18!
print("Outside background G at (700, 50):", arr[50, 700])
print("Inside flag G at (650, 150):", arr[150, 650])
print("Worker white at (300, 500):", arr[500, 300])
print("Outside left at (10, 100):", arr[100, 10])
