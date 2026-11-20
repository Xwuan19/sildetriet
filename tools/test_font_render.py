from PIL import Image, ImageDraw, ImageFont

font = ImageFont.truetype("fonts/PlayfairEditorial.ttf", 36)
im = Image.new("RGB", (600, 100), (40, 10, 15))
draw = ImageDraw.Draw(im)
draw.text((20, 20), "PHÂN CÔNG NHIỆM VỤ", font=font, fill=(232, 200, 114))
im.save("preview_red/test_font_render.png")
print("Saved test_font_render.png")
