from PIL import Image

for uid in [
    "ff2ce66e-e1af-4dcd-a6f3-371237481d50",
    "ef722432-40dc-4a74-a693-b2fa52917581",
    "e989484d-71c1-4601-9420-581dcdfca095",
    "a76de109-4561-47f9-af9f-73df23cdee12"
]:
    p = rf"C:\Users\ADMIN\AppData\Local\Temp\opencode\uploads\{uid}\image.png"
    im = Image.open(p)
    print(f"{uid}: size={im.size}, mode={im.mode}")
