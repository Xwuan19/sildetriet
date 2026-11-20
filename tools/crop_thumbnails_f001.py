from PIL import Image

im = Image.open("preview_red/intro_frames/f_001.png")
# Crop left thumbnail pane from frame 1
thumbnails = im.crop((60, 200, 280, 850))
thumbnails.save("preview_red/thumbnails_f001.png")
print("Saved thumbnails_f001.png")
