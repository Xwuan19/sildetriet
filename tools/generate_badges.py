from PIL import Image, ImageDraw, ImageFont

base = Image.open("assets/soviet_wax_seal_badge.png")
# Generate 01, 02, 03, 04 badges
# Let's see: we can create an empty wax seal by inpainting the center number, then writing 01, 02, 03, 04
# Or we can use the wax seal directly!
print("Wax badge size:", base.size)
