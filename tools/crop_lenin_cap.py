from PIL import Image

im1 = Image.open("preview_red/slideppt_media/image1.png")
# Lenin in image1.png is located at x: 950 to 1680, y: 150 to 945
lenin_crop = im1.crop((950, 150, 1680, 945))
lenin_crop.save("preview_red/lenin_cap_crop.png")
print("Saved lenin_cap_crop.png:", lenin_crop.size)
