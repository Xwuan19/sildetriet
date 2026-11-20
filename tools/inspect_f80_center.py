from PIL import Image

f80 = Image.open("preview_red/frame80_slide_clean.png")
w, h = f80.size
print("Clean frame 80 size:", w, h)

# Let's inspect where everything is on f80:
# Left: Hammer & sickle (x: 230 to 420), Star (x: 440 to 600)
# Bottom Left: Worker & Flag (x: 60 to 750, y: 240 to 940)
# Top Right: "Nội Dung Trình Bày" (x: 990 to 1640, y: 100 to 220)
# Middle to Right: In Tuyệt Kỹ's frame 80, what is at x: 750 to 1400, y: 250 to 900?
# Let's crop that central region:
center_crop = f80.crop((750, 200, 1500, 900))
center_crop.save("preview_red/f80_center_content.png")
print("Saved f80_center_content.png")
