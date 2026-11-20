# -*- coding: utf-8 -*-
"""
Dựng lại build_deck.py với hệ thống Morph kinetic chuẩn theo Tuyệt Kỹ PowerPoint:
- Đầy đủ 13 thành viên với vai trò chính xác.
- Mỗi layer đều có bản sao morph (off-canvas) trên các slide lân cận.
- Cú pháp !!NAME để PowerPoint khớp cặp 100%.
"""
from __future__ import annotations

import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

from PIL import Image
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, MSO_AUTO_SIZE, PP_ALIGN
from pptx.oxml.ns import nsdecls, qn
from pptx.oxml import parse_xml
from pptx.util import Inches, Pt
from lxml import etree

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
FONTS = ROOT / "fonts"
OUT = ROOT / "Triet_hoc_Mac_Lenin_Loi_chao.pptx"

LENIN_HERO_IMG = ASSETS / "lenin_warm.png"
RAYS_IMG = ASSETS / "rays_gold.png"
GRAIN_IMG = ASSETS / "grain_red.png"

# Palette
INK = RGBColor(0x1B, 0x03, 0x05)
CREAM = RGBColor(0xF7, 0xEC, 0xD3)
GOLD_LIGHT = RGBColor(0xF4, 0xDF, 0xA3)
GOLD = RGBColor(0xD6, 0xAF, 0x64)
GOLD_DEEP = RGBColor(0xA5, 0x76, 0x2B)
MUTED = RGBColor(0xC9, 0xAD, 0x7C)
CARD_BG = RGBColor(0x28, 0x05, 0x08)

DISPLAY = "Playfair Editorial"
DISPLAY_IT = "Playfair Editorial Italic"
SCRIPT = "Script Viet"
SANS = "Be Vietnam Pro"
SANS_SEMI = "Be Vietnam Pro SemiBold"
SANS_BOLD = "Be Vietnam Pro Bold"

W, H = 13.333, 7.5
L, R, T, B = 0.68, 12.66, 0.52, 6.96

GOLD_STOPS = [
    (0.00, "FFF7DC"),
    (0.16, "F3D98F"),
    (0.38, "DDB65F"),
    (0.56, "B9852F"),
    (0.74, "E7C471"),
    (0.88, "C79A44"),
    (1.00, "8E611C"),
]

def set_fill_alpha(shape, opacity_pct: float) -> None:
    solid = shape.fill._xPr.find(qn("a:solidFill"))
    if solid is None:
        return
    srgb = solid.find(qn("a:srgbClr"))
    if srgb is None:
        return
    for old in srgb.findall(qn("a:alpha")):
        srgb.remove(old)
    alpha = etree.SubElement(srgb, qn("a:alpha"))
    alpha.set("val", str(int(opacity_pct * 1000)))

def set_line_alpha(shape, opacity_pct: float) -> None:
    ln = shape.line._get_or_add_ln()
    solid = ln.find(qn("a:solidFill"))
    if solid is None:
        return
    srgb = solid.find(qn("a:srgbClr"))
    if srgb is None:
        return
    for old in srgb.findall(qn("a:alpha")):
        srgb.remove(old)
    alpha = etree.SubElement(srgb, qn("a:alpha"))
    alpha.set("val", str(int(opacity_pct * 1000)))

def gradient_shape(shape, stops, angle=90, radial=False) -> None:
    shape.fill.gradient()
    grad = shape.fill._xPr.find(qn("a:gradFill"))
    gs_lst = grad.find(qn("a:gsLst"))
    for gs in list(gs_lst):
        gs_lst.remove(gs)
    for pos, color, alpha in stops:
        gs = etree.SubElement(gs_lst, qn("a:gs"))
        gs.set("pos", str(int(pos * 100000)))
        clr = etree.SubElement(gs, qn("a:srgbClr"))
        clr.set("val", color)
        if alpha is not None:
            a = etree.SubElement(clr, qn("a:alpha"))
            a.set("val", str(int(alpha * 1000)))
    lin = grad.find(qn("a:lin"))
    if radial:
        if lin is not None:
            grad.remove(lin)
        path = etree.SubElement(grad, qn("a:path"))
        path.set("path", "circle")
        rect = etree.SubElement(path, qn("a:fillToRect"))
        for k in ("l", "t", "r", "b"):
            rect.set(k, "50000")
    else:
        if lin is None:
            lin = etree.SubElement(grad, qn("a:lin"))
        lin.set("ang", str(int(angle * 60000)))
        lin.set("scaled", "0")

def add_rect(slide, name, x, y, w, h, fill=None, line=None, line_w=0.75,
             opacity=None, line_opacity=None, shape=MSO_SHAPE.RECTANGLE):
    shp = slide.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    shp.name = name
    shp.shadow.inherit = False
    if fill is None:
        shp.fill.background()
    else:
        shp.fill.solid()
        shp.fill.fore_color.rgb = fill
        if opacity is not None:
            set_fill_alpha(shp, opacity)
    if line is None:
        shp.line.fill.background()
    else:
        shp.line.color.rgb = line
        shp.line.width = Pt(line_w)
        if line_opacity is not None:
            set_line_alpha(shp, line_opacity)
    return shp

def add_gradient_rect(slide, name, x, y, w, h, stops, angle=115, radial=False, line=None, line_w=0.6):
    shp = add_rect(slide, name, x, y, w, h, fill=INK, line=line, line_w=line_w)
    gradient_shape(shp, stops, angle=angle, radial=radial)
    return shp

def apply_text_gradient(run, stops) -> None:
    rpr = run.font._element
    solid = rpr.find(qn("a:solidFill"))
    gs_xml = []
    for pos, color in stops:
        gs_xml.append(f'<a:gs pos="{int(pos * 100000)}"><a:srgbClr val="{color}"/></a:gs>')
    grad = parse_xml(
        f'<a:gradFill {nsdecls("a")} rotWithShape="1">'
        f'<a:gsLst>{"".join(gs_xml)}</a:gsLst>'
        f'<a:lin ang="5400000" scaled="0"/></a:gradFill>'
    )
    if solid is not None:
        solid.addprevious(grad)
        rpr.remove(solid)
    else:
        latin = rpr.find(qn("a:latin"))
        if latin is not None:
            latin.addprevious(grad)
        else:
            rpr.append(grad)

def apply_text_shadow(run) -> None:
    rpr = run.font._element
    latin = rpr.find(qn("a:latin"))
    effect = parse_xml(
        f'<a:effectLst {nsdecls("a")}>'
        f'<a:outerShdw blurRad="38100" dist="25400" dir="5400000" algn="t" rotWithShape="0">'
        f'<a:srgbClr val="1B0305"><a:alpha val="42000"/></a:srgbClr>'
        f'</a:outerShdw></a:effectLst>'
    )
    if latin is not None:
        latin.addprevious(effect)
    else:
        rpr.append(effect)

def add_text(slide, name, text, x, y, w, h, font=SANS, size=12, bold=False,
             italic=False, color=CREAM, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP,
             spacing=None, line_spacing=None, caps=False, wrap=True,
             gradient=None, shadow=False):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tb.name = name
    tf = tb.text_frame
    tf.word_wrap = wrap
    tf.auto_size = MSO_AUTO_SIZE.NONE
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
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
        apply_text_gradient(r, gradient)
    if shadow:
        apply_text_shadow(r)
    return tb

def add_picture(slide, path, name, x, y, w, h, descr=""):
    pic = slide.shapes.add_picture(str(path), Inches(x), Inches(y), Inches(w), Inches(h))
    pic.name = name
    if descr:
        pic._element.nvPicPr.cNvPr.set("descr", descr)
    return pic

def add_lenin(slide, path, name, x, bottom, height, descr=""):
    with Image.open(path) as im:
        ar = im.width / im.height
    width = height * ar
    return add_picture(slide, path, name, x, bottom - height, width, height, descr)

MORPH_XML = """<mc:AlternateContent xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006">
  <mc:Choice xmlns:p159="http://schemas.microsoft.com/office/powerpoint/2015/09/main" Requires="p159">
    <p:transition xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" xmlns:p14="http://schemas.microsoft.com/office/powerpoint/2010/main" spd="slow" p14:dur="2000">
      <p159:morph option="byObject"/>
    </p:transition>
  </mc:Choice>
  <mc:Fallback>
    <p:transition xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" spd="slow">
      <p:fade/>
    </p:transition>
  </mc:Fallback>
</mc:AlternateContent>"""

def add_morph(slide, duration=2000) -> None:
    sld = slide._element
    ns_mc = "{http://schemas.openxmlformats.org/markup-compatibility/2006}AlternateContent"
    for old in sld.findall(ns_mc):
        sld.remove(old)
    xml = MORPH_XML.replace('p14:dur="2000"', f'p14:dur="{duration}"')
    el = etree.fromstring(xml.encode("utf-8"))
    clr = sld.find(qn("p:clrMapOvr"))
    if clr is not None:
        clr.addnext(el)
    else:
        sld.append(el)

def set_vertical(tb) -> None:
    body_pr = tb.text_frame._txBody.find(qn("a:bodyPr"))
    body_pr.set("vert", "vert270")

# ---------------------------------------------------------------- Shared Stage & Anchors
def add_shared_background(slide):
    add_gradient_rect(
        slide, "!!BG_DEEP", 0, 0, W, H,
        [(0.00, "8E191D", None), (0.42, "650E13", None), (1.00, "2C0408", None)],
        angle=118,
    )
    add_picture(slide, RAYS_IMG, "!!RAY_BURST", 0, 0, W, H, "Tia sáng vàng tạo chiều sâu")
    add_picture(slide, GRAIN_IMG, "!!TEXTURE_GRAIN", 0, 0, W, H, "Lớp hạt nhẹ cổ điển")
    add_rect(slide, "!!FRAME_TOP", L, T, R - L, 0.007, fill=GOLD, opacity=26)
    add_rect(slide, "!!FRAME_BOTTOM", L, B, R - L, 0.007, fill=GOLD, opacity=26)
    add_rect(slide, "!!FRAME_LEFT", L, T, 0.007, B - T, fill=GOLD, opacity=26)
    add_rect(slide, "!!FRAME_RIGHT", R, T, 0.007, B - T, fill=GOLD, opacity=26)

def add_masthead(slide):
    add_rect(slide, "!!KICKER_MARK", L + 0.01, 0.735, 0.095, 0.095, fill=GOLD)
    add_text(slide, "!!KICKER_TEXT", "HỌC PHẦN TRIẾT HỌC MÁC – LÊNIN",
             L + 0.22, 0.70, 7.4, 0.24, font=SANS_SEMI, size=9.2, color=GOLD,
             spacing=2.5, caps=True)
    add_rect(slide, "!!KICKER_RULE", L + 0.01, 0.94, 5.25, 0.006, fill=GOLD, opacity=22)

def add_footer(slide, page, right_text):
    add_text(slide, "!!FOOTER_LEFT", "NHÓM 13 THÀNH VIÊN  ·  ĐẠI HỌC QUỐC GIA",
             L, 7.04, 5.2, 0.18, font=SANS, size=7.4, color=MUTED, spacing=1.2)
    add_text(slide, "!!FOOTER_RIGHT", right_text, 8.55, 7.04, 3.30, 0.18,
             font=SANS, size=7.4, color=MUTED, spacing=1.2, align=PP_ALIGN.RIGHT)
    add_text(slide, "!!PAGE_NO", page, 12.00, 7.04, 0.66, 0.18,
             font=SANS_SEMI, size=7.4, color=GOLD, spacing=1.0, align=PP_ALIGN.RIGHT)
    add_text(slide, "!!CREDIT_IMAGE",
             "Chân dung: V. I. Lenin, 1920 · Wikimedia Commons · Public Domain",
             L, 7.23, 7.2, 0.16, font=SANS, size=6.2, color=MUTED, opacity=55)

def add_side_tag(slide, text):
    tb = add_text(slide, "!!SIDE_TEXT", text, 0.33, 1.45, 0.22, 4.45,
                  font=SANS_SEMI, size=6.8, color=GOLD, spacing=1.8,
                  caps=True, wrap=False, anchor=MSO_ANCHOR.MIDDLE)
    set_vertical(tb)

# Helper to populate structured rich text into member cards
def fill_card_1_content(tb):
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = Inches(0.12)
    p0 = tf.paragraphs[0]
    p0.text = "I. BAN ĐIỀU HÀNH & KỸ THUẬT"
    p0.font.name = SANS_BOLD
    p0.font.size = Pt(10)
    p0.font.color.rgb = GOLD
    p0.space_after = Pt(4)
    
    items_coord = [
        ("Nhóm Trưởng", "@tao", "Điều phối chung & Tổng hợp phần phạm trù"),
        ("Thư Ký", "@Nguyễn Anh Thư", "Quản lý tiến độ & Tổng hợp phần quy luật"),
        ("Thiết Kế Slide", "@Quyen Le", "Kỹ thuật đồ hoạ & Hiệu ứng trình bày"),
    ]
    for role, name, desc in items_coord:
        p = tf.add_paragraph()
        p.space_after = Pt(3)
        r1 = p.add_run()
        r1.text = f"• {role}: "
        r1.font.name = SANS_SEMI
        r1.font.size = Pt(8.6)
        r1.font.color.rgb = GOLD_LIGHT
        r2 = p.add_run()
        r2.text = f"{name}\n"
        r2.font.name = SANS_BOLD
        r2.font.size = Pt(9.0)
        r2.font.color.rgb = CREAM
        r3 = p.add_run()
        r3.text = f"  ↳ {desc}"
        r3.font.name = SANS
        r3.font.size = Pt(7.6)
        r3.font.color.rgb = MUTED

    p_div = tf.add_paragraph()
    p_div.text = "II. BAN THUYẾT TRÌNH & PHẢN BIỆN"
    p_div.font.name = SANS_BOLD
    p_div.font.size = Pt(10)
    p_div.font.color.rgb = GOLD
    p_div.space_before = Pt(6)
    p_div.space_after = Pt(4)

    items_pres = [
        ("Thuyết Trình 01", "@Trần Nam Anh", "Dẫn dắt bài nói, phân tích luận điểm"),
        ("Thuyết Trình 02", "@Giaa Minhh", "Trình bày trực quan, điều phối câu hỏi"),
        ("Câu Hỏi Liên Quan", "@Phạm Văn Huy", "Nghiên cứu câu hỏi mở rộng & liên hệ"),
    ]
    for role, name, desc in items_pres:
        p = tf.add_paragraph()
        p.space_after = Pt(3)
        r1 = p.add_run()
        r1.text = f"• {role}: "
        r1.font.name = SANS_SEMI
        r1.font.size = Pt(8.6)
        r1.font.color.rgb = GOLD_LIGHT
        r2 = p.add_run()
        r2.text = f"{name}\n"
        r2.font.name = SANS_BOLD
        r2.font.size = Pt(9.0)
        r2.font.color.rgb = CREAM
        r3 = p.add_run()
        r3.text = f"  ↳ {desc}"
        r3.font.name = SANS
        r3.font.size = Pt(7.6)
        r3.font.color.rgb = MUTED

def fill_card_2_content(tb):
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = Inches(0.12)
    p0 = tf.paragraphs[0]
    p0.text = "III. TÌM THÔNG TIN: 3 QUY LUẬT"
    p0.font.name = SANS_BOLD
    p0.font.size = Pt(10)
    p0.font.color.rgb = GOLD
    p0.space_after = Pt(4)

    items_laws = [
        ("Quy luật Lượng – Chất", "@Hồng Nhung"),
        ("Quy luật Mâu Thuẫn", "@Khánh Linh"),
        ("QL Phủ Định của Phủ Định", "@Hồng Nhung"),
        ("Tổng hợp & Lọc ý", "@Nguyễn Anh Thư"),
    ]
    for role, name in items_laws:
        p = tf.add_paragraph()
        p.space_after = Pt(2)
        r1 = p.add_run()
        r1.text = f"• {role}: "
        r1.font.name = SANS_SEMI
        r1.font.size = Pt(8.4)
        r1.font.color.rgb = GOLD_LIGHT
        r2 = p.add_run()
        r2.text = f"{name}"
        r2.font.name = SANS_BOLD
        r2.font.size = Pt(8.8)
        r2.font.color.rgb = CREAM

    p_div = tf.add_paragraph()
    p_div.text = "IV. TÌM THÔNG TIN: CÁC CẶP PHẠM TRÙ"
    p_div.font.name = SANS_BOLD
    p_div.font.size = Pt(10)
    p_div.font.color.rgb = GOLD
    p_div.space_before = Pt(6)
    p_div.space_after = Pt(4)

    items_cats = [
        ("Nguyên nhân – Kết quả", "@Phạm Duy"),
        ("Tất nhiên – Ngẫu nhiên", "@Đào Dươngg"),
        ("Nội dung – Hình thức", "@Vũ Minh Nghĩa"),
        ("Khả năng – Hiện thực", "@Duy"),
        ("Tổng hợp & Lọc ý", "@tao"),
    ]
    for role, name in items_cats:
        p = tf.add_paragraph()
        p.space_after = Pt(2)
        r1 = p.add_run()
        r1.text = f"• {role}: "
        r1.font.name = SANS_SEMI
        r1.font.size = Pt(8.4)
        r1.font.color.rgb = GOLD_LIGHT
        r2 = p.add_run()
        r2.text = f"{name}"
        r2.font.name = SANS_BOLD
        r2.font.size = Pt(8.8)
        r2.font.color.rgb = CREAM

print("Content fillers defined.")
