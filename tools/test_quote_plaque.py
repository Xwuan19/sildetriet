# -*- coding: utf-8 -*-
import subprocess

ps_test = r"""
$path_gltf = (Join-Path (Get-Location) "assets\models3d\lenin_seattle\Lenin_Seattle_Bronze.gltf")
$ppt = New-Object -ComObject PowerPoint.Application
$pres = $ppt.Presentations.Add()
$s = $pres.Slides.Add(1, 12)

# 1. Add 3D model
$m = $s.Shapes.Add3DModel($path_gltf, 0, -1, 9.20 * 72, 0.50 * 72, 3.90 * 72, 6.40 * 72)
$m.Model3D.RotationX = -90
$m.Model3D.RotationY = 240
$m.Model3D.RotationZ = 0

# 2. Add Quote Plaque shape
$q_bg = $s.Shapes.AddShape(1, 9.20 * 72, 5.85 * 72, 3.75 * 72, 1.00 * 72)
$q_bg.Fill.Solid()
$q_bg.Fill.ForeColor.RGB = 0x18135C # Dark red/card bg in BGR: 0x18, 0x13, 0x5C -> 0x5C1318 in RGB is R=92, G=19, B=24 -> BGR is 24 + 19*256 + 92*65536 = 6034200
$q_bg.Line.ForeColor.RGB = 0x74C9E2 # Gold in BGR
$q_bg.Line.Weight = 1.0

# Bring to front
$q_bg.ZOrder(0) # msoBringToFront

$tb = $s.Shapes.AddTextbox(1, 9.20 * 72, 5.85 * 72, 3.75 * 72, 1.00 * 72)
$tb.TextFrame.Text = "“Không có lý luận cách mạng thì`nkhông có phong trào cách mạng.”`n— V. I. LÊNIN (1902)"
$tb.TextFrame.TextRange.Font.Size = 9
$tb.TextFrame.TextRange.Font.Color.RGB = 0xB8E6F5
$tb.ZOrder(0)

$out_png = (Join-Path (Get-Location) "preview_red\test_quote_plaque_front.png")
$s.Export($out_png, "PNG", 1920, 1080)
Write-Output "Exported test_quote_plaque_front.png"

$pres.Close()
$ppt.Quit()
"""

with open("tools/test_quote_plaque.ps1", "w", encoding="utf-8") as f:
    f.write(ps_test)

res = subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", "tools/test_quote_plaque.ps1"], capture_output=True, text=True)
print(res.stdout)
if res.stderr:
    print("Stderr:", res.stderr)
