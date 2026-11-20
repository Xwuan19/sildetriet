from PIL import Image

im2 = Image.open("preview_red/slideppt_media/image2.png")
# Let's resize to a preview and save
preview = im2.resize((960, 540))
preview.save("preview_red/image2_preview.png")
print("Saved preview_red/image2_preview.png")
