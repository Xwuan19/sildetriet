from PIL import Image

bg = Image.open("assets/master_stage_clean_bg.png").convert("RGBA")
# Resize bg to 1920x1080
bg = bg.resize((1920, 1080))

poster = Image.open("assets/soviet_worker_flag_clean.png").convert("RGBA")
hs = Image.open("assets/soviet_hammer_sickle_clean.png").convert("RGBA")
star = Image.open("assets/soviet_3d_star_clean.png").convert("RGBA")

# Let's scale poster to height ~720 (which is ~5 inches out of 7.5 inches)
p_w, p_h = poster.size
new_ph = 700
new_pw = int(p_w * (new_ph / p_h))
poster_scaled = poster.resize((new_pw, new_ph), Image.Resampling.LANCZOS)

# Scale emblems
hs_scaled = hs.resize((int(hs.width * 1.3), int(hs.height * 1.3)), Image.Resampling.LANCZOS)
star_scaled = star.resize((int(star.width * 1.3), int(star.height * 1.3)), Image.Resampling.LANCZOS)

# Paste on bg
# Hammer & sickle at x=130, y=80
bg.paste(hs_scaled, (130, 80), hs_scaled)
# Star at x=310, y=70
bg.paste(star_scaled, (310, 70), star_scaled)
# Worker flag at x=50, y=380
bg.paste(poster_scaled, (50, 380), poster_scaled)

bg.save("preview_red/composite_test_slide2_left.png")
print("Saved composite_test_slide2_left.png!")
