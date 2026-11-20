# -*- coding: utf-8 -*-
"""Agent 5: Layout & UI/UX Designer (Nhà thiết kế Bố cục & Lắp ráp Kỹ thuật)
Nhiệm vụ: Nhận toàn bộ nguyên liệu từ Strategist, Data và Visual Creator,
tính toán tọa độ chuẩn xác trên hệ lưới 16:9, xuất mã render và dựng file PPTX hoàn chỉnh.
"""

from pathlib import Path
import json
from typing import List
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import nsdecls, qn
from pptx.oxml import parse_xml
from lxml import etree

from studio.schemas import DesignTokens, SlideSpec, VisualSlot, ContentItem


class LayoutDesigner:
    def __init__(self, output_path: Path):
        self.output_path = output_path

    @staticmethod
    def _add_morph(slide, duration_ms: int = 1000):
        sldPr = slide._element.get_or_add_element(qn("p:sldPr"))
        for child in list(sldPr):
            if child.tag.endswith("transition"):
                sldPr.remove(child)
        trans_xml = f"""
        <p:transition xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"
                      xmlns:p14="http://schemas.microsoft.com/office/powerpoint/2010/main"
                      spd="med" p14:dur="{duration_ms}">
            <p14:morph option="byObject"/>
        </p:transition>
        """
        sldPr.append(parse_xml(trans_xml))

    @staticmethod
    def _hex_to_rgb(hex_str: str) -> RGBColor:
        h = hex_str.lstrip("#")
        return RGBColor(*(int(h[i:i+2], 16) for i in (0, 2, 4)))

    @staticmethod
    def _gradient_shape(shape, stops, angle=90, radial=False):
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
            if lin is not None:
                lin.set("ang", str(int(angle * 60000)))

    @staticmethod
    def _set_opacity(shape, opacity_percent: float):
        spPr = shape._element.spPr
        solidFill = spPr.find(qn("a:solidFill"))
        if solidFill is not None:
            clr = solidFill.find(qn("a:srgbClr"))
            if clr is not None:
                a = etree.SubElement(clr, qn("a:alpha"))
                a.set("val", str(int(opacity_percent * 1000)))

    def render_presentation(self, slides_spec: List[SlideSpec], tokens: DesignTokens) -> Path:
        prs = Presentation()
        prs.slide_width = Inches(tokens.slide_width)
        prs.slide_height = Inches(tokens.slide_height)

        GOLD = self._hex_to_rgb(tokens.accent_gold)
        CREAM = self._hex_to_rgb(tokens.text_cream)
        MUTED = self._hex_to_rgb(tokens.text_muted)
        CARD_BG = self._hex_to_rgb(tokens.card_bg)

        GOLD_STOPS = [
            (0.00, "FFFFFF", None),
            (0.18, "F5E7B2", None),
            (0.52, "E8C872", None),
            (0.82, "C39838", None),
            (1.00, "8A6318", None),
        ]

        for spec in slides_spec:
            s = prs.slides.add_slide(prs.slide_layouts[6])

            # 1. Vẽ các Visual Slots
            for vs in spec.visual_slots:
                if vs.role in ("background", "character_hero", "character_watermark", "poster_bottom_left", "emblem", "emblem_top_left", "offscreen_bottom", "offscreen_top", "offscreen_left", "offscreen_right"):
                    if vs.asset_path and Path(vs.asset_path).exists():
                        pic = s.shapes.add_picture(vs.asset_path, Inches(vs.x), Inches(vs.y), Inches(vs.w), Inches(vs.h))
                        pic._element.nvPicPr.cNvPr.set("name", vs.shape_morph_id)
                elif vs.role == "glow":
                    rect = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(vs.x), Inches(vs.y), Inches(vs.w), Inches(vs.h))
                    rect.name = vs.shape_morph_id
                    rect.line.fill.background()
                    self._gradient_shape(rect, [(0.0, "C23A32", 32), (0.55, "8E1A1E", 12), (1.0, "8E1A1E", 0)], radial=True)
                elif vs.role == "vector_star":
                    star = s.shapes.add_shape(MSO_SHAPE.STAR_5_POINT, Inches(vs.x), Inches(vs.y), Inches(vs.w), Inches(vs.h))
                    star.name = vs.shape_morph_id
                    star.fill.background()
                    star.line.color.rgb = GOLD
                    star.line.width = Pt(0.8)
                    star.rotation = 12
                    self._set_opacity(star, 18.0)
                elif vs.role == "vector_ring":
                    ring = s.shapes.add_shape(MSO_SHAPE.OVAL, Inches(vs.x), Inches(vs.y), Inches(vs.w), Inches(vs.h))
                    ring.name = vs.shape_morph_id
                    ring.fill.background()
                    ring.line.color.rgb = GOLD
                    ring.line.width = Pt(0.9)
                    self._set_opacity(ring, 42.0)
                elif vs.role == "card_container":
                    card = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(vs.x), Inches(vs.y), Inches(vs.w), Inches(vs.h))
                    card.name = vs.shape_morph_id
                    card.fill.solid()
                    card.fill.fore_color.rgb = CARD_BG
                    card.line.color.rgb = GOLD
                    card.line.width = Pt(0.8)
                    self._set_opacity(card, 88.0)

            # 2. Render Text Content theo Slide Type
            if spec.slide_id == 1:
                # Tiêu đề & nội dung Slide 1
                tb_sal = s.shapes.add_textbox(Inches(0.95), Inches(1.48), Inches(5.8), Inches(0.52))
                tb_sal.name = "!!COVER_SALUTATION"
                p = tb_sal.text_frame.paragraphs[0]
                r = p.add_run()
                r.text = "Kính chào thầy cô và các bạn"
                r.font.name = tokens.font_script
                r.font.size = Pt(29)
                r.font.color.rgb = GOLD

                tb_t1 = s.shapes.add_textbox(Inches(0.95), Inches(2.05), Inches(5.8), Inches(1.05))
                tb_t1.name = "!!COVER_TITLE_1"
                p = tb_t1.text_frame.paragraphs[0]
                r = p.add_run()
                r.text = "Triết học"
                r.font.name = tokens.font_display
                r.font.size = Pt(74)
                r.font.color.rgb = CREAM

                tb_t2 = s.shapes.add_textbox(Inches(0.95), Inches(3.10), Inches(5.8), Inches(1.10))
                tb_t2.name = "!!COVER_TITLE_2"
                p = tb_t2.text_frame.paragraphs[0]
                r = p.add_run()
                r.text = "Mác – Lênin"
                r.font.name = tokens.font_display
                r.font.size = Pt(74)
                r.font.color.rgb = GOLD

                # Phụ đề & Manifesto
                tb_sub = s.shapes.add_textbox(Inches(0.95), Inches(4.46), Inches(5.6), Inches(0.22))
                tb_sub.name = "!!COVER_SUB"
                p = tb_sub.text_frame.paragraphs[0]
                r = p.add_run()
                r.text = spec.subheadline
                r.font.name = tokens.font_sans
                r.font.bold = True
                r.font.size = Pt(8.4)
                r.font.color.rgb = GOLD

                tb_man = s.shapes.add_textbox(Inches(0.95), Inches(4.78), Inches(5.75), Inches(0.58))
                tb_man.name = "!!COVER_MANIFESTO"
                p = tb_man.text_frame.paragraphs[0]
                r = p.add_run()
                r.text = spec.quote
                r.font.name = "Playfair Editorial Italic"
                r.font.italic = True
                r.font.size = Pt(15.5)
                r.font.color.rgb = CREAM

                # Presenter pill
                pill = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.95), Inches(5.85), Inches(3.55), Inches(0.44))
                pill.name = "!!PRESENTER_BOX"
                pill.fill.solid()
                pill.fill.fore_color.rgb = CARD_BG
                pill.line.color.rgb = GOLD
                pill.line.width = Pt(0.6)
                self._set_opacity(pill, 90.0)

                tb_p = s.shapes.add_textbox(Inches(1.38), Inches(5.94), Inches(3.0), Inches(0.26))
                tb_p.name = "!!PRESENTER_TXT"
                p = tb_p.text_frame.paragraphs[0]
                r = p.add_run()
                r.text = "Trình bày: Nhóm 13 thành viên"
                r.font.name = tokens.font_sans
                r.font.size = Pt(8.5)
                r.font.color.rgb = GOLD

                # Off-screen items Slide 2
                tb_off_h = s.shapes.add_textbox(Inches(15.0), Inches(0.60), Inches(7.90), Inches(0.95))
                tb_off_h.name = "!!TEAM_HEADER"

            elif spec.slide_id == 2:
                # Slide 1 elements exit left
                tb_ex_t1 = s.shapes.add_textbox(Inches(-10.0), Inches(2.05), Inches(5.8), Inches(1.05))
                tb_ex_t1.name = "!!COVER_TITLE_1"
                tb_ex_t2 = s.shapes.add_textbox(Inches(-10.0), Inches(3.10), Inches(5.8), Inches(1.10))
                tb_ex_t2.name = "!!COVER_TITLE_2"
                tb_ex_sal = s.shapes.add_textbox(Inches(-9.0), Inches(1.48), Inches(5.8), Inches(0.52))
                tb_ex_sal.name = "!!COVER_SALUTATION"
                tb_ex_sub = s.shapes.add_textbox(Inches(-8.0), Inches(4.46), Inches(5.6), Inches(0.22))
                tb_ex_sub.name = "!!COVER_SUB"
                tb_ex_man = s.shapes.add_textbox(Inches(-10.0), Inches(4.78), Inches(5.75), Inches(0.58))
                tb_ex_man.name = "!!COVER_MANIFESTO"

                # Header Slide 2
                tb_h = s.shapes.add_textbox(Inches(4.80), Inches(0.60), Inches(7.90), Inches(0.95))
                tb_h.name = "!!TEAM_HEADER"
                tf_h = tb_h.text_frame
                tf_h.word_wrap = True
                p_k = tf_h.paragraphs[0]
                r_k = p_k.add_run()
                r_k.text = f"{spec.kicker}\n"
                r_k.font.name = tokens.font_sans
                r_k.font.bold = True
                r_k.font.size = Pt(8.5)
                r_k.font.color.rgb = GOLD
                r_k.font._element.set("spc", "180")

                p_t = tf_h.add_paragraph()
                r_t = p_t.add_run()
                r_t.text = spec.headline
                r_t.font.name = tokens.font_display
                r_t.font.bold = True
                r_t.font.size = Pt(26.0)
                r_t.font.color.rgb = GOLD

                # 4 Cards Layout
                coords = [
                    (4.80, 1.70, 3.90, 2.50),  # Card 1
                    (8.85, 1.70, 3.90, 2.50),  # Card 2
                    (4.80, 4.35, 3.90, 2.65),  # Card 3
                    (8.85, 4.35, 3.90, 2.65),  # Card 4
                ]
                for idx, item in enumerate(spec.items):
                    x, y, w, h = coords[idx]
                    # Card box
                    box = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
                    box.name = f"!!CARD_PANEL_{idx+1}"
                    box.fill.solid()
                    box.fill.fore_color.rgb = CARD_BG
                    box.line.color.rgb = GOLD
                    box.line.width = Pt(0.6)
                    self._set_opacity(box, 82.0)

                    # Wax badge
                    if item.badge_label and Path(item.badge_label).exists():
                        badge_pic = s.shapes.add_picture(item.badge_label, Inches(x + 0.15), Inches(y + 0.14), Inches(0.38), Inches(0.35))
                        badge_pic._element.nvPicPr.cNvPr.set("name", f"!!SEAL_BADGE_{idx+1}")

                    # Text content
                    tb = s.shapes.add_textbox(Inches(x + 0.58), Inches(y + 0.10), Inches(w - 0.70), Inches(h - 0.20))
                    tb.name = f"!!CARD_CONTENT_{idx+1}"
                    tf = tb.text_frame
                    tf.word_wrap = True
                    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

                    p0 = tf.paragraphs[0]
                    p0.space_after = Pt(4)
                    r_title = p0.add_run()
                    r_title.text = item.title
                    r_title.font.name = tokens.font_sans
                    r_title.font.bold = True
                    r_title.font.size = Pt(8.8)
                    r_title.font.color.rgb = GOLD
                    r_title.font._element.set("spc", "110")

                    members_data = json.loads(item.body)
                    is_compact = len(members_data) >= 4
                    for name, role, desc in members_data:
                        p_m = tf.add_paragraph()
                        p_m.space_after = Pt(2.0 if is_compact else 3.5)

                        r_n = p_m.add_run()
                        r_n.text = f"{name} "
                        r_n.font.name = tokens.font_display
                        r_n.font.bold = True
                        r_n.font.size = Pt(9.2 if is_compact else 9.8)
                        r_n.font.color.rgb = CREAM

                        r_r = p_m.add_run()
                        r_r.text = f"· {role}\n"
                        r_r.font.name = tokens.font_sans
                        r_r.font.size = Pt(7.2 if is_compact else 7.8)
                        r_r.font.color.rgb = GOLD

                        r_d = p_m.add_run()
                        r_d.text = f"“{desc}”"
                        r_d.font.name = "Playfair Editorial Italic"
                        r_d.font.italic = True
                        r_d.font.size = Pt(7.2 if is_compact else 7.8)
                        r_d.font.color.rgb = MUTED

            elif spec.slide_id == 3:
                # Slide 2 elements exit
                tb_ex_h = s.shapes.add_textbox(Inches(-8.0), Inches(0.60), Inches(7.90), Inches(0.95))
                tb_ex_h.name = "!!TEAM_HEADER"
                for idx in range(1, 5):
                    box_ex = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(-8.0), Inches(2.0), Inches(3.88), Inches(2.38))
                    box_ex.name = f"!!CARD_PANEL_{idx}"

                # CẢM ƠN
                tb_c = s.shapes.add_textbox(Inches(0.76), Inches(1.53), Inches(7.4), Inches(1.85))
                tb_c.name = "!!THANKS_1"
                p = tb_c.text_frame.paragraphs[0]
                r = p.add_run()
                r.text = "CẢM"
                r.font.name = tokens.font_display
                r.font.bold = True
                r.font.size = Pt(132)
                r.font.color.rgb = GOLD

                tb_o = s.shapes.add_textbox(Inches(0.76), Inches(3.35), Inches(7.4), Inches(1.85))
                tb_o.name = "!!THANKS_2"
                p = tb_o.text_frame.paragraphs[0]
                r = p.add_run()
                r.text = "ƠN"
                r.font.name = tokens.font_display
                r.font.bold = True
                r.font.size = Pt(132)
                r.font.color.rgb = GOLD

                tb_sc = s.shapes.add_textbox(Inches(0.86), Inches(5.35), Inches(5.8), Inches(0.60))
                tb_sc.name = "!!THANKS_SCRIPT"
                p = tb_sc.text_frame.paragraphs[0]
                r = p.add_run()
                r.text = spec.subheadline
                r.font.name = tokens.font_script
                r.font.size = Pt(29)
                r.font.color.rgb = GOLD

                tb_lead = s.shapes.add_textbox(Inches(0.86), Inches(5.88), Inches(6.25), Inches(0.62))
                tb_lead.name = "!!THANKS_LEAD"
                p = tb_lead.text_frame.paragraphs[0]
                r = p.add_run()
                r.text = spec.quote
                r.font.name = "Playfair Editorial Italic"
                r.font.italic = True
                r.font.size = Pt(14.2)
                r.font.color.rgb = CREAM

                # Chapter 01 badge text
                tb_bnum = s.shapes.add_textbox(Inches(9.38), Inches(2.50), Inches(3.28), Inches(1.30))
                tb_bnum.name = "!!BADGE_NUM"
                p = tb_bnum.text_frame.paragraphs[0]
                p.alignment = PP_ALIGN.CENTER
                r = p.add_run()
                r.text = "01"
                r.font.name = tokens.font_display
                r.font.bold = True
                r.font.size = Pt(78)
                r.font.color.rgb = GOLD

                tb_blabel = s.shapes.add_textbox(Inches(9.38), Inches(3.90), Inches(3.28), Inches(0.26))
                tb_blabel.name = "!!BADGE_LABEL"
                p = tb_blabel.text_frame.paragraphs[0]
                p.alignment = PP_ALIGN.CENTER
                r = p.add_run()
                r.text = "CHƯƠNG"
                r.font.name = tokens.font_sans
                r.font.bold = True
                r.font.size = Pt(11.0)
                r.font.color.rgb = GOLD

                tb_bsub = s.shapes.add_textbox(Inches(9.38), Inches(4.22), Inches(3.28), Inches(0.24))
                tb_bsub.name = "!!BADGE_SUB"
                p = tb_bsub.text_frame.paragraphs[0]
                p.alignment = PP_ALIGN.CENTER
                r = p.add_run()
                r.text = "DUY VẬT BIỆN CHỨNG"
                r.font.name = tokens.font_sans
                r.font.size = Pt(7.2)
                r.font.color.rgb = GOLD

            # Gán Speaker Notes
            if spec.speaker_notes:
                s.notes_slide.notes_text_frame.text = spec.speaker_notes

            # Kích hoạt Kinetic Morphing transition
            self._add_morph(s, tokens.morph_duration_ms)

        prs.save(str(self.output_path))
        return self.output_path
