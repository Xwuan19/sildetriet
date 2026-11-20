import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE
from pathlib import Path
from lxml import etree
from pptx.oxml.ns import qn

prs = pptx.Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
s = prs.slides.add_slide(prs.slide_layouts[6])

W, H = 13.333, 7.500
CARD_BG = RGBColor(0x28, 0x08, 0x0C)
GOLD = RGBColor(0xE8, 0xC8, 0x72)
CREAM = RGBColor(0xFB, 0xF6, 0xEE)
MUTED = RGBColor(0xD6, 0xC4, 0xB8)
GOLD_LIGHT = RGBColor(0xF3, 0xE2, 0xB8)

DISPLAY = "Playfair Editorial"
DISPLAY_IT = "Playfair Editorial Italic"
SANS_SEMI = "Be Vietnam Pro SemiBold"

# Background
s.shapes.add_picture("assets/stage_bg_clean_dimmed.png", 0, 0, Inches(W), Inches(H))

# Left: Emblems
s.shapes.add_picture("assets/soviet_hammer_sickle_clean.png", Inches(1.20), Inches(0.55), Inches(1.15), Inches(1.00))
s.shapes.add_picture("assets/soviet_3d_star_clean.png", Inches(2.45), Inches(0.50), Inches(1.15), Inches(1.10))

# Left: Worker Flag
s.shapes.add_picture("assets/soviet_worker_flag_clean.png", Inches(0.15), Inches(2.35), Inches(4.55), Inches(5.15))

# Right: Lenin Crimson Watermark
s.shapes.add_picture("assets/lenin_crimson_watermark.png", Inches(8.50), Inches(0.50), Inches(4.70), Inches(6.90))

# Header on top-right
tb_h = s.shapes.add_textbox(Inches(4.80), Inches(0.60), Inches(7.90), Inches(0.95))
tf_h = tb_h.text_frame
tf_h.word_wrap = True
p_k = tf_h.paragraphs[0]
r_k = p_k.add_run()
r_k.text = "ĐỘI NGŨ THỰC HIỆN  ·  HỌC PHẦN TRIẾT HỌC MÁC – LÊNIN\n"
r_k.font.name = SANS_SEMI
r_k.font.size = Pt(8.5)
r_k.font.color.rgb = GOLD
r_k.font._element.set("spc", "180")

p_t = tf_h.add_paragraph()
r_t = p_t.add_run()
r_t.text = "PHÂN CÔNG NHIỆM VỤ"
r_t.font.name = DISPLAY
r_t.font.bold = True
r_t.font.size = Pt(26.0)
r_t.font.color.rgb = GOLD

# 4 Cards Layout:
# Col 1: x = 4.80, w = 3.90
# Col 2: x = 8.85, w = 3.90
# Row 1: y = 1.70, h = 2.50
# Row 2: y = 4.35, h = 2.65

def add_styled_card(s, x, y, w, h, badge_path, roman, title, members):
    # Card background box
    shape = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    shape.fill.solid()
    shape.fill.fore_color.rgb = CARD_BG
    shape.line.color.rgb = GOLD
    shape.line.width = Pt(0.6)
    
    # Set opacity
    spPr = shape._element.spPr
    solidFill = spPr.find(qn("a:solidFill"))
    if solidFill is not None:
        clr = solidFill.find(qn("a:srgbClr"))
        if clr is not None:
            a = etree.SubElement(clr, qn("a:alpha"))
            a.set("val", "82000")
            
    # Add badge icon
    s.shapes.add_picture(badge_path, Inches(x + 0.15), Inches(y + 0.14), Inches(0.38), Inches(0.35))
    
    # Text box
    tb = s.shapes.add_textbox(Inches(x + 0.58), Inches(y + 0.10), Inches(w - 0.70), Inches(h - 0.20))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    
    p0 = tf.paragraphs[0]
    p0.space_after = Pt(4)
    r_title = p0.add_run()
    r_title.text = f"{roman}.  {title.upper()}"
    r_title.font.name = SANS_SEMI
    r_title.font.bold = True
    r_title.font.size = Pt(8.8)
    r_title.font.color.rgb = GOLD
    r_title.font._element.set("spc", "110")
    
    is_compact = len(members) >= 4
    for name, role, desc in members:
        p = tf.add_paragraph()
        p.space_after = Pt(2.0 if is_compact else 3.5)
        
        r_n = p.add_run()
        r_n.text = f"{name} "
        r_n.font.name = DISPLAY
        r_n.font.bold = True
        r_n.font.size = Pt(9.2 if is_compact else 9.8)
        r_n.font.color.rgb = CREAM
        
        r_r = p.add_run()
        r_r.text = f"· {role}\n"
        r_r.font.name = SANS_SEMI
        r_r.font.size = Pt(7.2 if is_compact else 7.8)
        r_r.font.color.rgb = GOLD_LIGHT
        
        r_d = p.add_run()
        r_d.text = f"“{desc}”"
        r_d.font.name = DISPLAY_IT
        r_d.font.italic = True
        r_d.font.size = Pt(7.2 if is_compact else 7.8)
        r_d.font.color.rgb = MUTED

c1 = [
    ("Nhóm Trưởng", "Điều phối chung", "Điều phối tiến độ & Tổng hợp các cặp phạm trù"),
    ("Nguyễn Anh Thư", "Thư ký học thuật", "Quản lý hồ sơ nghiên cứu & Tổng hợp quy luật"),
    ("Quyên Lê", "Thiết kế & Kỹ thuật", "Kiến trúc mỹ thuật, typography & chuyển động morph"),
]
add_styled_card(s, 4.80, 1.70, 3.90, 2.50, "assets/soviet_seal_badge_1.png", "I", "Ban Điều Hành & Kỹ Thuật", c1)

c2 = [
    ("Trần Nam Anh", "Thuyết trình 01", "Dẫn dắt bài nói, phân tích cơ sở lý luận & luận điểm"),
    ("Giaa Minhh", "Thuyết trình 02", "Trình bày trực quan, liên hệ thực tiễn sinh động"),
    ("Phạm Văn Huy", "Thảo luận", "Nghiên cứu câu hỏi tương tác & phản biện"),
]
add_styled_card(s, 8.85, 1.70, 3.90, 2.50, "assets/soviet_seal_badge_2.png", "II", "Ban Thuyết Trình & Phản Biện", c2)

c3 = [
    ("Hồng Nhung", "QL Lượng – Chất", "Tích luỹ lượng đổi dẫn đến biến đổi về chất"),
    ("Khánh Linh", "QL Mâu Thuẫn", "Nguồn gốc, động lực nội tại của sự phát triển"),
    ("Hồng Nhung", "QL Phủ Định của PĐ", "Khuynh hướng vận động xoáy ốc tiến lên"),
    ("Nguyễn Anh Thư", "Tổng hợp luận điểm", "Đúc kết luận điểm trọng tâm của ba quy luật"),
]
add_styled_card(s, 4.80, 4.35, 3.90, 2.65, "assets/soviet_seal_badge_3.png", "III", "Nghiên Cứu 3 Quy Luật Cơ Bản", c3)

c4 = [
    ("Phạm Duy", "Nguyên nhân – KQ", "Phân tích mối liên hệ nhân quả khách quan"),
    ("Đào Dươngg", "Tất nhiên – NN", "Bản chất bên trong & hiện tượng bên ngoài"),
    ("Vũ Minh Nghĩa", "Nội dung – HT", "Thống nhất biện chứng giữa nội dung & hình thức"),
    ("Duy", "Khả năng – HT", "Điều kiện khách quan chuyển hoá vào thực tiễn"),
    ("Nhóm Trưởng", "Tổng hợp luận cứ", "Kiểm duyệt hệ thống luận cứ & kết luận"),
]
add_styled_card(s, 8.85, 4.35, 3.90, 2.65, "assets/soviet_seal_badge_4.png", "IV", "Các Cặp Phạm Trù Biện Chứng", c4)

prs.save("preview_red/test_slide2_new_style.pptx")
print("Saved test_slide2_new_style.pptx!")
