from PIL import Image
from pathlib import Path

frames_dir = Path("preview_red/trans_analysis_frames")
sheet = Image.new("RGB", (5 * 320, 6 * 180))
for i in range(1, 31):
    f_path = frames_dir / f"frame_{i:04d}.png"
    im = Image.open(f_path).resize((320, 180))
    r = (i - 1) // 5
    c = (i - 1) % 5
    sheet.paste(im, (c * 320, r * 180))

sheet.save("preview_red/trans_frames_1_30.png")
print("Saved trans_frames_1_30.png")
