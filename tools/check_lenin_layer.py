from PIL import Image

im = Image.open("preview_red/crop_lenin_watermark.png")
print("Lenin watermark size:", im.size)
# In frame 80, the right half of the slide has Lenin embedded in the background!
# Let's see: in Slide 2 of Tuyệt Kỹ's template:
# The background itself already has the Lenin watermark blended, OR Lenin is an image layer!
# Notice in image2.png of slideppt_media, image2.png WAS the background with Lenin already baked in!
# Let's check image2.png!
im2 = Image.open("preview_red/slideppt_media/image2.png")
print("image2 size:", im2.size)
