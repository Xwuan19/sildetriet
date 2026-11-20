from PIL import Image

# Let's crop the right half of image2.png (x: 840 to 1680, y: 0 to 945)
im2 = Image.open("preview_red/slideppt_media/image2.png")
w, h = im2.size
lenin_half = im2.crop((840, 0, w, h))
lenin_half.save("preview_red/image2_right_half.png")
print("Saved image2_right_half.png")
