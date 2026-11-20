from PIL import Image

im = Image.open("preview_red/lenin_tribune_original.jpg")
print("Russian Museum image size:", im.size)
preview = im.resize((480, int(im.height * 480 / im.width)))
preview.save("preview_red/lenin_tribune_preview.jpg")
