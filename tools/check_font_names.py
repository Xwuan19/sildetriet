from fontTools.ttLib import TTFont

font = TTFont("fonts/PlayfairEditorial.ttf")
for record in font['name'].names:
    if record.nameID in (1, 2, 4, 6):
        print(record.nameID, record.toStr())
