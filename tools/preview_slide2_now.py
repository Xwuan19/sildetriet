# -*- coding: utf-8 -*-
import sys
from pathlib import Path
from PIL import Image
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml import parse_xml
from pptx.oxml.ns import nsdecls, qn

W, H = 13.333, 7.500
L, R, T, B = 0.68, 12.66, 0.52, 6.96

ROOT = Path(".")
ASSETS = ROOT / "assets"
RAYS_IMG = ASSETS / "rays_gold.png"
GRAIN_IMG = ASSETS / "grain_red.png"
LENIN_MEDALLION = ASSETS / "lenin_medallion.png"

DISPLAY = "Playfair Editorial"
DISPLAY_IT = "Playfair Editorial"
SCRIPT = "ScriptViet-Bold"
SANS_SEMI = "Be Vietnam Pro SemiBold"
SANS = "Be Vietnam Pro"

GOLD = RGBColor(0xE8, 0xC8, 0x72)
GOLD_LIGHT = RGBColor(0xF3, 0xE2, 0xB8)
CREAM = RGBColor(0xFB, 0xF6, 0xEE)
MUTED = RGBColor(0xD6, 0xC4, 0xB8)
CARD_BG = RGBColor(0x28, 0x08, 0x0C)

GOLD_STOPS = [
    (0.00, "FFFFFF"),
    (0.20, "F5E7B2"),
    (0.55, "E8C872"),
    (0.85, "C39838"),
    (1.00, "8A6318"),
]

def apply_gradient_fill(shape, stops, angle=90):
    spPr = shape._element.spPr
    for old in spPr.findall(qn("a:solidFill")) + spPr.findall(qn("a:gradFill")):
        spPr.remove(old)
    gsLst = "".join(f'<a:gs pos="{int(p * 100000)}"><a:srgbClr val="{c}"/></a:gs>' for p, c in stops)
    xml = f'<a:gradFill xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"><a:gsLst>{gsLst}</a:gsLst><a:lin ang="{int(angle * 60000)}"/></a:gradFill>'
    spPr.append(parse_xml(xml))

def add_rect(slide, name, x, y, w, h, fill=None, line=None, line_w=0.5, opacity=100, line_opacity=100, shape=MSO_SHAPE.RECTANGLE):
    shp = slide.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    shp.name = name
    if fill is None:
        shp.fill.background()
    else:
        shp.fill.solid()
        shp.fill.fore_color.rgb = fill
        if opacity < 100:
            shp.fill._fill._xPr.find(qn("a:solidFill")).find(qn("a:srgbClr")).append(
                parse_xml(f'<a:alpha xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" val="{int(opacity * 1000)}"/>')
            )
    if line is None:
        shp.line.fill.background()
    else:
        shp.line.color.rgb = line
        shp.line.width = Pt(line_w)
        if line_opacity < 100:
            shp.line._xPr.find(qn("a:solidFill")).find(qn("a:srgbClr")).append(
                parse_xml(f'<a:alpha xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" val="{int(line_opacity * 1000)}"/>')
            )
    return shp

def add_gradient_rect(slide, name, x, y, w, h, stops, angle=90, radial=False):
    shp = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    shp.name = name
    shp.line.fill.background()
    spPr = shp._element.spPr
    for old in spPr.findall(qn("a:solidFill")) + spPr.findall(qn("a:gradFill")):
        spPr.remove(old)
    gsLst = ""
    for pos, col, alpha in stops:
        a_xml = f'<a:alpha val="{int(alpha * 1000)}"/>' if alpha is not None else ""
        gsLst += f'<a:gs pos="{int(pos * 100000)}"><a:srgbClr val="{col}">{a_xml}</a:srgbClr></a:gs>'
    if radial:
        xml = f'<a:gradFill xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"><a:gsLst>{gsLst}</a:gsLst><a:path path="circle"><a:fillToRect l="50000" t="50000" r="50000" b="50000"/></a:path></a:gradFill>'
    else:
        xml = f'<a:gradFill xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"><a:gsLst>{gsLst}</a:gsLst><a:lin ang="{int(angle * 60000)}"/></a:gradFill>'
    spPr.append(parse_xml(xml))
    return shp

def add_picture(slide, path, name, x, y, w, h, descr=""):
    pic = slide.shapes.add_picture(str(path), Inches(x), Inches(y), Inches(w), Inches(h))
    pic.name = name
    if descr:
        pic._element.nvPicPr.cNvPr.set("descr", descr)
    return pic

def add_text(slide, name, text, x, y, w, h, font=SANS, size=12, bold=False, italic=False, color=CREAM, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, spacing=None, gradient=None, shadow=False, caps=False, wrap=True, line_spacing=None):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tb.name = name
    tf = tb.text_frame
    tf.word_wrap = wrap
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    tf.vertical_anchor = anchor
    p = tf.paragraphs[0]
    p.alignment = align
    if line_spacing is not None:
        p.line_spacing = line_spacing
    r = p.add_run()
    r.text = text.upper() if caps else text
    r.font.name = font
    r.font.size = Pt(size)
    r.font.bold = bold
    r.font.italic = italic
    r.font.color.rgb = color
    if spacing is not None:
        r.font._element.set("spc", str(int(spacing * 100)))
    if gradient:
        # gradient text
        rPr = r._r.get_or_add_rPr()
        for old in rPr.findall(qn("a:solidFill")):
            rPr.remove(old)
        gsLst = "".join(f'<a:gs pos="{int(p * 100000)}"><a:srgbClr val="{c}"/></a:gs>' for p, c in gradient)
        xml = f'<a:gradFill xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"><a:gsLst>{gsLst}</a:gsLst><a:lin ang="5400000"/></a:gradFill>'
        rPr.append(parse_xml(xml))
    return tb

def populate_card(tb, header_num, header_text, items):
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(0.14)
    tf.margin_top = Inches(0.10)
    tf.margin_bottom = Inches(0.06)
    
    # Header paragraph
    p0 = tf.paragraphs[0]
    p0.space_after = Pt(4)
    r_num = p0.add_run()
    r_num.text = f"{header_num}. "
    r_num.font.name = DISPLAY
    r_num.font.bold = True
    r_num.font.size = Pt(11.0)
    r_num.font.color.rgb = GOLD
    
    r_head = p0.add_run()
    r_head.text = header_text.upper()
    r_head.font.name = SANS_SEMI
    r_head.font.size = Pt(8.8)
    r_head.font.color.rgb = GOLD
    r_head.font._element.set("spc", "120")
    
    is_compact = len(items) >= 4
    for name, role, desc in items:
        p = tf.add_paragraph()
        p.space_after = Pt(2.5 if is_compact else 4.0)
        
        # Name in Playfair Editorial bold
        r_n = p.add_run()
        r_n.text = f"{name}  "
        r_n.font.name = DISPLAY
        r_n.font.bold = True
        r_n.font.size = Pt(9.6 if is_compact else 10.2)
        r_n.font.color.rgb = CREAM
        
        # Role in Be Vietnam Pro SemiBold
        r_r = p.add_run()
        r_r.text = f"·  {role.upper()}\n"
        r_r.font.name = SANS_SEMI
        r_r.font.size = Pt(7.4 if is_compact else 8.0)
        r_r.font.color.rgb = GOLD_LIGHT
        r_r.font._element.set("spc", "90")
        
        # Duty in Playfair Editorial Italic
        r_d = p.add_run()
        r_d.text = f"“{desc}”"
        r_d.font.name = DISPLAY_IT
        r_d.font.italic = True
        r_d.font.size = Pt(7.5 if is_compact else 8.2)
        r_d.font.color.rgb = MUTED

# Build presentation
prs = Presentation()
prs.slide_width = Inches(W)
prs.slide_height = Inches(H)
s = prs.slides.add_slide(prs.slide_layouts[6])

# Background
add_gradient_rect(s, "!!BG_DEEP", 0, 0, W, H, [(0.00, "8E191D", None), (0.42, "650E13", None), (1.00, "2C0408", None)], angle=118)
add_picture(s, RAYS_IMG, "!!RAY_BURST", 0, 0, W, H)
add_picture(s, GRAIN_IMG, "!!TEXTURE_GRAIN", 0, 0, W, H)
add_rect(s, "!!FRAME_TOP", L, T, R - L, 0.007, fill=GOLD, opacity=26)
add_rect(s, "!!FRAME_BOTTOM", L, B, R - L, 0.007, fill=GOLD, opacity=26)
add_rect(s, "!!FRAME_LEFT", L, T, 0.007, B - T, fill=GOLD, opacity=26)
add_rect(s, "!!FRAME_RIGHT", R, T, 0.007, B - T, fill=GOLD, opacity=26)

# Masthead & footer
add_rect(s, "!!KICKER_MARK", L + 0.01, 0.735, 0.095, 0.095, fill=GOLD)
add_text(s, "!!KICKER_TEXT", "HỌC PHẦN TRIẾT HỌC MÁC – LÊNIN", L + 0.22, 0.70, 7.4, 0.24, font=SANS_SEMI, size=9.2, color=GOLD, spacing=2.5, caps=True)
add_rect(s, "!!KICKER_RULE", L + 0.01, 0.94, 5.25, 0.006, fill=GOLD, opacity=22)
add_text(s, "!!FOOTER_LEFT", "NHÓM 13 THÀNH VIÊN  ·  ĐẠI HỌC QUỐC GIA", L, 7.04, 5.2, 0.18, font=SANS, size=7.4, color=MUTED, spacing=1.2)
add_text(s, "!!FOOTER_RIGHT", "ĐỘI NGŨ THỰC HIỆN  ·  13 THÀNH VIÊN", 8.55, 7.04, 3.30, 0.18, font=SANS, size=7.4, color=MUTED, spacing=1.2, align=PP_ALIGN.RIGHT)
add_text(s, "!!PAGE_NO", "02 / 03", 12.00, 7.04, 0.66, 0.18, font=SANS_SEMI, size=7.4, color=GOLD, spacing=1.0, align=PP_ALIGN.RIGHT)

# Heading
add_text(s, "!!TEAM_KICKER", "ĐỘI NGŨ THỰC HIỆN  ·  NHÓM 04", 0.84, 1.15, 6.5, 0.20, font=SANS_SEMI, size=8.5, color=GOLD, spacing=1.6)
add_text(s, "!!TEAM_TITLE", "CHÚNG TÔI", 0.80, 1.36, 4.2, 0.55, font=DISPLAY, size=38, color=GOLD, gradient=GOLD_STOPS)
add_text(s, "!!TEAM_SUB", "mười ba thành viên, một tinh thần biện chứng", 4.15, 1.48, 4.6, 0.40, font=SCRIPT, size=21, color=GOLD_LIGHT)

# Separator between grid and right column
add_rect(s, "!!COLUMN_RULE", 8.85, 1.25, 0.008, 5.55, fill=GOLD, opacity=18)

# 4 Cards
c1_items = [
    ("Nhóm Trưởng", "Điều phối chung", "Điều phối tiến độ & Tổng hợp các cặp phạm trù"),
    ("Nguyễn Anh Thư", "Thư ký học thuật", "Quản lý hồ sơ nghiên cứu & Tổng hợp phần quy luật"),
    ("Quyên Lê", "Thiết kế & Kỹ thuật", "Kiến trúc mỹ thuật, typography & chuyển động morph"),
]
add_rect(s, "!!CARD_PANEL_1", 0.84, 1.98, 3.88, 2.38, fill=CARD_BG, line=GOLD, line_w=0.6, opacity=86, line_opacity=35)
tb1 = add_text(s, "!!CARD_CONTENT_1", "", 0.84, 1.98, 3.88, 2.38)
populate_card(tb1, "I", "Ban Điều Hành & Kỹ Thuật", c1_items)

c2_items = [
    ("Trần Nam Anh", "Thuyết trình 01", "Dẫn dắt bài nói, phân tích cơ sở lý luận & luận điểm"),
    ("Giaa Minhh", "Thuyết trình 02", "Trình bày trực quan, liên hệ thực tiễn sinh động"),
    ("Phạm Văn Huy", "Câu hỏi thảo luận", "Nghiên cứu câu hỏi tương tác & phản biện mở rộng"),
]
add_rect(s, "!!CARD_PANEL_2", 4.86, 1.98, 3.88, 2.38, fill=CARD_BG, line=GOLD, line_w=0.6, opacity=86, line_opacity=35)
tb2 = add_text(s, "!!CARD_CONTENT_2", "", 4.86, 1.98, 3.88, 2.38)
populate_card(tb2, "II", "Ban Thuyết Trình & Phản Biện", c2_items)

c3_items = [
    ("Hồng Nhung", "QL Lượng – Chất", "Tích luỹ lượng đổi dẫn đến biến đổi về chất"),
    ("Khánh Linh", "QL Mâu Thuẫn", "Nguồn gốc, động lực nội tại của sự phát triển"),
    ("Hồng Nhung", "QL Phủ Định của PĐ", "Khuynh hướng vận động xoáy ốc tiến lên"),
    ("Nguyễn Anh Thư", "Tổng hợp & Lọc ý", "Đúc kết luận điểm trọng tâm của ba quy luật"),
]
add_rect(s, "!!CARD_PANEL_3", 0.84, 4.46, 3.88, 2.44, fill=CARD_BG, line=GOLD, line_w=0.6, opacity=86, line_opacity=35)
tb3 = add_text(s, "!!CARD_CONTENT_3", "", 0.84, 4.46, 3.88, 2.44)
populate_card(tb3, "III", "Nghiên Cứu 3 Quy Luật Cơ Bản", c3_items)

c4_items = [
    ("Phạm Duy", "Nguyên nhân – Kết quả", "Phân tích mối liên hệ nhân quả khách quan"),
    ("Đào Dươngg", "Tất nhiên – Ngẫu nhiên", "Bản chất bên trong & hiện tượng bên ngoài"),
    ("Vũ Minh Nghĩa", "Nội dung – Hình thức", "Thống nhất biện chứng giữa nội dung & hình thức"),
    ("Duy", "Khả năng – Hiện thực", "Điều kiện khách quan chuyển hoá vào thực tiễn"),
    ("Nhóm Trưởng", "Tổng hợp luận cứ", "Kiểm duyệt hệ thống luận cứ & kết luận"),
]
add_rect(s, "!!CARD_PANEL_4", 4.86, 4.46, 3.88, 2.44, fill=CARD_BG, line=GOLD, line_w=0.6, opacity=86, line_opacity=35)
tb4 = add_text(s, "!!CARD_CONTENT_4", "", 4.86, 4.46, 3.88, 2.44)
populate_card(tb4, "IV", "Các Cặp Phạm Trù Biện Chứng", c4_items)

# Right Column: Glow, Star, Ring, Medallion, Quote
add_gradient_rect(s, "!!GLOW_PORTRAIT", 8.85, 0.25, 4.20, 4.20, [(0.0, "C23A32", 30), (0.55, "8E1A1E", 12), (1.0, "8E1A1E", 0)], radial=True)
star = add_rect(s, "!!STAR_BACK", 9.15, 0.95, 4.20, 4.20, fill=None, line=GOLD, line_w=0.8, line_opacity=18, shape=MSO_SHAPE.STAR_5_POINT)
star.rotation = 12
add_rect(s, "!!ORBIT_RING", 9.54, 1.30, 3.42, 3.42, fill=None, line=GOLD, line_w=0.9, line_opacity=45, shape=MSO_SHAPE.OVAL)
add_picture(s, LENIN_MEDALLION, "!!PORTRAIT_LENIN", 9.72, 1.48, 3.06, 3.06, "Huy hiệu chân dung V. I. Lenin")

add_text(s, "!!PORTRAIT_CAPTION", "V. I. LENIN  ·  1870 – 1924", 8.95, 4.76, 3.65, 0.22, font=SANS_SEMI, size=8.0, color=GOLD, spacing=1.8, align=PP_ALIGN.CENTER)
add_text(s, "!!PORTRAIT_QUOTE", "“Không có lý luận cách mạng thì không có phong trào cách mạng.”", 9.00, 5.08, 3.55, 0.85, font=DISPLAY_IT, size=11.5, italic=True, color=CREAM, align=PP_ALIGN.CENTER, line_spacing=1.12)
add_text(s, "!!PORTRAIT_SOURCE", "V. I. LÊNIN  ·  1902", 8.95, 6.00, 3.65, 0.20, font=SANS_SEMI, size=7.8, color=GOLD_LIGHT, spacing=1.6, align=PP_ALIGN.CENTER)

test_pptx = Path("preview_red/preview_slide2_new.pptx")
prs.save(test_pptx)
print("Saved preview_red/preview_slide2_new.pptx successfully!")
