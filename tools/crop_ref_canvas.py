from PIL import Image

im = Image.open("preview_red/edit_mode_1080p/edit_1.5.png")
# The PowerPoint slide canvas in edit_1.5.png:
# Let's crop the slide canvas area
# Slide area is approximately from x=576 to 1728 (width 1152), y=268 to 916 (height 648)
# Let's crop and inspect the exact card
card_crop = im.crop((580, 270, 1720, 915))
card_crop.save("preview_red/ref_slide_canvas.png")

# Also crop just the card inside
inner_card = im.crop((600, 280, 1370, 905))
inner_card.save("preview_red/ref_inner_card.png")

print("Saved cropped reference canvas!")
