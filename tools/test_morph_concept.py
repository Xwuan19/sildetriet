# -*- coding: utf-8 -*-
"""Test how PowerPoint handles Morph with !! naming and off-screen shapes."""
import sys
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from lxml import etree
from pptx.oxml.ns import qn

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

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

def add_morph(slide, dur=2000):
    sld = slide._element
    xml = MORPH_XML.replace('p14:dur="2000"', f'p14:dur="{dur}"')
    el = etree.fromstring(xml.encode("utf-8"))
    clr = sld.find(qn("p:clrMapOvr"))
    if clr is not None:
        clr.addnext(el)
    else:
        sld.append(el)

# Slide 1:
s1 = prs.slides.add_slide(prs.slide_layouts[6])
add_morph(s1)
# Box A on screen
b1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1), Inches(2), Inches(3), Inches(2))
b1.name = "!!BOX_A"
b1.fill.solid()
b1.fill.fore_color.rgb = RGBColor(200, 50, 50)

# Box B off screen (bottom)
b2_off = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6), Inches(9), Inches(3), Inches(2))
b2_off.name = "!!BOX_B"
b2_off.fill.solid()
b2_off.fill.fore_color.rgb = RGBColor(50, 150, 50)

# Slide 2:
s2 = prs.slides.add_slide(prs.slide_layouts[6])
add_morph(s2)
# Box A moves off screen (left)
b1_off = s2.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(-5), Inches(2), Inches(3), Inches(2))
b1_off.name = "!!BOX_A"
b1_off.fill.solid()
b1_off.fill.fore_color.rgb = RGBColor(200, 50, 50)

# Box B moves on screen
b2_on = s2.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6), Inches(2), Inches(4), Inches(3))
b2_on.name = "!!BOX_B"
b2_on.fill.solid()
b2_on.fill.fore_color.rgb = RGBColor(50, 150, 50)

out = Path("test_morph.pptx")
prs.save(str(out))
print("Saved test_morph.pptx")
