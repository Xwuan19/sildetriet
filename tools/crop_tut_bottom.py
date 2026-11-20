from PIL import Image

im = Image.open("preview_red/tut_frame_1.5.png")
# In tut_frame_1.5.png:
# PowerPoint slide canvas in the middle:
# Let's crop the bottom of the canvas and Lenin
crop_bot = im.crop((1250, 700, 1750, 960))
crop_bot.save("preview_red/tut_lenin_bottom.png")
print("Saved tut_lenin_bottom.png")
