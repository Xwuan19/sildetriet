import zipfile
import xml.etree.ElementTree as ET

path = r"C:\Users\ADMIN\Downloads\SlidePPT\Mau_Slide_Triet_Hoc_Mac_Lenin_Morph.pptx"
with zipfile.ZipFile(path, 'r') as z:
    for name in z.namelist():
        if name.startswith("ppt/slides/slide1.xml"):
            xml_content = z.read(name)
            root = ET.fromstring(xml_content)
            # Find all cNvPr (names of shapes)
            for el in root.iter():
                if el.tag.endswith("cNvPr"):
                    print("Slide 1 shape:", el.attrib.get("name"), el.attrib.get("id"))

        if name.startswith("ppt/slides/slide2.xml"):
            xml_content = z.read(name)
            root = ET.fromstring(xml_content)
            for el in root.iter():
                if el.tag.endswith("cNvPr"):
                    print("Slide 2 shape:", el.attrib.get("name"), el.attrib.get("id"))
