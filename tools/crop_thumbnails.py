from PIL import Image

im = Image.open("preview_red/intro_frames/f_015.png")
# Crop left thumbnail pane: x from 60 to 280, y from 200 to 950
thumbnails = im.crop((60, 200, 280, 950))
thumbnails.save("preview_red/left_thumbnails.png")
print("Saved left_thumbnails.png")
