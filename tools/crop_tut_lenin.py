from PIL import Image

# In tut_frame_1.5.png (1920x1080), let's crop the right-hand Lenin on the slide canvas!
im = Image.open("preview_red/tut_frame_1.5.png")

# Let's crop the slide canvas area:
# In PowerPoint editor window, the slide canvas is roughly:
# x: 600 to 1800, y: 300 to 950
# Let's crop the Lenin on the right:
crop_right_lenin = im.crop((1200, 320, 1750, 930))
crop_right_lenin.save("preview_red/tut_lenin_crop.png")
print("Saved tut_lenin_crop.png")
