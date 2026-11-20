from PIL import Image

im = Image.open("preview_red/brodsky_lenin.jpg")
print("Size:", im.size)
preview = im.resize((480, int(im.height * 480 / im.width)))
preview.save("preview_red/brodsky_lenin_preview.jpg")
