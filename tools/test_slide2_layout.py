import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE
from pathlib import Path

prs = pptx.Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
s = prs.slides.add_slide(prs.slide_layouts[6])

# Test adding poster and emblems
s.shapes.add_picture("assets/soviet_worker_flag_clean.png", Inches(0.4), Inches(2.2), Inches(5.0), Inches(5.0))
s.shapes.add_picture("assets/soviet_hammer_sickle_clean.png", Inches(1.35), Inches(0.55), Inches(1.15), Inches(1.00))
s.shapes.add_picture("assets/soviet_3d_star_clean.png", Inches(2.65), Inches(0.50), Inches(1.15), Inches(1.10))
s.shapes.add_picture("assets/lenin_hero_clean.png", Inches(8.60), Inches(1.00), Inches(4.70), Inches(6.30))

prs.save("preview_red/test_slide2_layout.pptx")
print("Saved test_slide2_layout.pptx")
