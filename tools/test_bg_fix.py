# -*- coding: utf-8 -*-
from pptx import Presentation
from pptx.util import Inches
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn
from lxml import etree

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.500)
slide = prs.slides.add_slide(prs.slide_layouts[6])

shp = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.500))
shp.name = "!!BG_DEEP"
shp.line.fill.background()

# Now apply gradient_shape
def gradient_shape(shape, stops, angle=118, radial=False):
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

gradient_shape(shp, [(0.00, "8E191D", None), (0.42, "650E13", None), (1.00, "2C0408", None)], angle=118)

print("Generated spPr XML:\n", shp._element.spPr.xml)
prs.save("preview_red/test_grad_bg.pptx")
print("Saved preview_red/test_grad_bg.pptx")
