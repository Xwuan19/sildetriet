from PIL import Image

sheet = Image.new("RGB", (5 * 320, 3 * 180))
idx = 0
for i in range(1, 151, 10):
    im = Image.open(f"preview_red/trans_sample_{i:04d}.png")
    r = idx // 5
    c = idx % 5
    sheet.paste(im, (c * 320, r * 180))
    idx += 1

sheet.save("preview_red/trans_contact_sheet.png")
print("Saved trans_contact_sheet.png")
