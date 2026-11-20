# -*- coding: utf-8 -*-
"""
Tải font Google Fonts (có bộ ký tự tiếng Việt), tạo instance tĩnh và cài
cho riêng người dùng Windows (không cần quyền admin).

Font dùng trong deck:
  - Playfair Display Black / Black Italic  (tiêu đề lớn, đậm, có dấu tiếng Việt)
  - Script Viet Bold                       (dòng chào viết tay, phái sinh từ Dancing Script)
  - Be Vietnam Pro / SemiBold / Bold       (thân bài, thiết kế cho tiếng Việt)
"""
from __future__ import annotations

import ctypes
import os
import shutil
import sys
import urllib.request
from pathlib import Path

from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parent.parent
FONTS = ROOT / "fonts"
SRC = FONTS / "src"
FONTS.mkdir(exist_ok=True)
SRC.mkdir(exist_ok=True)

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124 Safari/537.36"
MIRRORS = [
    "https://cdn.jsdelivr.net/gh/google/fonts@main/ofl/{path}",
    "https://raw.githubusercontent.com/google/fonts/main/ofl/{path}",
]


def download(path: str, dest: Path) -> Path:
    if dest.exists() and dest.stat().st_size > 20_000:
        print(f"  đã có: {dest.name}")
        return dest
    last = None
    for mirror in MIRRORS:
        url = mirror.format(path=path)
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=90) as resp:
                data = resp.read()
            if len(data) < 20_000:
                raise ValueError("file quá nhỏ")
            dest.write_bytes(data)
            print(f"  tải: {dest.name} ({len(data)/1024:.0f} KB)")
            return dest
        except Exception as exc:  # noqa: BLE001
            last = exc
            print(f"  lỗi mirror {mirror.split('/')[2]}: {exc}")
    raise SystemExit(f"Không tải được {path}: {last}")


def set_names(font: TTFont, family: str, style: str, full: str, ps: str,
              weight: int, italic: bool = False, bold: bool = False) -> None:
    name = font["name"]
    for rec in list(name.names):
        if rec.nameID in (1, 2, 3, 4, 6, 16, 17, 21, 22, 25, 256, 262, 269, 270):
            name.removeNames(nameID=rec.nameID)
    for plat, enc, lang in ((3, 1, 0x409), (1, 0, 0)):
        name.setName(family, 1, plat, enc, lang)
        name.setName(style, 2, plat, enc, lang)
        name.setName(f"{full} v1.0", 3, plat, enc, lang)
        name.setName(full, 4, plat, enc, lang)
        name.setName(ps, 6, plat, enc, lang)
        name.setName(family, 16, plat, enc, lang)
        name.setName(style, 17, plat, enc, lang)
        name.setName(family, 21, plat, enc, lang)
        name.setName(style, 22, plat, enc, lang)
    os2 = font["OS/2"]
    os2.usWeightClass = weight
    if bold:
        os2.fsSelection = (os2.fsSelection & ~0b100000) | 0b100000  # BOLD
    else:
        os2.fsSelection &= ~0b100000
    if italic:
        os2.fsSelection = (os2.fsSelection & ~0b1) | 0b1  # ITALIC
        os2.fsSelection &= ~0b1000000  # REGULAR off
    else:
        os2.fsSelection &= ~0b1
    if weight == 400 and not italic:
        os2.fsSelection = (os2.fsSelection & ~0b1000000) | 0b1000000
    font["head"].macStyle = (1 if bold else 0) | (2 if italic else 0)


def make_instance(src: Path, dest: Path, axes: dict, family: str,
                  weight: int, italic: bool = False) -> Path:
    if dest.exists() and dest.stat().st_size > 20_000:
        print(f"  đã có: {dest.name}")
        return dest
    font = TTFont(str(src))
    if "fvar" in font:
        instantiateVariableFont(font, axes, inplace=True, updateFontNames=False)
    # STAT còn giữ tên trục "Black"/"Bold" của font biến thiên; Windows sẽ ghép
    # hậu tố đó vào tên family. Bỏ STAT để family hiển thị đúng.
    if "STAT" in font:
        del font["STAT"]
    ps = dest.stem.replace(" ", "")
    set_names(font, family, "Regular", family, ps, weight, italic=italic, bold=False)
    font.save(str(dest))
    print(f"  tạo: {dest.name} ({dest.stat().st_size/1024:.0f} KB)")
    return dest


def install_user_font(path: Path) -> None:
    user_fonts = Path(os.environ["LOCALAPPDATA"]) / "Microsoft" / "Windows" / "Fonts"
    user_fonts.mkdir(parents=True, exist_ok=True)
    target = user_fonts / path.name
    shutil.copy2(path, target)
    import winreg
    key_path = r"Software\Microsoft\Windows NT\CurrentVersion\Fonts"
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE) as key:
        winreg.SetValueEx(key, f"{path.stem} (TrueType)", 0, winreg.REG_SZ, path.name)
    ctypes.windll.gdi32.AddFontResourceW(str(target))
    print(f"  cài: {path.name}")


def broadcast_font_change() -> None:
    HWND_BROADCAST = 0xFFFF
    WM_FONTCHANGE = 0x001D
    ctypes.windll.user32.PostMessageW(HWND_BROADCAST, WM_FONTCHANGE, 0, 0)


def main() -> None:
    print("1. Tải font gốc")
    playfair = download("playfairdisplay/PlayfairDisplay%5Bwght%5D.ttf", SRC / "PlayfairDisplay-VF.ttf")
    playfair_it = download("playfairdisplay/PlayfairDisplay-Italic%5Bwght%5D.ttf", SRC / "PlayfairDisplay-Italic-VF.ttf")
    dancing = download("dancingscript/DancingScript%5Bwght%5D.ttf", SRC / "DancingScript-VF.ttf")

    print("2. Be Vietnam Pro")
    be_paths = {}
    static_ok = True
    for style, weight in (("Regular", 400), ("SemiBold", 600), ("Bold", 700)):
        try:
            be_paths[style] = download(
                f"bevietnampro/BeVietnamPro-{style}.ttf", SRC / f"BeVietnamPro-{style}.ttf")
        except SystemExit:
            static_ok = False
            break
    if not static_ok:
        print("  dùng variable font cho Be Vietnam Pro")
        try:
            be_var = download("bevietnampro/BeVietnamPro%5Bwght%5D.ttf", SRC / "BeVietnamPro-VF.ttf")
        except SystemExit:
            be_var = download("bevietnampro/BeVietnamPro%5Bital%2Cwght%5D.ttf", SRC / "BeVietnamPro-VF.ttf")
        be_paths = {}

    print("3. Tạo instance tĩnh")
    outputs = []
    # Tên family riêng, không chứa hậu tố kiểu "Black" để Windows không ghép đôi.
    # usWeightClass để 400 vì độ đậm đã nằm trong outline và tên family.
    outputs.append(make_instance(playfair, FONTS / "PlayfairEditorial.ttf",
                                 {"wght": 900}, "Playfair Editorial", 400))
    outputs.append(make_instance(playfair_it, FONTS / "PlayfairEditorial-Italic.ttf",
                                 {"wght": 900}, "Playfair Editorial Italic", 400, italic=True))
    # OFL cấm dùng tên dành riêng "Dancing Script" cho bản sửa đổi, nên đổi family.
    outputs.append(make_instance(dancing, FONTS / "ScriptViet-Bold.ttf",
                                 {"wght": 700}, "Script Viet", 700))
    if static_ok:
        for style, weight in (("Regular", 400), ("SemiBold", 600), ("Bold", 700)):
            src = be_paths[style]
            dest = FONTS / f"BeVietnamPro-{style}.ttf"
            if dest.exists() and dest.stat().st_size > 20_000:
                print(f"  đã có: {dest.name}")
            else:
                font = TTFont(str(src))
                family = "Be Vietnam Pro" if style == "Regular" else f"Be Vietnam Pro {style}"
                set_names(font, family, "Regular", family,
                          f"BeVietnamPro-{style}", weight)
                font.save(str(dest))
                print(f"  tạo: {dest.name}")
            outputs.append(dest)
    else:
        for style, weight in (("Regular", 400), ("SemiBold", 600), ("Bold", 700)):
            family = "Be Vietnam Pro" if style == "Regular" else f"Be Vietnam Pro {style}"
            outputs.append(make_instance(be_var, FONTS / f"BeVietnamPro-{style}.ttf",
                                         {"wght": weight}, family, weight))

    print("4. Cài font cho người dùng Windows")
    for path in outputs:
        install_user_font(path)
    broadcast_font_change()

    # Dọn bản Playfair cũ (nếu có) để menu font không bị trùng.
    import winreg
    user_fonts = Path(os.environ["LOCALAPPDATA"]) / "Microsoft" / "Windows" / "Fonts"
    key_path = r"Software\Microsoft\Windows NT\CurrentVersion\Fonts"
    for old_name in ("PlayfairDisplay-Black", "PlayfairDisplay-BlackItalic", "DancingScript-Bold"):
        old_file = user_fonts / f"{old_name}.ttf"
        if old_file.exists():
            ctypes.windll.gdi32.RemoveFontResourceW(str(old_file))
            try:
                old_file.unlink()
            except OSError:
                pass
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE) as key:
                winreg.DeleteValue(key, f"{old_name} (TrueType)")
        except OSError:
            pass
    broadcast_font_change()
    print("Xong. Mở PowerPoint mới để nhận font.")


if __name__ == "__main__":
    main()
