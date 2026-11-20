# -*- coding: utf-8 -*-
from pptx import Presentation
from pptx.oxml.xmlchemy import OxmlElement

prs_old = Presentation("archive/debug/embed_test.pptx")
s0 = prs_old.slides[0]
for shp in s0.shapes:
    if shp.name in ["BG_DEEP", "!!BG_DEEP"]:
        print("OLD BG_DEEP XML:\n", shp._element.spPr.xml)

prs_new = Presentation("Triet_hoc_Mac_Lenin_Loi_chao.pptx")
s0_new = prs_new.slides[0]
for shp in s0_new.shapes:
    if shp.name in ["BG_DEEP", "!!BG_DEEP"]:
        print("NEW BG_DEEP XML:\n", shp._element.spPr.xml)
