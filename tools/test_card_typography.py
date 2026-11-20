# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw, ImageFont
import os

fonts_dir = "fonts"
f_display_bold = ImageFont.truetype(os.path.join(fonts_dir, "PlayfairEditorial.ttf"), 22)
f_display_it = ImageFont.truetype(os.path.join(fonts_dir, "PlayfairEditorial-Italic.ttf"), 16)
f_sans_semi = ImageFont.truetype(os.path.join(fonts_dir, "BeVietnamPro-SemiBold.ttf"), 16)
f_sans_caps = ImageFont.truetype(os.path.join(fonts_dir, "BeVietnamPro-SemiBold.ttf"), 14)
f_script = ImageFont.truetype(os.path.join(fonts_dir, "ScriptViet-Bold.ttf"), 20)

im = Image.new("RGBA", (600, 350), (40, 10, 14, 255))
draw = ImageDraw.Draw(im)

# Card frame
draw.rectangle([10, 10, 590, 340], fill=(50, 12, 16, 220), outline=(232, 200, 114, 180), width=1)

# Card header
draw.text((25, 20), "II. BAN THUYẾT TRÌNH & PHẢN BIỆN", font=f_sans_caps, fill=(232, 200, 114))
draw.line([(25, 45), (575, 45)], fill=(232, 200, 114, 80), width=1)

# Member 1
y = 55
draw.text((25, y), "Trần Nam Anh", font=f_display_bold, fill=(251, 246, 238))
draw.text((180, y + 4), "·  THUYẾT TRÌNH 01", font=f_sans_caps, fill=(243, 226, 184))
draw.text((25, y + 28), "“Dẫn dắt bài nói, phân tích cơ sở lý luận & luận điểm”", font=f_display_it, fill=(214, 196, 184))

# Member 2
y += 65
draw.text((25, y), "Giaa Minhh", font=f_display_bold, fill=(251, 246, 238))
draw.text((160, y + 4), "·  THUYẾT TRÌNH 02", font=f_sans_caps, fill=(243, 226, 184))
draw.text((25, y + 28), "“Trình bày trực quan, liên hệ thực tiễn đời sống”", font=f_display_it, fill=(214, 196, 184))

# Member 3
y += 65
draw.text((25, y), "Phạm Văn Huy", font=f_display_bold, fill=(251, 246, 238))
draw.text((180, y + 4), "·  CÂU HỎI THẢO LUẬN", font=f_sans_caps, fill=(243, 226, 184))
draw.text((25, y + 28), "“Nghiên cứu câu hỏi tương tác & phản biện mở rộng”", font=f_display_it, fill=(214, 196, 184))

im.save("preview_red/card_test.png")
print("Saved preview_red/card_test.png")
