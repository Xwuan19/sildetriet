# -*- coding: utf-8 -*-
import sys
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

# Test script for Slide 2 card formatting
prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.500)
slide = prs.slides.add_slide(prs.slide_layouts[6])

DISPLAY = "Playfair Editorial"
DISPLAY_IT = "Playfair Editorial"
SANS_SEMI = "Be Vietnam Pro SemiBold"
SANS = "Be Vietnam Pro"

GOLD = RGBColor(0xE8, 0xC8, 0x72)
GOLD_LIGHT = RGBColor(0xF3, 0xE2, 0xB8)
CREAM = RGBColor(0xFB, 0xF6, 0xEE)
MUTED = RGBColor(0xD6, 0xC4, 0xB8)
CARD_BG = RGBColor(0x32, 0x0C, 0x10)

def style_card(tb, header_num, header_text, items):
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.14)
    tf.margin_right = Inches(0.14)
    tf.margin_top = Inches(0.10)
    tf.margin_bottom = Inches(0.08)
    
    # Header
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
        p_name = tf.add_paragraph()
        p_name.space_after = Pt(1 if is_compact else 2)
        
        # Name in Playfair Editorial bold
        r_n = p_name.add_run()
        r_n.text = f"{name}  "
        r_n.font.name = DISPLAY
        r_n.font.bold = True
        r_n.font.size = Pt(9.6 if is_compact else 10.2)
        r_n.font.color.rgb = CREAM
        
        # Role in Be Vietnam Pro SemiBold gold tracked
        r_r = p_name.add_run()
        r_r.text = f"·  {role.upper()}"
        r_r.font.name = SANS_SEMI
        r_r.font.size = Pt(7.4 if is_compact else 8.0)
        r_r.font.color.rgb = GOLD_LIGHT
        r_r.font._element.set("spc", "100")
        
        # Duty in Playfair Editorial Italic
        p_desc = tf.add_paragraph()
        p_desc.space_after = Pt(2.5 if is_compact else 4.0)
        r_d = p_desc.add_run()
        r_d.text = f"“{desc}”"
        r_d.font.name = DISPLAY_IT
        r_d.font.italic = True
        r_d.font.size = Pt(7.6 if is_compact else 8.2)
        r_d.font.color.rgb = MUTED

prs.save("preview_red/test_slide2_deck.pptx")
print("Saved test deck!")
