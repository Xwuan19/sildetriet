from PIL import Image

f80 = Image.open("preview_red/frame80_slide_clean.png")
w, h = f80.size
print(f"Clean Slide 2 size: {w}x{h}")

# 1. Gold Hammer & Sickle (top-left)
# In f80: x roughly 250 to 450, y roughly 60 to 200
hammer_sickle = f80.crop((230, 60, 420, 210))
hammer_sickle.save("preview_red/crop_hammer_sickle.png")

# 2. 3D Gold Star (top-left)
# x roughly 440 to 600, y roughly 60 to 210
star_3d = f80.crop((440, 60, 600, 215))
star_3d.save("preview_red/crop_star_3d.png")

# Both together:
emblem_pair = f80.crop((220, 50, 610, 220))
emblem_pair.save("preview_red/crop_emblem_pair.png")

# 3. Poster worker & flag:
# x roughly 60 to 800, y roughly 240 to 940
poster = f80.crop((60, 240, 800, 880))
poster.save("preview_red/crop_poster_worker.png")

# 4. Right side Lenin Watermark:
# x roughly 950 to 1780, y roughly 150 to 940
lenin_wm = f80.crop((950, 150, 1780, 880))
lenin_wm.save("preview_red/crop_lenin_watermark.png")

print("Saved individual crop tests!")
