import zipfile

src = r"C:\Users\ADMIN\Downloads\SlidePPT\Mau_Slide_Triet_Hoc_Mac_Lenin_Morph.pptx"
with zipfile.ZipFile(src, 'r') as z:
    for n in sorted(z.namelist()):
        if "media" in n:
            print(n, z.getinfo(n).file_size)
