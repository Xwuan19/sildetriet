from PIL import Image, ImageDraw, ImageFont

# Inpaint the center of the wax seal badge to get a clean base template
badge = Image.open("assets/soviet_wax_seal_badge.png").convert("RGBA")
w, h = badge.size

# Clone color from inside edge to fill center (x: 24 to 50, y: 18 to 48)
arr = list(badge.getdata())
clean_badge = badge.copy()
draw = ImageDraw.Draw(clean_badge)

# Fill circle in center with the wax seal color #c48b68
wax_color = (196, 139, 104, 255)
wax_inner = (180, 120, 85, 255)
draw.ellipse([22, 16, 52, 48], fill=wax_color, outline=wax_inner, width=1)

# Now generate badges 01, 02, 03, 04
for idx, num_str in enumerate(["01", "02", "03", "04"], start=1):
    b_im = clean_badge.copy()
    b_draw = ImageDraw.Draw(b_im)
    # Draw number in dark bronze/red #5a1c18
    # Since we have small size, draw clean text
    b_draw.text((27, 23), num_str, fill=(90, 28, 24, 255))
    b_im.save(f"assets/soviet_seal_badge_{idx}.png")
    print(f"Saved soviet_seal_badge_{idx}.png")
