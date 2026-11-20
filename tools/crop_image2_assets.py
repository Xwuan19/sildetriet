from PIL import Image

im2 = Image.open("preview_red/slideppt_media/image2.png")
print("image2 size:", im2.size)

# Crop poster on bottom-left:
# Look at image2:
# Worker & Marx-Engels-Lenin flag is roughly from x: 0 to 600, y: 350 to 945
poster_crop = im2.crop((0, 350, 600, 945))
poster_crop.save("preview_red/test_poster_crop.png")

# Crop Hammer & Sickle + Gold Star on top-left:
# Roughly x: 100 to 450, y: 50 to 300
emblem_crop = im2.crop((80, 40, 480, 320))
emblem_crop.save("preview_red/test_emblem_crop.png")

# Crop Lenin watermark on right:
# Roughly x: 950 to 1680, y: 100 to 945
lenin_crop = im2.crop((950, 100, 1680, 945))
lenin_crop.save("preview_red/test_lenin_watermark.png")

print("Saved test crops from image2.png")
