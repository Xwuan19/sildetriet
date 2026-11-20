from PIL import Image

im = Image.open("preview_red/edit_mode_1080p/edit_1.5.png")
# Let's crop the center slide canvas in edit mode (high res)
# Canvas is x: 570 to 1730, y: 260 to 920
canvas = im.crop((570, 260, 1730, 920))
canvas.save("preview_red/edit_mode_canvas_hd.png")

# Left part of canvas (the card):
card = im.crop((570, 260, 1330, 920))
card.save("preview_red/edit_mode_card_hd.png")

# Right part of canvas (Lenin on the right):
lenin_right = im.crop((1200, 260, 1730, 920))
lenin_right.save("preview_red/edit_mode_lenin_right_hd.png")

print("Saved HD crops of edit mode canvas!")
