from pathlib import Path
from PIL import Image

im1 = Image.open("preview_red/slideppt_media/image1.png").resize((320, 180))
im1.save("preview_red/thumb_img1.png")
im2 = Image.open("preview_red/slideppt_media/image2.png").resize((320, 180))
im2.save("preview_red/thumb_img2.png")
print("Saved thumb_img1 and thumb_img2")
