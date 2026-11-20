# -*- coding: utf-8 -*-
"""
TRIẾT HỌC MÁC – LÊNIN · bộ 3 slide LỜI CHÀO
Phong cách: đỏ sâu – vàng kim, chân dung Lenin cắt nền, chữ Việt phá cách.
- 16:9, mọi phần tử là layer riêng (không group), có tên trong Selection Pane.
- Morph 2,2 giây nhúng trực tiếp trong XML từng slide.
- Font: Playfair Editorial, Script Viet, Be Vietnam Pro.
"""

from __future__ import annotations

import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

from PIL import Image, ImageFont
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, MSO_AUTO_SIZE, PP_ALIGN
from pptx.oxml.ns import nsdecls, qn
from pptx.oxml import parse_xml
from pptx.util import Inches, Pt
from lxml import etree

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "assets"
FONTS = ROOT / "fonts"
OUT = ROOT / "Triet_hoc_Mac_Lenin_Loi_chao.pptx"

LENIN = ASSETS / "lenin_warm.png"
MEDALLION = ASSETS / "lenin_badge.png"
RAYS = ASSETS / "rays_gold.png"
GRAIN = ASSETS / "grain_red.png"

# ---------------------------------------------------------------- palette
INK = RGBColor(0x1B, 0x03, 0x05)
CREAM = RGBColor(0xF7, 0xEC, 0xD3)
GOLD_LIGHT = RGBColor(0xF4, 0xDF, 0xA3)
GOLD = RGBColor(0xD6, 0xAF, 0x64)
GOLD_DEEP = RGBColor(0xA5, 0x76, 0x2B)
RED = RGBColor(0x9E, 0x1B, 0x1F)
RED_DEEP = RGBColor(0x4A, 0x07, 0x0C)
MUTED = RGBColor(0xC9, 0xAD, 0x7C)

DISPLAY = "Playfair Editorial"
DISPLAY_IT = "Playfair Editorial Italic"
SCRIPT = "Script Viet"
SANS = "Be Vietnam Pro"
SANS_SEMI = "Be Vietnam Pro SemiBold"

FONT_FILES = {
    "display": FONTS / "PlayfairEditorial.ttf",
    "display_it": FONTS / "PlayfairEditorial-Italic.ttf",
    "script": FONTS / "ScriptViet-Bold.ttf",
    "sans": FONTS / "BeVietnamPro-Regular.ttf",
    "sans_semi": FONTS / "BeVietnamPro-SemiBold.ttf",
}

W, H = 13.333, 7.5
L, R, T, B = 0.68, 12.66, 0.52, 6.96

GOLD_STOPS = [
    (0.00, "FFF9E6"),
    (0.20, "F7E4AC"),
    (0.42, "E3C377"),
    (0.60, "C99A44"),
    (0.72, "EBD08C"),
    (0.86, "D4A94F"),
    (1.00, "A97424"),
]


# ---------------------------------------------------------------- xml helpers
def set_fill_alpha(shape, opacity_pct: float) -> None:
    solid = shape.fill._xPr.find(qn("a:solidFill"))
    srgb = solid.find(qn("a:srgbClr"))
    for old in srgb.findall(qn("a:alpha")):
        srgb.remove(old)
    alpha = etree.SubElement(srgb, qn("a:alpha"))
    alpha.set("val", str(int(opacity_pct * 1000)))


def set_line_alpha(shape, opacity_pct: float) -> None:
    ln = shape.line._get_or_add_ln()
    solid = ln.find(qn("a:solidFill"))
    srgb = solid.find(qn("a:srgbClr"))
    for old in srgb.findall(qn("a:alpha")):
        srgb.remove(old)
    alpha = etree.SubElement(srgb, qn("a:alpha"))
    alpha.set("val", str(int(opacity_pct * 1000)))


def gradient_shape(shape, stops, angle=90, radial=False) -> None:
    """Thay fill hiện tại bằng gradient nhiều stop (màu + alpha tuỳ chọn)."""
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


def add_gradient_rect(slide, name, x, y, w, h, stops, angle=115, radial=False,
                      line=None, line_w=0.6):
    shp = add_rect(slide, name, x, y, w, h, fill=INK, line=line, line_w=line_w)
    gradient_shape(shp, stops, angle=angle, radial=radial)
    return shp


def add_text(slide, name, text, x, y, w, h, font=SANS, size=12, bold=False,
             italic=False, color=CREAM, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP,
             spacing=None, line_spacing=None, caps=False, wrap=True,
             gradient=None, shadow=False, opacity=None):
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
    if opacity is not None:
        set_run_alpha(r, opacity)
    return tb


def set_run_alpha(run, opacity_pct: float) -> None:
    rpr = run.font._element
    solid = rpr.find(qn("a:solidFill"))
    if solid is None:
        return
    srgb = solid.find(qn("a:srgbClr"))
    if srgb is None:
        return
    for old in srgb.findall(qn("a:alpha")):
        srgb.remove(old)
    alpha = etree.SubElement(srgb, qn("a:alpha"))
    alpha.set("val", str(int(opacity_pct * 1000)))


def apply_text_gradient(run, stops) -> None:
    rpr = run.font._element
    solid = rpr.find(qn("a:solidFill"))
    gs_xml = []
    for pos, color in stops:
        gs_xml.append(
            f'<a:gs pos="{int(pos * 100000)}"><a:srgbClr val="{color}"/></a:gs>'
        )
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


def add_multirun(slide, name, runs, x, y, w, h, align=PP_ALIGN.LEFT,
                 anchor=MSO_ANCHOR.TOP, line_spacing=1.0, wrap=True):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tb.name = name
    tf = tb.text_frame
    tf.word_wrap = wrap
    tf.auto_size = MSO_AUTO_SIZE.NONE
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = anchor
    p = tf.paragraphs[0]
    p.alignment = align
    p.line_spacing = line_spacing
    for spec in runs:
        r = p.add_run()
        r.text = spec["text"]
        r.font.name = spec.get("font", SANS)
        r.font.size = Pt(spec.get("size", 12))
        r.font.bold = spec.get("bold", False)
        r.font.italic = spec.get("italic", False)
        r.font.color.rgb = spec.get("color", CREAM)
        if spec.get("spacing") is not None:
            r.font._element.set("spc", str(int(spec["spacing"] * 100)))
        if spec.get("gradient"):
            apply_text_gradient(r, spec["gradient"])
        if spec.get("shadow"):
            apply_text_shadow(r)
    return tb


def set_vertical(tb) -> None:
    body_pr = tb.text_frame._txBody.find(qn("a:bodyPr"))
    body_pr.set("vert", "vert270")


def add_picture(slide, path, name, x, y, w, h, descr):
    pic = slide.shapes.add_picture(str(path), Inches(x), Inches(y), Inches(w), Inches(h))
    pic.name = name
    pic._element.nvPicPr.cNvPr.set("descr", descr)
    return pic


def add_lenin(slide, path, name, x, bottom, height, descr):
    with Image.open(path) as im:
        ar = im.width / im.height
    width = height * ar
    return add_picture(slide, path, name, x, bottom - height, width, height, descr)


MORPH = """<mc:AlternateContent xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006">
  <mc:Choice xmlns:p159="http://schemas.microsoft.com/office/powerpoint/2015/09/main" Requires="p159">
    <p:transition xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" xmlns:p14="http://schemas.microsoft.com/office/powerpoint/2010/main" spd="slow" p14:dur="2200">
      <p159:morph option="byObject"/>
    </p:transition>
  </mc:Choice>
  <mc:Fallback>
    <p:transition xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" spd="slow">
      <p:fade/>
    </p:transition>
  </mc:Fallback>
</mc:AlternateContent>"""


def add_morph(slide, duration=2200) -> None:
    sld = slide._element
    ns_mc = "{http://schemas.openxmlformats.org/markup-compatibility/2006}AlternateContent"
    for old in sld.findall(ns_mc):
        sld.remove(old)
    xml = MORPH.replace('p14:dur="2200"', f'p14:dur="{duration}"')
    el = etree.fromstring(xml.encode("utf-8"))
    clr = sld.find(qn("p:clrMapOvr"))
    if clr is not None:
        clr.addnext(el)
    else:
        sld.append(el)


# ---------------------------------------------------------------- typography
def measure(text, key, pt):
    path = FONT_FILES[key]
    if not path.exists():
        path = Path("C:/Windows/Fonts/georgiab.ttf")
    f = ImageFont.truetype(str(path), max(8, int(round(pt * 96 / 72))))
    box = f.getbbox(text)
    return (box[2] - box[0]) / 96.0


def fit(text, key, max_width, start, minimum=40, spacing=0.0):
    size = start
    while size > minimum:
        extra = spacing * max(0, len(text) - 1) / 72.0
        if measure(text, key, size) + extra <= max_width:
            break
        size -= 1
    return size


# ---------------------------------------------------------------- shared layers
def add_background(slide):
    add_gradient_rect(
        slide, "BG_DEEP", 0, 0, W, H,
        [(0.00, "8E191D", None), (0.42, "650E13", None), (1.00, "2C0408", None)],
        angle=118,
    )
    add_picture(slide, RAYS, "RAY_BURST", 0, 0, W, H,
                "Chùm tia vàng rất nhẹ, tạo chiều sâu cho nền đỏ.")
    add_picture(slide, GRAIN, "TEXTURE_GRAIN", 0, 0, W, H,
                "Lớp grain đỏ rất nhẹ — có thể ẩn hoặc xoá.")
    add_rect(slide, "FRAME_TOP", L, T, R - L, 0.007, fill=GOLD, opacity=26)
    add_rect(slide, "FRAME_BOTTOM", L, B, R - L, 0.007, fill=GOLD, opacity=26)
    add_rect(slide, "FRAME_LEFT", L, T, 0.007, B - T, fill=GOLD, opacity=26)
    add_rect(slide, "FRAME_RIGHT", R, T, 0.007, B - T, fill=GOLD, opacity=26)


def add_masthead(slide):
    add_rect(slide, "KICKER_MARK", L + 0.01, 0.735, 0.095, 0.095, fill=GOLD)
    add_text(slide, "KICKER_TEXT", "HỌC PHẦN TRIẾT HỌC MÁC – LÊNIN",
             L + 0.22, 0.70, 7.4, 0.24, font=SANS_SEMI, size=9.2, color=GOLD,
             spacing=2.5, caps=True)
    add_rect(slide, "KICKER_RULE", L + 0.01, 0.94, 5.25, 0.006, fill=GOLD, opacity=22)


def add_footer(slide, page, right_text):
    add_text(slide, "FOOTER_LEFT", "NHÓM 04  ·  LỚP ................................",
             L, 7.04, 5.2, 0.18, font=SANS, size=7.4, color=MUTED, spacing=1.2)
    add_text(slide, "FOOTER_RIGHT", right_text, 8.55, 7.04, 3.30, 0.18,
             font=SANS, size=7.4, color=MUTED, spacing=1.2, align=PP_ALIGN.RIGHT)
    add_text(slide, "PAGE_NO", page, 12.00, 7.04, 0.66, 0.18,
             font=SANS_SEMI, size=7.4, color=GOLD, spacing=1.0, align=PP_ALIGN.RIGHT)
    add_text(slide, "CREDIT_IMAGE",
             "Chân dung: V. I. Lenin, 1920 · Wikimedia Commons · Public Domain",
             L, 7.23, 7.2, 0.16, font=SANS, size=6.2, color=MUTED, opacity=55)


def add_side(slide, text):
    tb = add_text(slide, "SIDE_TEXT", text, 0.33, 1.45, 0.22, 4.45,
                  font=SANS_SEMI, size=6.8, color=GOLD, spacing=1.8,
                  caps=True, wrap=False, anchor=MSO_ANCHOR.MIDDLE, opacity=55)
    set_vertical(tb)


def add_orbit_star(slide, star_x, star_y, star_w, ring_x, ring_y, ring_w,
                   star_opacity=18, ring_opacity=42, star_rot=12):
    add_rect(slide, "STAR_BACK", star_x, star_y, star_w, star_w, fill=None,
             line=GOLD, line_w=0.8, line_opacity=star_opacity,
             shape=MSO_SHAPE.STAR_5_POINT)
    slide.shapes[-1].rotation = star_rot
    add_rect(slide, "ORBIT_RING", ring_x, ring_y, ring_w, ring_w, fill=None,
             line=GOLD, line_w=0.9, line_opacity=ring_opacity, shape=MSO_SHAPE.OVAL)


# ---------------------------------------------------------------- slides
def slide_one(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    add_background(s)

    # quầng sáng sau chân dung
    add_gradient_rect(s, "GLOW_PORTRAIT", 7.55, -0.15, 6.1, 6.1,
                      [(0.0, "C23A32", 34), (0.55, "8E1A1E", 14), (1.0, "8E1A1E", 0)],
                      radial=True)
    add_orbit_star(s, 7.55, -0.72, 6.75, 7.95, 0.58, 5.25,
                   star_opacity=17, ring_opacity=38, star_rot=12)

    # chân dung Lenin (lớp ảnh nằm dưới chữ)
    add_lenin(s, LENIN, "LENIN_HERO", 8.28, 7.62, 7.28,
              "V. I. Lenin, chân dung 1920, đã tách nền và xử lý đỏ – vàng.")

    add_masthead(s)
    add_footer(s, "01 / 03", "LỜI CHÀO  ·  NHÓM 04")
    add_side(s, "LỜI CHÀO · 2026")

    # lời chào viết tay
    add_text(s, "SALUTATION", "Kính chào thầy cô và các bạn",
             0.84, 1.24, 6.7, 0.62, font=SCRIPT, size=32, color=GOLD_LIGHT,
             spacing=0.2)

    # tiêu đề chính
    size = min(fit("TRIẾT HỌC", "display", 6.55, 80, 56, spacing=-1.5),
               fit("MÁC – LÊNIN", "display", 7.55, 80, 56, spacing=-1.5))
    print(f"Cỡ tiêu đề chọn: {size}pt")
    add_text(s, "TITLE_LINE_1", "TRIẾT HỌC", 0.80, 2.08, 7.2, 1.10,
             font=DISPLAY, size=size, color=CREAM, spacing=-1.5, shadow=True)
    add_text(s, "TITLE_LINE_2", "MÁC – LÊNIN", 0.80, 3.16, 7.7, 1.18,
             font=DISPLAY, size=size, color=GOLD, spacing=-1.5,
             gradient=GOLD_STOPS, shadow=True)

    add_rect(s, "TITLE_RULE", 0.84, 4.46, 2.35, 0.018, fill=GOLD, opacity=85)
    add_text(s, "SUBTITLE_LABEL", "LỜI CHÀO  ·  GIỚI THIỆU NHÓM",
             0.84, 4.64, 4.8, 0.22, font=SANS_SEMI, size=8.6, color=GOLD,
             spacing=2.4, caps=True)
    add_text(s, "MANIFESTO",
             "Tư duy phê phán bắt đầu từ việc dám đặt lại câu hỏi.",
             0.82, 4.98, 6.75, 0.56, font=DISPLAY_IT, size=18.5, color=CREAM,
             line_spacing=1.06)
    add_text(s, "CHAPTER_LABEL", "CHƯƠNG 1  ·  CHỦ NGHĨA DUY VẬT BIỆN CHỨNG",
             0.84, 6.34, 6.6, 0.22, font=SANS_SEMI, size=8.4, color=GOLD,
             spacing=1.9, caps=True)

    s.notes_slide.notes_text_frame.text = (
        "Kính chào thầy cô và các bạn. Chúng em là Nhóm 04. "
        "Hôm nay nhóm xin gửi lời chào và giới thiệu đội ngũ trước khi bước vào Chương 1. "
        "Chúng em chọn một cách mở đầu ngắn: nói về cách nhóm làm việc, cách nhóm đặt câu hỏi, "
        "rồi mời cả lớp cùng bước vào phần nội dung. "
        "Thầy cô và các bạn có thể thay tên nhóm, lớp và tên thành viên ở các layer tương ứng."
    )
    return s


def slide_two(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    add_background(s)

    add_gradient_rect(s, "GLOW_PORTRAIT", 8.75, 0.25, 4.9, 4.9,
                      [(0.0, "C23A32", 28), (0.6, "8E1A1E", 10), (1.0, "8E1A1E", 0)],
                      radial=True)
    add_orbit_star(s, 9.08, 1.02, 4.25, 9.52, 1.32, 3.42,
                   star_opacity=24, ring_opacity=48, star_rot=18)

    add_picture(s, MEDALLION, "PORTRAIT_LENIN", 9.70, 1.50, 3.06, 3.06,
                "Chân dung Lenin trong huy hiệu tròn, xử lý vàng – đỏ.")

    add_masthead(s)
    add_footer(s, "02 / 03", "ĐỘI NGŨ  ·  5 THÀNH VIÊN")
    add_side(s, "TƯ DUY PHÊ PHÁN")

    add_text(s, "HEADING_KICKER", "ĐỘI NGŨ THỰC HIỆN  ·  NHÓM 04",
             0.84, 1.28, 6.5, 0.22, font=SANS_SEMI, size=8.8, color=GOLD,
             spacing=2.4, caps=True)
    add_text(s, "TITLE_CHUNG", "CHÚNG", 0.80, 1.55, 7.4, 1.32,
             font=DISPLAY, size=92, color=CREAM, spacing=-1.2, shadow=True)
    add_text(s, "TITLE_TOI", "TÔI", 0.80, 2.53, 7.4, 1.42,
             font=DISPLAY, size=112, color=GOLD, spacing=-1.2,
             gradient=GOLD_STOPS, shadow=True)
    add_text(s, "SUBHEAD_SCRIPT", "năm người, một cách nhìn",
             3.98, 3.64, 4.35, 0.58, font=SCRIPT, size=26, color=GOLD_LIGHT)
    add_rect(s, "COLUMN_RULE", 8.62, 1.28, 0.006, 5.30, fill=GOLD, opacity=18)

    rows = [
        ("01", "DẪN DẮT", "Kết nối nội dung, giữ nhịp tranh luận."),
        ("02", "NGHIÊN CỨU", "Đọc giáo trình, kiểm chứng luận điểm."),
        ("03", "BIÊN TẬP", "Chuẩn hoá ngôn ngữ, biên tập bản thảo."),
        ("04", "THIẾT KẾ", "Dựng hình ảnh, chữ và nhịp trình bày."),
        ("05", "THUYẾT TRÌNH", "Kể câu chuyện, dẫn dắt phần hỏi đáp."),
    ]
    y = 4.46
    for i, (num, role, desc) in enumerate(rows, start=1):
        add_rect(s, f"MEMBER_{i:02d}_RULE", 0.84, y - 0.04, 7.72, 0.006,
                 fill=GOLD, opacity=18)
        add_text(s, f"MEMBER_{i:02d}_NUM", num, 0.84, y + 0.035, 0.55, 0.30,
                 font=DISPLAY, size=16, color=GOLD, spacing=0.2)
        add_text(s, f"MEMBER_{i:02d}_ROLE", role, 1.50, y + 0.075, 2.05, 0.24,
                 font=SANS_SEMI, size=10.2, color=CREAM, spacing=1.0, caps=True)
        add_text(s, f"MEMBER_{i:02d}_DESC", desc, 3.62, y + 0.075, 3.30, 0.24,
                 font=SANS, size=9.0, color=MUTED)
        add_text(s, f"MEMBER_{i:02d}_NAME", "Tên thành viên", 7.04, y + 0.075, 1.46, 0.22,
                 font=SANS, size=8.0, color=GOLD, opacity=58, align=PP_ALIGN.RIGHT)
        y += 0.44
    add_rect(s, "MEMBER_END_RULE", 0.84, y - 0.03, 7.72, 0.008, fill=GOLD, opacity=30)

    add_text(s, "PORTRAIT_CAPTION", "V. I. LENIN  ·  1870 – 1924",
             9.55, 4.70, 3.36, 0.20, font=SANS_SEMI, size=7.4, color=GOLD,
             spacing=1.6, caps=True, align=PP_ALIGN.CENTER)
    add_text(s, "PORTRAIT_QUOTE",
             "“Không có lý luận cách mạng thì không có phong trào cách mạng.”",
             9.55, 5.02, 3.36, 0.72, font=DISPLAY_IT, size=11.4, color=CREAM,
             line_spacing=1.08, align=PP_ALIGN.CENTER)
    add_text(s, "PORTRAIT_SOURCE", "V. I. LÊNIN  ·  1902",
             9.55, 5.78, 3.36, 0.18, font=SANS_SEMI, size=6.8, color=MUTED,
             spacing=1.5, caps=True, align=PP_ALIGN.CENTER)

    s.notes_slide.notes_text_frame.text = (
        "Nhóm gồm năm thành viên, mỗi bạn phụ trách một vai trò: dẫn dắt, nghiên cứu, biên tập, "
        "thiết kế và thuyết trình. Cách chia việc này giúp nhóm vừa giữ được mạch lý luận, "
        "vừa kiểm tra chéo được nội dung. Thầy cô và các bạn có thể điền tên thành viên "
        "vào các layer MEMBER_01_NAME … MEMBER_05_NAME."
    )
    return s


def slide_three(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    add_background(s)

    add_orbit_star(s, 7.55, 0.55, 7.05, 9.38, 1.98, 3.28,
                   star_opacity=13, ring_opacity=58, star_rot=8)

    add_masthead(s)
    add_footer(s, "03 / 03", "LỜI CẢM ƠN  ·  NHÓM 04")
    add_side(s, "HẸN GẶP LẠI")

    add_text(s, "HEADING_KICKER_3", "LỜI CẢM ƠN  ·  NHÓM 04",
             0.84, 1.28, 5.5, 0.22, font=SANS_SEMI, size=8.8, color=GOLD,
             spacing=2.4, caps=True)
    add_text(s, "THANKS_1", "CẢM", 0.76, 1.53, 7.4, 1.85,
             font=DISPLAY, size=132, color=GOLD, spacing=-2.0,
             gradient=GOLD_STOPS, shadow=True)
    add_text(s, "THANKS_2", "ƠN", 0.76, 3.42, 7.4, 1.85,
             font=DISPLAY, size=132, color=GOLD, spacing=-2.0,
             gradient=GOLD_STOPS, shadow=True)
    add_text(s, "THANKS_SCRIPT", "và hẹn gặp lại ở Chương 1",
             0.86, 5.38, 5.8, 0.60, font=SCRIPT, size=29, color=GOLD_LIGHT)
    add_text(s, "THANKS_LEAD",
             "Mời thầy cô và các bạn bước vào hành trình tư duy phê phán.",
             0.86, 5.90, 6.25, 0.62, font=DISPLAY_IT, size=14.2, color=CREAM,
             line_spacing=1.08)
    add_text(s, "CHAPTER_LABEL_3", "CHƯƠNG 1  ·  CHỦ NGHĨA DUY VẬT BIỆN CHỨNG",
             0.86, 6.32, 6.6, 0.22, font=SANS_SEMI, size=8.2, color=GOLD,
             spacing=1.9, caps=True)

    # huy hiệu chương 1
    add_text(s, "BADGE_NUM", "01", 9.38, 3.02, 3.28, 1.02,
             font=DISPLAY, size=64, color=GOLD, gradient=GOLD_STOPS,
             align=PP_ALIGN.CENTER, shadow=True)
    add_text(s, "BADGE_LABEL", "CHƯƠNG", 9.38, 4.10, 3.28, 0.22,
             font=SANS_SEMI, size=7.8, color=GOLD, spacing=2.6, caps=True,
             align=PP_ALIGN.CENTER)

    add_text(s, "MARQUEE",
             "TƯ DUY PHÊ PHÁN  ·  THẾ GIỚI QUAN KHOA HỌC  ·  PHƯƠNG PHÁP LUẬN BIỆN CHỨNG  ·  "
             "TƯ DUY PHÊ PHÁN  ·  THẾ GIỚI QUAN KHOA HỌC  ·  PHƯƠNG PHÁP LUẬN BIỆN CHỨNG",
             0.86, 6.68, 11.6, 0.18, font=SANS, size=6.6, color=GOLD,
             spacing=1.6, opacity=48, wrap=False)

    s.notes_slide.notes_text_frame.text = (
        "Cảm ơn thầy cô và các bạn đã lắng nghe phần giới thiệu. "
        "Nhóm xin mời cả lớp bước vào Chương 1: Chủ nghĩa duy vật biện chứng. "
        "Phần tiếp theo sẽ bắt đầu từ câu hỏi trung tâm: vật chất và ý thức quan hệ với nhau như thế nào?"
    )
    return s


# ---------------------------------------------------------------- main
def main():
    for path in (LENIN, MEDALLION, RAYS, GRAIN):
        if not path.exists():
            raise SystemExit(f"Thiếu asset: {path}. Chạy tools/prepare_lenin.py trước.")
    for key, path in FONT_FILES.items():
        if not path.exists():
            print(f"CẢNH BÁO: thiếu font {path.name}; PowerPoint sẽ fallback.")

    prs = Presentation()
    prs.slide_width = Inches(W)
    prs.slide_height = Inches(H)
    prs.core_properties.title = "Triết học Mác – Lênin · Lời chào & giới thiệu nhóm"
    prs.core_properties.subject = "Bộ 3 slide mở đầu, phong cách đỏ – vàng, hiệu ứng Morph"
    prs.core_properties.author = "Nhóm 04"
    prs.core_properties.comments = (
        "Mỗi phần tử là một layer riêng, không group. Giữ nguyên tên shape để Morph ghép cặp. "
        "Font dùng: Playfair Editorial, Script Viet, Be Vietnam Pro."
    )

    slides = [slide_one(prs), slide_two(prs), slide_three(prs)]
    for s in slides:
        add_morph(s, 2200)

    prs.save(str(OUT))
    print(f"Đã lưu: {OUT} ({OUT.stat().st_size/1024:.0f} KB)")
    print(f"Số slide: {len(prs.slides)}")


if __name__ == "__main__":
    main()
