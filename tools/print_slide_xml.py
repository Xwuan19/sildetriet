import zipfile

path = r"C:\Users\ADMIN\Downloads\SlidePPT\Mau_Slide_Triet_Hoc_Mac_Lenin_Morph.pptx"
with zipfile.ZipFile(path, 'r') as z:
    print("Slide 1 XML:")
    print(z.read("ppt/slides/slide1.xml").decode("utf-8"))
    print("\nSlide 2 XML:")
    print(z.read("ppt/slides/slide2.xml").decode("utf-8"))
