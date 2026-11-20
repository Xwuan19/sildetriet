# -*- coding: utf-8 -*-
"""Bộ slide toàn diện: TRIẾT HỌC MÁC – LÊNIN (NHÓM 04)
Nội dung: 3 Quy luật cơ bản của phép biện chứng & 5 Cặp phạm trù biện chứng
Tài liệu nguồn: NHÓM 4(1).docx
Thiết kế theo ngôn ngữ Áp phích Cổ động Xô Viết & Tân cổ điển (Soviet Constructivist & Editorial Neo-Classical).
Tỷ lệ chuẩn 16:9 (13.333" x 7.500"), nhúng font và Morphing XML.
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
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import nsdecls, qn
from pptx.oxml import parse_xml
from pptx.util import Inches, Pt
from lxml import etree

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "assets"
FONTS = ROOT / "fonts"
OUT = ROOT / "Triet_hoc_Mac_Lenin_Nhom_4.pptx"

LENIN = ASSETS / "lenin_warm.png"
MEDALLION = ASSETS / "lenin_badge.png"
RAYS = ASSETS / "rays_gold.png"
GRAIN = ASSETS / "grain_red.png"

# Palette chuẩn mỹ thuật chính luận sang trọng
INK = RGBColor(0x1B, 0x03, 0x05)
CREAM = RGBColor(0xF7, 0xEC, 0xD3)
GOLD_LIGHT = RGBColor(0xF4, 0xDF, 0xA3)
GOLD = RGBColor(0xD6, 0xAF, 0x64)
GOLD_DEEP = RGBColor(0xA5, 0x76, 0x2B)
RED = RGBColor(0x9E, 0x1B, 0x1F)
RED_DEEP = RGBColor(0x4A, 0x07, 0x0C)
MUTED = RGBColor(0xC9, 0xAD, 0x7C)
CARD_BG = RGBColor(0x28, 0x05, 0x08)

DISPLAY = "Playfair Editorial"
DISPLAY_IT = "Playfair Editorial Italic"
SCRIPT = "Script Viet"
SANS = "Be Vietnam Pro"
SANS_SEMI = "Be Vietnam Pro SemiBold"

W, H = 13.333, 7.5
L, R, T, B = 0.68, 12.66, 0.52, 6.96
TOTAL_SLIDES = 18

GOLD_STOPS = [
    (0.00, "FFF9E6"),
    (0.20, "F7E4AC"),
    (0.48, "D6AF64"),
    (0.78, "A5762B"),
    (1.00, "704812"),
]


# ---------------------------------------------------------------- CORE HELPERS
def set_fill_alpha(shape, alpha_pct: float) -> None:
    val = int(alpha_pct * 1000)
    solid = shape.fill._xPr.find(qn("a:solidFill"))
    if solid is not None:
        clr = solid.find(qn("a:srgbClr"))
        if clr is not None:
            for old in clr.findall(qn("a:alpha")):
                clr.remove(old)
            clr.append(parse_xml(f'<a:alpha {nsdecls("a")} val="{val}"/>'))


def set_line_alpha(shape, alpha_pct: float) -> None:
    val = int(alpha_pct * 1000)
    ln = shape.line._get_or_add_ln()
    solid = ln.find(qn("a:solidFill"))
    if solid is not None:
        clr = solid.find(qn("a:srgbClr"))
        if clr is not None:
            for old in clr.findall(qn("a:alpha")):
                clr.remove(old)
            clr.append(parse_xml(f'<a:alpha {nsdecls("a")} val="{val}"/>'))


def add_rect(slide, name, x, y, w, h, fill=None, line=None, line_w=0.5,
             opacity=None, line_opacity=None, shape=MSO_SHAPE.RECTANGLE):
    shp = slide.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    shp.name = name
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
        f'<a:lin ang="5400000" scaled="0"/>'
        f'</a:gradFill>'
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
    effect = parse_xml(
        f'<a:effectLst {nsdecls("a")}>'
        f'<a:outerShdw blurRad="38100" dist="25400" dir="5400000" algn="t" rotWithShape="0">'
        f'<a:srgbClr val="1B0305"><a:alpha val="42000"/></a:srgbClr>'
        f'</a:outerShdw>'
        f'</a:effectLst>'
    )
    latin = rpr.find(qn("a:latin"))
    if latin is not None:
        latin.addprevious(effect)
    else:
        rpr.append(effect)


def set_text_run_alpha(run, alpha_pct: float) -> None:
    rpr = run.font._element
    val = int(alpha_pct * 1000)
    solid = rpr.find(qn("a:solidFill"))
    if solid is not None:
        clr = solid.find(qn("a:srgbClr"))
        if clr is not None:
            clr.append(parse_xml(f'<a:alpha {nsdecls("a")} val="{val}"/>'))


def add_text(slide, name, text, x, y, w, h, font=SANS, size=12, bold=False,
             italic=False, color=CREAM, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP,
             spacing=None, gradient=None, shadow=False, caps=False, wrap=True,
             opacity=None, line_spacing=None):
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
        apply_text_gradient(r, gradient)
    if shadow:
        apply_text_shadow(r)
    if opacity is not None:
        set_text_run_alpha(r, opacity)
    return tb


def set_vertical(tb) -> None:
    body_pr = tb.text_frame._txBody.find(qn("a:bodyPr"))
    body_pr.set("vert", "vert270")


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


def add_background(slide):
    add_gradient_rect(
        slide, "BG_DEEP", 0, 0, W, H,
        [(0.00, "8E191D", None), (0.42, "650E13", None), (1.00, "2C0408", None)],
        angle=118,
    )
    add_picture(slide, RAYS, "RAY_BURST", 0, 0, W, H, "Tia sáng vàng chiều sâu")
    add_picture(slide, GRAIN, "TEXTURE_GRAIN", 0, 0, W, H, "Lớp hạt nhẹ cổ điển")
    add_rect(slide, "FRAME_TOP", L, T, R - L, 0.007, fill=GOLD, opacity=26)
    add_rect(slide, "FRAME_BOTTOM", L, B, R - L, 0.007, fill=GOLD, opacity=26)
    add_rect(slide, "FRAME_LEFT", L, T, 0.007, B - T, fill=GOLD, opacity=26)
    add_rect(slide, "FRAME_RIGHT", R, T, 0.007, B - T, fill=GOLD, opacity=26)


def add_masthead(slide, kicker="HỌC PHẦN TRIẾT HỌC MÁC – LÊNIN"):
    add_rect(slide, "KICKER_MARK", L + 0.01, 0.735, 0.095, 0.095, fill=GOLD)
    add_text(slide, "KICKER_TEXT", kicker,
             L + 0.22, 0.70, 7.4, 0.24, font=SANS_SEMI, size=9.2, color=GOLD,
             spacing=2.5, caps=True)
    add_rect(slide, "KICKER_RULE", L + 0.01, 0.94, 5.25, 0.006, fill=GOLD, opacity=22)


def add_footer(slide, current_page, right_text):
    add_text(slide, "FOOTER_LEFT", "NHÓM 04  ·  HỌC PHẦN TRIẾT HỌC MÁC – LÊNIN",
             L, 7.04, 5.2, 0.18, font=SANS, size=7.4, color=MUTED, spacing=1.2)
    add_text(slide, "FOOTER_RIGHT", right_text, 8.55, 7.04, 3.30, 0.18,
             font=SANS, size=7.4, color=MUTED, spacing=1.2, align=PP_ALIGN.RIGHT)
    page_str = f"{current_page:02d} / {TOTAL_SLIDES:02d}"
    add_text(slide, "PAGE_NO", page_str, 12.00, 7.04, 0.66, 0.18,
             font=SANS_SEMI, size=7.4, color=GOLD, spacing=1.0, align=PP_ALIGN.RIGHT)


def add_side_badge(slide, text):
    tb = add_text(slide, "SIDE_TEXT", text, 0.33, 1.45, 0.22, 4.45,
                  font=SANS_SEMI, size=6.8, color=GOLD, spacing=1.8,
                  caps=True, wrap=False, anchor=MSO_ANCHOR.MIDDLE)
    set_vertical(tb)


def add_slide_header(slide, subtitle, title):
    add_text(slide, "SEC_SUBTITLE", subtitle, L + 0.02, 1.15, 10.5, 0.22,
             font=SANS_SEMI, size=8.8, color=GOLD, spacing=2.2, caps=True)
    t_len = len(title)
    if t_len > 48:
        sz = 26
    elif t_len > 40:
        sz = 28
    elif t_len > 32:
        sz = 30
    else:
        sz = 32
    add_text(slide, "SEC_TITLE", title, L - 0.02, 1.36, 11.95, 0.65,
             font=DISPLAY, size=sz, color=CREAM, shadow=True, wrap=False)


def add_card(slide, name, x, y, w, h, title, items, badge_num=None, highlight_title=False):
    add_rect(slide, f"{name}_BG", x, y, w, h, fill=CARD_BG, line=GOLD, line_w=0.6,
             opacity=88, line_opacity=35, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    tb = add_text(slide, f"{name}_TXT", "", x + 0.22, y + 0.18, w - 0.44, h - 0.34)
    tf = tb.text_frame
    tf.word_wrap = True
    
    p0 = tf.paragraphs[0]
    p0.space_after = Pt(4)
    if badge_num:
        r_num = p0.add_run()
        r_num.text = f"{badge_num}  "
        r_num.font.name = DISPLAY
        r_num.font.bold = True
        r_num.font.size = Pt(13)
        r_num.font.color.rgb = GOLD
    
    r_t = p0.add_run()
    r_t.text = title.upper()
    r_t.font.name = SANS_SEMI
    r_t.font.bold = True
    r_t.font.size = Pt(9.6 if len(title) > 30 else 10.4)
    r_t.font.color.rgb = GOLD_LIGHT if highlight_title else GOLD
    r_t.font._element.set("spc", "100")
    
    for label, desc in items:
        p = tf.add_paragraph()
        p.space_after = Pt(3.5)
        if label:
            r_l = p.add_run()
            r_l.text = f"• {label}: "
            r_l.font.name = SANS_SEMI
            r_l.font.size = Pt(8.6)
            r_l.font.color.rgb = GOLD_LIGHT
        r_d = p.add_run()
        r_d.text = desc
        r_d.font.name = SANS
        r_d.font.size = Pt(8.4)
        r_d.font.color.rgb = CREAM


MORPH = """<mc:AlternateContent xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006">
  <mc:Choice xmlns:p159="http://schemas.microsoft.com/office/powerpoint/2015/09/main" Requires="p159">
    <p:transition xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" xmlns:p14="http://schemas.microsoft.com/office/powerpoint/2010/main" spd="slow" p14:dur="1500">
      <p159:morph option="byObject"/>
    </p:transition>
  </mc:Choice>
  <mc:Fallback>
    <p:transition xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" spd="slow">
      <p:fade/>
    </p:transition>
  </mc:Fallback>
</mc:AlternateContent>"""


def add_morph(slide, duration=1500) -> None:
    sld = slide._element
    ns_mc = "{http://schemas.openxmlformats.org/markup-compatibility/2006}AlternateContent"
    for old in sld.findall(ns_mc):
        sld.remove(old)
    xml = MORPH.replace('p14:dur="1500"', f'p14:dur="{duration}"')
    el = etree.fromstring(xml.encode("utf-8"))
    clr = sld.find(qn("p:clrMapOvr"))
    if clr is not None:
        clr.addnext(el)
    else:
        sld.append(el)


# ================================================================ SLIDE DEFINITIONS

# SLIDE 1: BÌA CHÍNH LUẬN
def build_slide_01(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    add_background(s)

    add_gradient_rect(s, "GLOW_PORTRAIT", 7.55, -0.15, 6.1, 6.1,
                      [(0.0, "C23A32", 34), (0.55, "8E1A1E", 14), (1.0, "8E1A1E", 0)], radial=True)
    star = add_rect(s, "STAR_BACK", 7.55, -0.72, 6.75, 6.75, fill=None, line=GOLD, line_w=0.8, line_opacity=17, shape=MSO_SHAPE.STAR_5_POINT)
    star.rotation = 12
    add_rect(s, "ORBIT_RING", 7.95, 0.58, 5.25, 5.25, fill=None, line=GOLD, line_w=0.9, line_opacity=38, shape=MSO_SHAPE.OVAL)
    add_lenin(s, LENIN, "LENIN_HERO", 8.28, 7.62, 7.28, "V. I. Lenin")

    add_masthead(s)
    add_footer(s, 1, "LỜI CHÀO  ·  NHÓM 04")
    add_side_badge(s, "LỜI CHÀO · 2026")

    add_text(s, "SALUTATION", "Kính chào thầy cô và các bạn", 0.84, 1.24, 6.7, 0.62, font=SCRIPT, size=32, color=GOLD_LIGHT)
    add_text(s, "TITLE_1", "TRIẾT HỌC", 0.80, 1.88, 7.4, 1.25, font=DISPLAY, size=77, color=CREAM, spacing=-1.0, shadow=True)
    add_text(s, "TITLE_2", "MÁC – LÊNIN", 0.80, 3.12, 7.4, 1.35, font=DISPLAY, size=77, color=GOLD, spacing=-1.0, gradient=GOLD_STOPS, shadow=True)

    add_rect(s, "TITLE_RULE", 0.84, 4.46, 2.35, 0.018, fill=GOLD, opacity=85)
    add_text(s, "SUBTITLE_LABEL", "BÁO CÁO THẢO LUẬN  ·  NHÓM 04", 0.84, 4.64, 5.8, 0.22, font=SANS_SEMI, size=8.6, color=GOLD, spacing=2.4, caps=True)
    add_text(s, "MANIFESTO", "3 Quy Luật Cơ Bản & 5 Cặp Phạm Trù Của Phép Biện Chứng Duy Vật", 0.82, 4.98, 6.75, 0.56, font=DISPLAY_IT, size=17.5, color=CREAM, line_spacing=1.06)
    add_text(s, "CHAPTER_LABEL", "CHƯƠNG 1  ·  CHỦ NGHĨA DUY VẬT BIỆN CHỨNG", 0.84, 6.34, 6.6, 0.22, font=SANS_SEMI, size=8.4, color=GOLD, spacing=1.9, caps=True)

    s.notes_slide.notes_text_frame.text = "Kính chào thầy cô và các bạn. Chúng em là Nhóm 04. Hôm nay nhóm xin trình bày báo cáo thảo luận chuyên sâu về 3 Quy luật cơ bản và 5 Cặp phạm trù của phép biện chứng duy vật."
    return s


def populate_member_card(tb, header_num, header_text, items):
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(0.14)
    tf.margin_top = Inches(0.10)
    tf.margin_bottom = Inches(0.06)
    
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
        
        r_n = p.add_run()
        r_n.text = f"{name}  "
        r_n.font.name = DISPLAY
        r_n.font.bold = True
        r_n.font.size = Pt(9.6 if is_compact else 10.2)
        r_n.font.color.rgb = CREAM
        
        r_r = p.add_run()
        r_r.text = f"·  {role.upper()}\n"
        r_r.font.name = SANS_SEMI
        r_r.font.size = Pt(7.4 if is_compact else 8.0)
        r_r.font.color.rgb = GOLD_LIGHT
        r_r.font._element.set("spc", "90")
        
        r_d = p.add_run()
        r_d.text = f"“{desc}”"
        r_d.font.name = DISPLAY_IT
        r_d.font.italic = True
        r_d.font.size = Pt(7.5 if is_compact else 8.2)
        r_d.font.color.rgb = MUTED


# SLIDE 2: ĐỘI NGŨ THỰC HIỆN NHÓM 04
def build_slide_02(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    add_background(s)

    add_masthead(s)
    add_footer(s, 2, "ĐỘI NGŨ  ·  13 THÀNH VIÊN")
    add_side_badge(s, "TƯ DUY PHÊ PHÁN")

    # Heading
    add_text(s, "TEAM_KICKER", "ĐỘI NGŨ THỰC HIỆN  ·  NHÓM 04", 0.84, 1.15, 6.5, 0.20, font=SANS_SEMI, size=8.5, color=GOLD, spacing=1.6)
    add_text(s, "TEAM_TITLE", "CHÚNG TÔI", 0.80, 1.34, 3.6, 0.55, font=DISPLAY, size=38, color=GOLD, gradient=GOLD_STOPS)
    add_text(s, "TEAM_SUB", "mười ba thành viên, một tinh thần biện chứng", 3.82, 1.48, 4.95, 0.35, font=SCRIPT, size=18, color=GOLD_LIGHT, wrap=False)

    # Separator between grid and right column
    add_rect(s, "COLUMN_RULE", 8.85, 1.25, 0.008, 5.55, fill=GOLD, opacity=18)

    # 4 Cards for 13 members
    c1_items = [
        ("Nhóm Trưởng", "Điều phối chung", "Điều phối tiến độ & Tổng hợp các cặp phạm trù"),
        ("Nguyễn Anh Thư", "Thư ký học thuật", "Quản lý hồ sơ nghiên cứu & Tổng hợp phần quy luật"),
        ("Quyên Lê", "Thiết kế & Kỹ thuật", "Kiến trúc mỹ thuật, typography & chuyển động morph"),
    ]
    add_rect(s, "CARD_PANEL_1", 0.84, 1.98, 3.88, 2.38, fill=CARD_BG, line=GOLD, line_w=0.6, opacity=86, line_opacity=35)
    tb1 = add_text(s, "CARD_CONTENT_1", "", 0.84, 1.98, 3.88, 2.38)
    populate_member_card(tb1, "I", "Ban Điều Hành & Kỹ Thuật", c1_items)

    c2_items = [
        ("Trần Nam Anh", "Thuyết trình 01", "Dẫn dắt bài nói, phân tích cơ sở lý luận & luận điểm"),
        ("Giaa Minhh", "Thuyết trình 02", "Trình bày trực quan, liên hệ thực tiễn sinh động"),
        ("Phạm Văn Huy", "Câu hỏi thảo luận", "Nghiên cứu câu hỏi tương tác & phản biện mở rộng"),
    ]
    add_rect(s, "CARD_PANEL_2", 4.86, 1.98, 3.88, 2.38, fill=CARD_BG, line=GOLD, line_w=0.6, opacity=86, line_opacity=35)
    tb2 = add_text(s, "CARD_CONTENT_2", "", 4.86, 1.98, 3.88, 2.38)
    populate_member_card(tb2, "II", "Ban Thuyết Trình & Phản Biện", c2_items)

    c3_items = [
        ("Hồng Nhung", "QL Lượng – Chất", "Tích luỹ lượng đổi dẫn đến biến đổi về chất"),
        ("Khánh Linh", "QL Mâu Thuẫn", "Nguồn gốc, động lực nội tại của sự phát triển"),
        ("Hồng Nhung", "QL Phủ Định của PĐ", "Khuynh hướng vận động xoáy ốc tiến lên"),
        ("Nguyễn Anh Thư", "Tổng hợp & Lọc ý", "Đúc kết luận điểm trọng tâm của ba quy luật"),
    ]
    add_rect(s, "CARD_PANEL_3", 0.84, 4.46, 3.88, 2.44, fill=CARD_BG, line=GOLD, line_w=0.6, opacity=86, line_opacity=35)
    tb3 = add_text(s, "CARD_CONTENT_3", "", 0.84, 4.46, 3.88, 2.44)
    populate_member_card(tb3, "III", "Nghiên Cứu 3 Quy Luật Cơ Bản", c3_items)

    c4_items = [
        ("Phạm Duy", "Nguyên nhân – Kết quả", "Phân tích mối liên hệ nhân quả khách quan"),
        ("Đào Dươngg", "Tất nhiên – Ngẫu nhiên", "Bản chất bên trong & hiện tượng bên ngoài"),
        ("Vũ Minh Nghĩa", "Nội dung – Hình thức", "Thống nhất biện chứng giữa nội dung & hình thức"),
        ("Duy", "Khả năng – Hiện thực", "Điều kiện khách quan chuyển hoá vào thực tiễn"),
        ("Nhóm Trưởng", "Tổng hợp luận cứ", "Kiểm duyệt hệ thống luận cứ & kết luận"),
    ]
    add_rect(s, "CARD_PANEL_4", 4.86, 4.46, 3.88, 2.44, fill=CARD_BG, line=GOLD, line_w=0.6, opacity=86, line_opacity=35)
    tb4 = add_text(s, "CARD_CONTENT_4", "", 4.86, 4.46, 3.88, 2.44)
    populate_member_card(tb4, "IV", "Các Cặp Phạm Trù Biện Chứng", c4_items)

    # Right Column: Glow, Star, Ring, Medallion, Quote
    add_gradient_rect(s, "GLOW_PORTRAIT", 8.85, 0.25, 4.20, 4.20, [(0.0, "C23A32", 30), (0.55, "8E1A1E", 12), (1.0, "8E1A1E", 0)], radial=True)
    star = add_rect(s, "STAR_BACK", 9.15, 0.95, 4.20, 4.20, fill=None, line=GOLD, line_w=0.8, line_opacity=18, shape=MSO_SHAPE.STAR_5_POINT)
    star.rotation = 12
    add_rect(s, "ORBIT_RING", 9.54, 1.30, 3.42, 3.42, fill=None, line=GOLD, line_w=0.9, line_opacity=45, shape=MSO_SHAPE.OVAL)
    add_picture(s, MEDALLION, "PORTRAIT_LENIN", 9.72, 1.48, 3.06, 3.06, "Huy hiệu chân dung V. I. Lenin")

    add_text(s, "PORTRAIT_CAPTION", "V. I. LENIN  ·  1870 – 1924", 8.95, 4.76, 3.65, 0.22, font=SANS_SEMI, size=8.0, color=GOLD, spacing=1.8, align=PP_ALIGN.CENTER)
    add_text(s, "PORTRAIT_QUOTE", "“Không có lý luận cách mạng thì không có phong trào cách mạng.”", 9.00, 5.08, 3.55, 0.85, font=DISPLAY_IT, size=11.5, italic=True, color=CREAM, align=PP_ALIGN.CENTER, line_spacing=1.12)
    add_text(s, "PORTRAIT_SOURCE", "V. I. LÊNIN  ·  1902", 8.95, 6.00, 3.65, 0.20, font=SANS_SEMI, size=7.8, color=GOLD_LIGHT, spacing=1.6, align=PP_ALIGN.CENTER)

    s.notes_slide.notes_text_frame.text = "Nhóm 04 gồm 13 thành viên phối hợp chặt chẽ trên 4 phân ban: Ban Điều hành & Kỹ thuật, Ban Thuyết trình & Phản biện, Nhóm Nghiên cứu 3 Quy luật và Nhóm Nghiên cứu 5 Cặp phạm trù."
    return s


# SLIDE 3: MỤC LỤC TỔNG QUAN BÀI THẢO LUẬN
def build_slide_03(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    add_background(s)
    add_masthead(s)
    add_footer(s, 3, "TỔNG QUAN NỘI DUNG")
    add_side_badge(s, "CẤU TRÚC BÀI NÓI")
    add_slide_header(s, "NỘI DUNG BÁO CÁO", "Cấu Trúc Hệ Thống Luận Điểm")

    # 2 Cột lớn: Phần I và Phần II
    p1_items = [
        ("01", "Quy luật Chuyển hóa Lượng – Chất: Cách thức vận động và phát triển"),
        ("02", "Quy luật Mâu thuẫn (Hạt nhân): Nguồn gốc và động lực nội tại"),
        ("03", "Quy luật Phủ định của phủ định: Khuynh hướng vận động xoáy ốc tiến lên"),
    ]
    add_card(s, "AGENDA_P1", 0.84, 2.20, 5.75, 4.45, "PHẦN I: BA QUY LUẬT CƠ BẢN", p1_items, badge_num="I", highlight_title=True)

    p2_items = [
        ("01", "Nguyên nhân và Kết quả: Mối liên hệ sản sinh khách quan"),
        ("02", "Tất nhiên và Ngẫu nhiên: Vai trò quyết định & yếu tố bổ sung"),
        ("03", "Nội dung và Hình thức: Thống nhất biện chứng & sự phù hợp"),
        ("04", "Bản chất và Hiện tượng: Bản chất bên trong bộc lộ qua biểu hiện ngoài"),
        ("05", "Khả năng và Hiện thực: Điều kiện khách quan để biến tiềm năng thành hiện thực"),
    ]
    add_card(s, "AGENDA_P2", 6.84, 2.20, 5.75, 4.45, "PHẦN II: NĂM CẶP PHẠM TRÙ", p2_items, badge_num="II", highlight_title=True)

    s.notes_slide.notes_text_frame.text = "Nội dung báo cáo hôm nay gồm 2 trụ cột căn bản: Phần I làm rõ 3 Quy luật lớn chỉ ra cách thức, động lực và khuynh hướng; Phần II đi sâu vào 5 cặp phạm trù phản ánh các mối liên hệ phổ biến."
    return s


# SLIDE 4: BANNER CHUYỂN MỤC PHẦN I
def build_slide_04(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    add_background(s)
    add_masthead(s)
    add_footer(s, 4, "PHẦN I  ·  3 QUY LUẬT")
    add_side_badge(s, "PHẦN I · QUY LUẬT")

    add_text(s, "SEC1_NUM", "PHẦN I", 0.84, 1.85, 8.5, 0.40, font=SANS_SEMI, size=14, color=GOLD, spacing=3.0, caps=True)
    add_text(s, "SEC1_TITLE_1", "BA QUY LUẬT CƠ BẢN", 0.80, 2.30, 11.5, 1.10, font=DISPLAY, size=58, color=CREAM, shadow=True, wrap=False)
    add_text(s, "SEC1_TITLE_2", "CỦA PHÉP BIỆN CHỨNG DUY VẬT", 0.80, 3.45, 11.5, 1.10, font=DISPLAY, size=48, color=GOLD, gradient=GOLD_STOPS, shadow=True, wrap=False)

    add_rect(s, "SEC1_RULE", 0.84, 4.75, 3.50, 0.016, fill=GOLD, opacity=85)
    add_text(s, "SEC1_DESC", "“Phép biện chứng là môn khoa học về những quy luật phổ biến của sự vận động và sự phát triển của tự nhiên, của xã hội loài người và của tư duy.”",
             0.84, 5.05, 9.8, 0.95, font=DISPLAY_IT, size=16.5, color=CREAM, line_spacing=1.15)
    add_text(s, "SEC1_SRC", "— PH. ĂNG-GHEN (Chống Đuy-rinh)", 0.84, 6.15, 6.5, 0.25, font=SANS_SEMI, size=8.5, color=MUTED, spacing=1.6)

    s.notes_slide.notes_text_frame.text = "Chúng ta bắt đầu với Phần I: Ba quy luật cơ bản của phép biện chứng duy vật. Đây là những quy luật phổ biến nhất chi phối mọi quá trình vận động trong tự nhiên, xã hội và tư duy."
    return s


# SLIDE 5: QUY LUẬT LƯỢNG - CHẤT (KHÁI NIỆM & ĐẶC TRƯNG)
def build_slide_05(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    add_background(s)
    add_masthead(s)
    add_footer(s, 5, "QUY LUẬT LƯỢNG – CHẤT")
    add_side_badge(s, "QUY LUẬT 01")
    add_slide_header(s, "QUY LUẬT 01  ·  CÁCH THỨC CỦA SỰ PHÁT TRIỂN", "Quy Luật Lượng – Chất: Khái Niệm & Đặc Trưng")

    c1 = [
        ("Khái niệm", "Tính quy định khách quan vốn có của sự vật, là sự thống nhất hữu cơ các thuộc tính làm cho sự vật là nó chứ không phải là cái khác."),
        ("Tính khách quan", "Gắn liền hữu cơ với sự vật; không có chất thuần túy tồn tại ngoài sự vật."),
        ("Tính ổn định", "Có tính ổn định tương đối, nói lên mặt đứng im tương đối của sự vật."),
        ("Ví dụ điển hình", "Đồng có màu đỏ ánh kim, dẫn điện, dẫn nhiệt tốt, dẻo. Than chì và kim cương cùng từ cacbon nhưng liên kết khác nhau nên chất khác nhau."),
    ]
    add_card(s, "QC_CHAT", 0.84, 2.15, 5.75, 4.50, "TÍNH QUY ĐỊNH VỀ CHẤT", c1, badge_num="01")

    c2 = [
        ("Khái niệm", "Tính quy định khách quan vốn có về mặt số lượng, quy mô, trình độ, nhịp điệu của sự vận động và phát triển của sự vật."),
        ("Hình thức biểu thị", "Xác định bằng đơn vị đo lường cụ thể hoặc các đại lượng trừu tượng, khái quát."),
        ("Tính biến đổi", "Nói lên mặt thường xuyên biến đổi của sự vật trong tiến trình vận động."),
        ("Ví dụ điển hình", "Cây trồng: lượng là chiều cao, số lá, sinh khối; Số 8: lượng chỉ 8 đơn vị cụ thể, phân biệt với các lượng khác."),
    ]
    add_card(s, "QC_LUONG", 6.84, 2.15, 5.75, 4.50, "TÍNH QUY ĐỊNH VỀ LƯỢNG", c2, badge_num="02")

    s.notes_slide.notes_text_frame.text = "Quy luật này trả lời cho câu hỏi: Sự vật phát triển theo cách thức nào? Chất là mặt ổn định tương đối tạo nên bản sắc sự vật, còn lượng là mặt thường xuyên biến đổi."
    return s


# SLIDE 6: QUY LUẬT LƯỢNG - CHẤT (ĐỘ - ĐIỂM NÚT - BƯỚC NHẢY)
def build_slide_06(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    add_background(s)
    add_masthead(s)
    add_footer(s, 6, "QUY LUẬT LƯỢNG – CHẤT")
    add_side_badge(s, "QUY LUẬT 01")
    add_slide_header(s, "CƠ CHẾ BIẾN ĐỔI BIỆN CHỨNG", "Mối Quan Hệ: Độ — Điểm Nút — Bước Nhảy")

    # 3 Khối quy trình chuyển hóa
    step1 = [
        ("Định nghĩa", "Khoảng giới hạn mà sự thay đổi về lượng chưa làm thay đổi căn bản chất của sự vật."),
        ("Đặc tính", "Sự vật vẫn là nó, lượng biến đổi âm thầm nhưng chất cũ được bảo tồn."),
    ]
    add_card(s, "STEP_DO", 0.84, 2.20, 3.75, 2.50, "1. ĐỘ (GIỚI HẠN)", step1, badge_num="A")

    step2 = [
        ("Định nghĩa", "Thời điểm, giới hạn mà tại đó sự thay đổi về lượng đủ để làm thay đổi chất của sự vật."),
        ("Đặc tính", "Ranh giới kết thúc của một độ cũ, chuẩn bị cho bước chuyển hóa."),
    ]
    add_card(s, "STEP_NUT", 4.84, 2.20, 3.75, 2.50, "2. ĐIỂM NÚT (NGƯỠNG)", step2, badge_num="B")

    step3 = [
        ("Định nghĩa", "Sự chuyển hóa về chất do những thay đổi về lượng trước đó gây ra tại điểm nút."),
        ("Đặc tính", "Chất cũ mất đi, chất mới ra đời mở ra một độ mới cao hơn."),
    ]
    add_card(s, "STEP_NHAY", 8.84, 2.20, 3.75, 2.50, "3. BƯỚC NHẢY (CHẤT MỚI)", step3, badge_num="C")

    # Khung ví dụ thực tiễn sinh viên ở dưới
    vd_items = [
        ("Tích lũy lượng", "Sinh viên học tập từng ngày, tích lũy số giờ đọc sách, bài tập, vốn kiến thức."),
        ("Trong khoảng Độ", "Kiến thức tăng dần nhưng trình độ chung chưa có sự thay đổi đột phá."),
        ("Điểm nút & Bước nhảy", "Vượt qua kỳ thi tốt nghiệp / bảo vệ khóa luận; chuyển từ Trung bình sang Khá, Giỏi."),
        ("Chất mới tác động ngược lại lượng", "Khi trình độ được nâng lên, sinh viên tiếp thu kiến thức nhanh hơn, giải quyết bài tập khó hơn."),
    ]
    add_card(s, "VD_STUDENT", 0.84, 4.90, 11.75, 1.85, "VÍ DỤ THỰC TIỄN: QUÁ TRÌNH HỌC TẬP CỦA SINH VIÊN", vd_items, highlight_title=True)

    s.notes_slide.notes_text_frame.text = "Lượng đổi dẫn đến chất đổi. Sự biến đổi phải tích lũy trong độ, đạt điểm nút mới thực hiện bước nhảy. Khi có chất mới, nó sẽ quay lại kích thích lượng tích lũy với tốc độ cao hơn."
    return s


# SLIDE 7: QUY LUẬT LƯỢNG - CHẤT (Ý NGHĨA PHƯƠNG PHÁP LUẬN)
def build_slide_07(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    add_background(s)
    add_masthead(s)
    add_footer(s, 7, "QUY LUẬT LƯỢNG – CHẤT")
    add_side_badge(s, "PHƯƠNG PHÁP LUẬN")
    add_slide_header(s, "Ý NGHĨA PHƯƠNG PHÁP LUẬN", "Vận Dụng Quy Luật Lượng – Chất Vào Thực Tiễn")

    c1 = [
        ("Tích lũy kiên trì", "Muốn có biến đổi về chất phải kiên trì tích lũy đủ về lượng; không thể đốt cháy giai đoạn."),
        ("Chống bệnh chủ quan nóng vội", "Phê phán tư tưởng 'tả khuynh', chưa tích lũy đủ lượng đã nôn nóng thực hiện bước nhảy liều lĩnh."),
        ("Chống bệnh bảo thủ trì trệ", "Phê phán tư tưởng 'hữu khuynh', lượng đã chín muồi nhưng do do dự, ngại đổi mới mà không dám thực hiện bước nhảy."),
    ]
    add_card(s, "PPL_1", 0.84, 2.20, 5.75, 4.45, "NGUYÊN TẮC TÍCH LŨY & BƯỚC NHẢY", c1, badge_num="I")

    c2 = [
        ("Vận dụng linh hoạt các bước nhảy", "Tùy điều kiện cụ thể để lựa chọn bước nhảy toàn bộ hay cục bộ, bước nhảy đột biến hay dần dần."),
        ("Thay đổi phương thức liên kết", "Chất của sự vật còn do phương thức liên kết giữa các yếu tố tạo thành; sắp xếp lại tổ chức có thể tạo ra chất mới."),
        ("Liên hệ học tập", "Tích lũy kiến thức bền bỉ từng ngày, rèn luyện tư duy phản biện, chuẩn bị kỹ lưỡng để vượt qua các kỳ thi lớn."),
    ]
    add_card(s, "PPL_2", 6.84, 2.20, 5.75, 4.45, "LINH HOẠT VÀ TÁI CẤU TRÚC", c2, badge_num="II")

    s.notes_slide.notes_text_frame.text = "Ý nghĩa lớn nhất là nhắc nhở chúng ta: muốn thành tài phải học hành chăm chỉ tích lũy kiến thức, khắc phục bệnh nóng vội muốn đốt cháy giai đoạn cũng như bệnh ỷ lại, lười biếng."
    return s


# SLIDE 8: QUY LUẬT MÂU THUẪN (HẠT NHÂN CỦA PHÉP BIỆN CHỨNG)
def build_slide_08(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    add_background(s)
    add_masthead(s)
    add_footer(s, 8, "QUY LUẬT MÂU THUẪN")
    add_side_badge(s, "QUY LUẬT 02")
    add_slide_header(s, "QUY LUẬT 02  ·  NGUỒN GỐC CỦA SỰ PHÁT TRIỂN", "Quy Luật Mâu Thuẫn: Hạt Nhân Phép Biện Chứng")

    c1 = [
        ("Vị trí cốt lõi", "Là quy luật quan trọng nhất, được Lênin coi là 'hạt nhân' của phép biện chứng duy vật."),
        ("Tính khách quan & phổ biến", "Tồn tại trong mọi lĩnh vực: tự nhiên, xã hội và tư duy; không phụ thuộc ý muốn chủ quan."),
        ("Vai trò định hướng", "Chỉ rõ nguồn gốc và động lực nội tại của mọi sự vận động, biến đổi và phát triển."),
    ]
    add_card(s, "MT_VITRI", 0.84, 2.20, 5.75, 4.45, "VỊ TRÍ & VAI TRÒ CỦA QUY LUẬT", c1, badge_num="01")

    c2 = [
        ("Mặt đối lập", "Những mặt có những đặc điểm, thuộc tính, khuynh hướng biến đổi trái ngược nhau tồn tại khách quan. Ví dụ: Người mua muốn giá thấp, Người bán muốn giá cao."),
        ("Mâu thuẫn biện chứng", "Chỉ mối liên hệ thống nhất, đấu tranh và chuyển hoá giữa các mặt đối lập của sự vật, hiện tượng. Ví dụ: Lực hút và lực đẩy trong cấu trúc vật chất."),
        ("Tính biện chứng", "Các mặt đối lập vừa nương tựa nhau vừa bài trừ nhau, tạo thành xung lực phát triển."),
    ]
    add_card(s, "MT_KHAINIEM", 6.84, 2.20, 5.75, 4.45, "MẶT ĐỐI LẬP & MÂU THUẪN", c2, badge_num="02")

    s.notes_slide.notes_text_frame.text = "Lênin khẳng định quy luật mâu thuẫn là hạt nhân của phép biện chứng. Không có mâu thuẫn thì không có vận động; chính xung đột nội tại giữa các mặt đối lập là động lực thúc đẩy sự vật đi lên."
    return s


# SLIDE 9: QUY LUẬT MÂU THUẪN (THỐNG NHẤT & ĐẤU TRANH)
def build_slide_09(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    add_background(s)
    add_masthead(s)
    add_footer(s, 9, "QUY LUẬT MÂU THUẪN")
    add_side_badge(s, "QUY LUẬT 02")
    add_slide_header(s, "CƠ CHẾ NGUỒN GỐC & ĐỘNG LỰC", "Sự Thống Nhất & Đấu Tranh Của Các Mặt Đối Lập")

    c1 = [
        ("Định nghĩa", "Sự liên hệ, ràng buộc, phụ thuộc và làm tiền đề tồn tại cho nhau; mặt này lấy mặt kia làm điều kiện tồn tại."),
        ("Tính chất", "Mang tính tương đối, tạm thời, gắn liền với trạng thái đứng im tương đối của sự vật."),
        ("Ví dụ", "Trong cơ thể sống có quá trình Đồng hóa và Dị hóa luôn gắn kết phụ thuộc lẫn nhau."),
    ]
    add_card(s, "MT_THONGNHAT", 0.84, 2.20, 5.75, 4.45, "SỰ THỐNG NHẤT CÁC MẶT ĐỐI LẬP", c1, badge_num="A")

    c2 = [
        ("Định nghĩa", "Sự tác động qua lại theo xu hướng bài trừ, phủ định và chống đối lẫn nhau giữa các mặt đối lập."),
        ("Tính chất", "Mang tính tuyệt đối, diễn ra liên tục không ngừng trong suốt quá trình tồn tại của mâu thuẫn."),
        ("Tiến trình phát triển", "Từ khác biệt → đối lập → xung đột gay gắt → chuyển hóa lẫn nhau → phá vỡ thể thống nhất cũ, hình thành sự vật mới."),
    ]
    add_card(s, "MT_DAUTRANH", 6.84, 2.20, 5.75, 4.45, "SỰ ĐẤU TRANH CÁC MẶT ĐỐI LẬP", c2, badge_num="B")

    s.notes_slide.notes_text_frame.text = "Thống nhất là tạm thời, đấu tranh là tuyệt đối. Khi đấu tranh đạt tới đỉnh điểm, sự thống nhất cũ bị phá vỡ, sự vật cũ chuyển thành sự vật mới và một mâu thuẫn mới lại xuất hiện."
    return s


# SLIDE 10: QUY LUẬT MÂU THUẪN (Ý NGHĨA & LIÊN HỆ BẢN THÂN)
def build_slide_10(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    add_background(s)
    add_masthead(s)
    add_footer(s, 10, "QUY LUẬT MÂU THUẪN")
    add_side_badge(s, "PHƯƠNG PHÁP LUẬN")
    add_slide_header(s, "Ý NGHĨA PHƯƠNG PHÁP LUẬN & LIÊN HỆ BẢN THÂN", "Nhận Thức & Giải Quyết Mâu Thuẫn Trong Đời Sống")

    c1 = [
        ("Thừa nhận mâu thuẫn khách quan", "Không né tránh, lo sợ mâu thuẫn; xem mâu thuẫn là hiện tượng tất yếu của sự phát triển."),
        ("Phân tích cụ thể mâu thuẫn", "Phân biệt mâu thuẫn bên trong/bên ngoài, cơ bản/không cơ bản, chủ yếu/thứ yếu để tìm phương pháp giải quyết đúng."),
        ("Giải quyết bằng đấu tranh", "Mâu thuẫn phải được giải quyết bằng đấu tranh giữa các mặt đối lập, tuyệt đối không điều hòa mâu thuẫn một cách thỏa hiệp vô nguyên tắc."),
    ]
    add_card(s, "MT_PPL", 0.84, 2.20, 5.75, 4.45, "Ý NGHĨA PHƯƠNG PHÁP LUẬN", c1, badge_num="I")

    c2 = [
        ("Trong học tập", "Đấu tranh không ngừng giữa sự lười biếng và tính chăm chỉ; chủ động tìm tòi giải quyết những kiến thức chưa hiểu."),
        ("Trong đời sống", "Khi gặp khó khăn hay bất đồng, cần bình tĩnh phân tích bản chất vấn đề để tìm cách giải quyết phù hợp, không trốn tránh."),
        ("Rèn luyện bản thân", "Thẳng thắn nhìn nhận những thói quen xấu, khiếm khuyết của bản thân để kiên quyết đấu tranh hoàn thiện nhân cách."),
    ]
    add_card(s, "MT_LIENHE", 6.84, 2.20, 5.75, 4.45, "BÀI HỌC LIÊN HỆ BẢN THÂN", c2, badge_num="II")

    s.notes_slide.notes_text_frame.text = "Bài học thực tiễn: Sinh viên không được sợ va chạm hay sợ mâu thuẫn. Trong chính bản thân mỗi người luôn có sự giằng co giữa chăm chỉ và lười biếng; chiến thắng sự trì trệ chính là phát triển."
    return s


# SLIDE 11: QUY LUẬT PHỦ ĐỊNH CỦA PHỦ ĐỊNH (PHỦ ĐỊNH BIỆN CHỨNG)
def build_slide_11(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    add_background(s)
    add_masthead(s)
    add_footer(s, 11, "PHỦ ĐỊNH CỦA PHỦ ĐỊNH")
    add_side_badge(s, "QUY LUẬT 03")
    add_slide_header(s, "QUY LUẬT 03  ·  KHUYNH HƯỚNG CỦA SỰ PHÁT TRIỂN", "Quy Luật Phủ Định Của Phủ Định: Bản Chất Biện Chứng")

    c1 = [
        ("Vị trí quy luật", "Chỉ ra khuynh hướng, con đường vận động tiến lên của sự vật, hiện tượng."),
        ("Phủ định thông thường", "Sự thay thế đơn thuần của sự vật này bằng sự vật khác."),
        ("Phủ định biện chứng", "Sự phủ định tự thân, tạo điều kiện, tiền đề cho quá trình phát triển tiếp theo của sự vật."),
    ]
    add_card(s, "PD_KHAINIEM", 0.84, 2.20, 5.75, 4.45, "KHÁI NIỆM & VỊ TRÍ", c1, badge_num="01")

    c2 = [
        ("Tính khách quan", "Bắt nguồn từ việc giải quyết mâu thuẫn bên trong sự vật, là quá trình tự thân không phụ thuộc ý muốn chủ quan."),
        ("Tính kế thừa", "Không xóa bỏ sạch trơn; loại bỏ yếu tố lạc hậu, giữ lại và cải tạo những yếu tố tích cực của cái cũ cho cái mới."),
        ("Ví dụ thực tiễn", "Chuyển từ việc đọc sách thụ động sang chủ động ghi chú, tổng hợp; tiếp thu tinh hoa văn hóa truyền thống trong xã hội hiện đại."),
    ]
    add_card(s, "PD_TINHTHAT", 6.84, 2.20, 5.75, 4.45, "HAI TÍNH CHẤT CƠ BẢN", c2, badge_num="02")

    s.notes_slide.notes_text_frame.text = "Quy luật phủ định của phủ định chỉ ra khuynh hướng phát triển. Phủ định biện chứng có tính khách quan và tính kế thừa: cái mới ra đời không phủ nhận sạch trơn cái cũ mà kế thừa những giá trị tiến bộ."
    return s


# SLIDE 12: QUY LUẬT PHỦ ĐỊNH CỦA PHỦ ĐỊNH (CON ĐƯỜNG XOÁY ỐC)
def build_slide_12(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    add_background(s)
    add_masthead(s)
    add_footer(s, 12, "PHỦ ĐỊNH CỦA PHỦ ĐỊNH")
    add_side_badge(s, "QUY LUẬT 03")
    add_slide_header(s, "HÌNH THỨC PHÁT TRIỂN XOẮN ỐC", "Chu Kỳ Phát Triển & Phương Pháp Luận Thực Tiễn")

    c1 = [
        ("Bản chất chu kỳ", "Qua ít nhất hai lần phủ định biện chứng, sự vật dường như quay lại điểm xuất phát ban đầu nhưng trên nền tảng cao hơn."),
        ("Con đường xoắn ốc", "Sự phát triển không diễn ra theo đường thẳng tắp mà theo đường xoắn ốc quanh co, phức tạp gồm: tính kế thừa, tính chu kỳ và tính tiến lên."),
        ("Ví dụ sinh viên", "Dùng kiến thức THPT làm nền tảng → tiếp thu tri thức đại học → vận dụng vào thực hành nghiên cứu chuyên sâu."),
    ]
    add_card(s, "PD_XOAYOC", 0.84, 2.20, 5.75, 4.45, "CON ĐƯỜNG PHÁT TRIỂN XOẮN ỐC", c1, badge_num="A")

    c2 = [
        ("Kiên định mục tiêu", "Hiểu rằng phát triển là quanh co, có lúc thụt lùi tạm thời; phải vững vàng niềm tin, xem xét nguyên nhân thất bại để khắc phục."),
        ("Chống phủ định sạch trơn", "Có thái độ tôn trọng cái cũ, kế thừa các giá trị văn hóa và tri thức truyền thống."),
        ("Chống kế thừa nguyên xi", "Ủng hộ cái mới, cái tiến bộ; không sao chép máy móc những mô hình lỗi thời."),
        ("Làm việc nhóm", "Mỗi lần tranh luận khó khăn là một lần rút kinh nghiệm để phối hợp hiệu quả hơn."),
    ]
    add_card(s, "PD_PPL", 6.84, 2.20, 5.75, 4.45, "Ý NGHĨA PHƯƠNG PHÁP LUẬN", c2, badge_num="B")

    s.notes_slide.notes_text_frame.text = "Sự phát triển đi theo đường xoắn ốc: dường như quay về cái ban đầu nhưng ở trình độ cao hơn. Trong học tập và nghiên cứu, thất bại tạm thời chỉ là khúc quanh trên đường đi lên."
    return s


# SLIDE 13: BANNER CHUYỂN MỤC PHẦN II
def build_slide_13(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    add_background(s)
    add_masthead(s)
    add_footer(s, 13, "PHẦN II  ·  5 CẶP PHẠM TRÙ")
    add_side_badge(s, "PHẦN II · PHẠM TRÙ")

    add_text(s, "SEC2_NUM", "PHẦN II", 0.84, 1.85, 8.5, 0.40, font=SANS_SEMI, size=14, color=GOLD, spacing=3.0, caps=True)
    add_text(s, "SEC2_TITLE_1", "NĂM CẶP PHẠM TRÙ CƠ BẢN", 0.80, 2.30, 11.5, 1.10, font=DISPLAY, size=50, color=CREAM, shadow=True, wrap=False)
    add_text(s, "SEC2_TITLE_2", "CỦA PHÉP BIỆN CHỨNG DUY VẬT", 0.80, 3.40, 11.5, 1.10, font=DISPLAY, size=46, color=GOLD, gradient=GOLD_STOPS, shadow=True, wrap=False)

    add_rect(s, "SEC2_RULE", 0.84, 4.75, 3.50, 0.016, fill=GOLD, opacity=85)
    add_text(s, "SEC2_DESC", "“Các phạm trù là những nấc thang của sự nhận thức thế giới, là những điểm nút trong mạng lưới giúp con người nhận thức và làm chủ giới tự nhiên.”",
             0.84, 5.05, 9.8, 0.95, font=DISPLAY_IT, size=16.5, color=CREAM, line_spacing=1.15)
    add_text(s, "SEC2_SRC", "— V. I. LÊNIN (Bút ký triết học)", 0.84, 6.15, 6.5, 0.25, font=SANS_SEMI, size=8.5, color=MUTED, spacing=1.6)

    s.notes_slide.notes_text_frame.text = "Chúng ta bước sang Phần II: Năm cặp phạm trù cơ bản. Các phạm trù phản ánh những mối liên hệ phổ biến nhất giữa các mặt của hiện thực khách quan."
    return s


# SLIDE 14: CẶP PHẠM TRÙ I & II (NGUYÊN NHÂN - KẾT QUẢ & TẤT NHIÊN - NGẪU NHIÊN)
def build_slide_14(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    add_background(s)
    add_masthead(s)
    add_footer(s, 14, "CẶP PHẠM TRÙ 01 & 02")
    add_side_badge(s, "PHẠM TRÙ I & II")
    add_slide_header(s, "CÁC MỐI LIÊN HỆ PHỔ BIẾN", "Nguyên Nhân – Kết Quả & Tất Nhiên – Ngẫu Nhiên")

    c1 = [
        ("Khái niệm", "Nguyên nhân là sự tác động lẫn nhau gây ra biến đổi; Kết quả là biến đổi xuất hiện do nguyên nhân tạo thành."),
        ("Mối quan hệ", "Nguyên nhân luôn đi trước kết quả; một nguyên nhân có thể sinh nhiều kết quả; có thể đổi vị trí cho nhau theo chuỗi mắt xích."),
        ("Ví dụ", "Chặt phá rừng → lũ lụt, xói mòn, biến đổi khí hậu; Chăm học → điểm tốt → việc làm ổn định."),
        ("Phương pháp luận", "Muốn xóa bỏ hiện tượng tiêu cực phải tìm đúng nguyên nhân; phân biệt nguyên nhân chủ yếu/thứ yếu."),
    ]
    add_card(s, "CAT_NN_KQ", 0.84, 2.20, 5.75, 4.45, "1. NGUYÊN NHÂN VÀ KẾT QUẢ", c1, badge_num="01")

    c2 = [
        ("Khái niệm", "Tất nhiên do nguyên nhân bên trong quyết định, nhất định phải xảy ra; Ngẫu nhiên do nhân tố bên ngoài ngẫu hợp quyết định."),
        ("Mối quan hệ", "Cùng tồn tại khách quan; Cái tất nhiên đóng vai trò quyết định và luôn vạch đường đi qua vô số cái ngẫu nhiên."),
        ("Ví dụ", "Con người sinh ra tất nhiên sẽ chết; Gieo đồng xu có mặt sấp/ngửa là tất nhiên, mặt nào rơi trúng là ngẫu nhiên."),
        ("Phương pháp luận", "Hoạt động thực tiễn phải dựa vào cái tất nhiên; đồng thời dự phòng phương án cho các tình huống ngẫu nhiên bất ngờ."),
    ]
    add_card(s, "CAT_TN_NN", 6.84, 2.20, 5.75, 4.45, "2. TẤT NHIÊN VÀ NGẪU NHIÊN", c2, badge_num="02")

    s.notes_slide.notes_text_frame.text = "Cặp 1 nhắc ta: không có kết quả nào không có nguyên nhân. Cặp 2 nhắc ta: trong học tập, điểm cao đến từ sự rèn luyện bền bỉ (tất nhiên), chứ không thể trông chờ vào may rủi (ngẫu nhiên)."
    return s


# SLIDE 15: CẶP PHẠM TRÙ III & IV (NỘI DUNG - HÌNH THỨC & BẢN CHẤT - HIỆN TƯỢNG)
def build_slide_15(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    add_background(s)
    add_masthead(s)
    add_footer(s, 15, "CẶP PHẠM TRÙ 03 & 04")
    add_side_badge(s, "PHẠM TRÙ III & IV")
    add_slide_header(s, "CÁC MỐI LIÊN HỆ PHỔ BIẾN", "Nội Dung – Hình Thức & Bản Chất – Hiện Tượng")

    c1 = [
        ("Khái niệm", "Nội dung là tổng hợp các yếu tố tạo nên sự vật; Hình thức là phương thức tổ chức, liên kết các yếu tố đó."),
        ("Mối quan hệ", "Nội dung quyết định hình thức; hình thức phù hợp thúc đẩy nội dung, hình thức lỗi thời kìm hãm sự phát triển."),
        ("Ví dụ thực tiễn", "Đổi mới quản lý kinh tế năm 1986 ở Việt Nam; Nội dung học tập là tri thức, hình thức là phương pháp học phù hợp."),
        ("Phương pháp luận", "Căn cứ vào nội dung để chọn hình thức; kiên quyết thay đổi hình thức khi nó trở nên lạc hậu."),
    ]
    add_card(s, "CAT_ND_HT", 0.84, 2.20, 5.75, 4.45, "3. NỘI DUNG VÀ HÌNH THỨC", c1, badge_num="03")

    c2 = [
        ("Khái niệm", "Bản chất là tổng thể mối liên hệ ổn định sâu xa bên trong; Hiện tượng là biểu hiện bên ngoài của bản chất."),
        ("Mối quan hệ", "Thống nhất: bản chất bộc lộ qua hiện tượng; Mâu thuẫn: hiện tượng có thể biểu hiện sai lệch hoặc xuyên tạc bản chất."),
        ("Ví dụ", "Chế độ tư bản trả lương cao để che giấu bản chất bóc lột giá trị thặng dư."),
        ("Phương pháp luận", "Không đánh giá con người, sự vật chỉ qua vẻ bề ngoài; trong học tập không chạy theo điểm số ảo mà chú trọng thực chất."),
    ]
    add_card(s, "CAT_BC_HT", 6.84, 2.20, 5.75, 4.45, "4. BẢN CHẤT VÀ HIỆN TƯỢNG", c2, badge_num="04")

    s.notes_slide.notes_text_frame.text = "Nội dung quyết định hình thức; bản chất chi phối hiện tượng. Đừng để hiện tượng bên ngoài đánh lừa; muốn thấu hiểu bản chất phải nghiên cứu sâu sắc nhiều hiện tượng đa chiều."
    return s


# SLIDE 16: CẶP PHẠM TRÙ V (KHẢ NĂNG VÀ HIỆN THỰC)
def build_slide_16(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    add_background(s)
    add_masthead(s)
    add_footer(s, 16, "CẶP PHẠM TRÙ 05")
    add_side_badge(s, "PHẠM TRÙ V")
    add_slide_header(s, "CƠ CHẾ CHUYỂN HÓA VÀ HÀNH ĐỘNG", "Khả Năng Và Hiện Thực: Điều Kiện Để Chuyển Hóa")

    c1 = [
        ("Khái niệm Khả năng", "Những cái hiện chưa có, đang tồn tại tiềm ẩn trong sự vật nhưng sẽ xuất hiện khi có điều kiện thích hợp."),
        ("Khái niệm Hiện thực", "Những cái đã xuất hiện, đang tồn tại thực sự (gồm hiện thực khách quan và hiện thực chủ quan)."),
        ("Mối quan hệ biện chứng", "Khả năng và hiện thực gắn bó chặt chẽ, thường xuyên chuyển hóa cho nhau. Hiện thực được chuẩn bị bởi khả năng; khả năng hướng tới thành hiện thực."),
    ]
    add_card(s, "CAT_KN_HT", 0.84, 2.20, 5.75, 4.45, "KHÁI NIỆM & MỐI QUAN HỆ", c1, badge_num="05")

    c2 = [
        ("Điều kiện chuyển hóa", "Cần có một tập hợp điều kiện cần và đủ để khả năng biến thành hiện thực. Ví dụ: Cách mạng XHCN cần tình thế và thời cơ cách mạng chín muồi."),
        ("Ý nghĩa phương pháp luận", "Thực tiễn phải dựa vào hiện thực, không được ảo tưởng dựa vào khả năng chưa có; nhưng phải chủ động tạo điều kiện biến khả năng tốt thành hiện thực."),
        ("Liên hệ sinh viên", "Mọi sinh viên đều có khả năng ra trường loại Giỏi, nhưng phải bằng hành động cụ thể: kỷ luật tự giác, rèn luyện kỹ năng, nỗ lực tích lũy tri thức."),
    ]
    add_card(s, "CAT_KN_PPL", 6.84, 2.20, 5.75, 4.45, "ĐIỀU KIỆN & HÀNH ĐỘNG THỰC TIỄN", c2, badge_num="PPL")

    s.notes_slide.notes_text_frame.text = "Khả năng không tự động biến thành hiện thực nếu thiếu điều kiện và nỗ lực chủ quan. Sinh viên muốn biến ước mơ sự nghiệp thành hiện thực phải bắt đầu từ hành động cụ thể hôm nay."
    return s


# SLIDE 17: TỔNG KẾT PHƯƠNG PHÁP LUẬN TOÀN BÀI
def build_slide_17(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    add_background(s)
    add_masthead(s)
    add_footer(s, 17, "TỔNG KẾT LUẬN ĐIỂM")
    add_side_badge(s, "TỔNG KẾT")
    add_slide_header(s, "GIÁ TRỊ CỐT LÕI CỦA PHÉP BIỆN CHỨNG", "Tổng Kết: Thế Giới Quan Khoa Học & Tư Duy Biện Chứng")

    c1 = [
        ("Về quy luật phát triển", "Hiểu rằng mọi sự vật phát triển theo cách tích lũy lượng → chất, động lực từ giải quyết mâu thuẫn, khuynh hướng xoắn ốc tiến lên."),
        ("Tránh các sai lầm tư duy", "Chống giáo điều, máy móc; khắc phục bệnh nôn nóng đốt cháy giai đoạn cũng như bệnh bảo thủ trì trệ."),
    ]
    add_card(s, "SUM_1", 0.84, 2.20, 5.75, 4.45, "HỆ THỐNG QUY LUẬT PHỔ BIẾN", c1, badge_num="I")

    c2 = [
        ("Về phương pháp nhận thức", "Đi từ hiện tượng vào bản chất, tìm đúng nguyên nhân khách quan, nắm bắt cái tất nhiên và chuẩn bị các điều kiện thực tiễn."),
        ("Hành động thực tiễn", "Xây dựng tư duy phản biện khoa học, chủ động thích ứng với biến động và không ngừng hoàn thiện bản thân trong kỷ nguyên mới."),
    ]
    add_card(s, "SUM_2", 6.84, 2.20, 5.75, 4.45, "PHƯƠNG PHÁP HÀNH ĐỘNG", c2, badge_num="II")

    s.notes_slide.notes_text_frame.text = "Tổng kết lại: Phép biện chứng duy vật cung cấp cho chúng ta một thế giới quan khoa học và phương pháp luận sắc bén để nhận thức và cải tạo thế giới."
    return s


# SLIDE 18: LỜI CẢM ƠN & THẢO LUẬN (Q&A)
def build_slide_18(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    add_background(s)

    star = add_rect(s, "STAR_BACK", 7.55, 0.55, 7.05, 7.05, fill=None, line=GOLD, line_w=0.8, line_opacity=13, shape=MSO_SHAPE.STAR_5_POINT)
    star.rotation = 8
    add_rect(s, "ORBIT_RING", 9.38, 1.98, 3.28, 3.28, fill=None, line=GOLD, line_w=0.9, line_opacity=58, shape=MSO_SHAPE.OVAL)

    add_masthead(s)
    add_footer(s, 18, "LỜI CẢM ƠN  ·  NHÓM 04")
    add_side_badge(s, "HẸN GẶP LẠI")

    add_text(s, "HEADING_KICKER_18", "BÁO CÁO THẢO LUẬN HOÀN THÀNH  ·  NHÓM 04", 0.84, 1.28, 6.5, 0.22, font=SANS_SEMI, size=8.8, color=GOLD, spacing=2.4, caps=True)
    add_text(s, "THANKS_1", "CẢM", 0.76, 1.53, 7.4, 1.85, font=DISPLAY, size=132, color=GOLD, spacing=-2.0, gradient=GOLD_STOPS, shadow=True)
    add_text(s, "THANKS_2", "ƠN", 0.76, 3.42, 7.4, 1.85, font=DISPLAY, size=132, color=GOLD, spacing=-2.0, gradient=GOLD_STOPS, shadow=True)
    add_text(s, "THANKS_SCRIPT", "thầy cô và các bạn đã chú ý lắng nghe", 0.86, 5.38, 6.8, 0.60, font=SCRIPT, size=29, color=GOLD_LIGHT)
    add_text(s, "THANKS_LEAD", "Rất mong nhận được những câu hỏi và ý kiến đóng góp quý báu.", 0.86, 5.90, 7.5, 0.62, font=DISPLAY_IT, size=14.5, color=CREAM, line_spacing=1.08)

    # Huy hiệu Q&A
    add_text(s, "BADGE_NUM", "Q&A", 9.38, 2.95, 3.28, 1.02, font=DISPLAY, size=52, color=GOLD, gradient=GOLD_STOPS, align=PP_ALIGN.CENTER, shadow=True)
    add_text(s, "BADGE_LABEL", "THẢO LUẬN MỞ RỘNG", 9.38, 4.10, 3.28, 0.22, font=SANS_SEMI, size=7.8, color=GOLD, spacing=2.0, caps=True, align=PP_ALIGN.CENTER)

    add_text(s, "MARQUEE", "TƯ DUY PHÊ PHÁN  ·  THẾ GIỚI QUAN KHOA HỌC  ·  PHƯƠNG PHÁP LUẬN BIỆN CHỨNG", 0.86, 6.68, 11.6, 0.18, font=SANS, size=6.8, color=GOLD, spacing=1.6, opacity=48)

    s.notes_slide.notes_text_frame.text = "Bài thuyết trình của Nhóm 04 đến đây là kết thúc. Chúng em xin chân thành cảm ơn thầy cô và các bạn. Nhóm rất mong nhận được câu hỏi thảo luận để cùng làm sâu sắc thêm bài học."
    return s


# ================================================================ MAIN
def main():
    prs = Presentation()
    prs.slide_width = Inches(W)
    prs.slide_height = Inches(H)
    prs.core_properties.title = "Triết học Mác – Lênin · 3 Quy luật & 5 Cặp phạm trù"
    prs.core_properties.subject = "Báo cáo thảo luận Nhóm 04"
    prs.core_properties.author = "Nhóm 04"

    builders = [
        build_slide_01, build_slide_02, build_slide_03, build_slide_04,
        build_slide_05, build_slide_06, build_slide_07, build_slide_08,
        build_slide_09, build_slide_10, build_slide_11, build_slide_12,
        build_slide_13, build_slide_14, build_slide_15, build_slide_16,
        build_slide_17, build_slide_18,
    ]

    for builder in builders:
        s = builder(prs)
        add_morph(s, 1500)

    prs.save(str(OUT))
    print(f"Đã lưu: {OUT} ({OUT.stat().st_size/1024:.0f} KB)")
    print(f"Tổng số slide đã tạo: {len(prs.slides)}")


if __name__ == "__main__":
    main()
