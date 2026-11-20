from PIL import Image

im = Image.open("preview_red/canvas_sec_001.png")
# Let's inspect the two Lenins and the card in high resolution
# The card area:
card = im.crop((50, 50, 800, 750))
card.save("preview_red/detail_card.png")

# The right area:
right_lenin = im.crop((700, 50, 1150, 750))
right_lenin.save("preview_red/detail_right_lenin.png")
print("Saved details!")
