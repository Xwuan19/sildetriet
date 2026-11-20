import os
import win32com.client

ppt = win32com.client.Dispatch("PowerPoint.Application")
try:
    p = os.path.abspath("preview_red/test_slide2_layout.pptx")
    pres = ppt.Presentations.Open(p, True, False, False)
    pres.Export(os.path.abspath("preview_red/test_slide2_export"), "PNG", 1920, 1080)
    pres.Close()
    print("Exported test slide 2 layout PNG")
finally:
    ppt.Quit()
