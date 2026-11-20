from PIL import Image

for name in ["emblem_hammer_sickle.png", "emblem_gold_star.png", "soviet_gold_emblem.png", "gold_star_clean.png"]:
    p = f"assets/{name}"
    im = Image.open(p)
    print(f"{name}: size={im.size}, mode={im.mode}")
