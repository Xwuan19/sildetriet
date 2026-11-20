from pathlib import Path

win_fonts = list(Path(r"C:\Windows\Fonts").glob("*Playfair*"))
print("Installed Playfair fonts in Windows:", win_fonts)
