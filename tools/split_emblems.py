from PIL import Image

pair = Image.open("assets/soviet_gold_emblem_pair_clean.png")
w, h = pair.size

# Find bbox of non-zero alpha
# Left half for hammer & sickle
hs = pair.crop((80, 0, 240, h))
bbox_hs = hs.getbbox()
if bbox_hs:
    hs = hs.crop(bbox_hs)
hs.save("assets/soviet_hammer_sickle_clean.png")

# Right half for star
st = pair.crop((245, 0, w, h))
bbox_st = st.getbbox()
if bbox_st:
    st = st.crop(bbox_st)
st.save("assets/soviet_3d_star_clean.png")

print(f"Saved hammer_sickle ({hs.size}) and star ({st.size})")
