# -*- coding: utf-8 -*-
import subprocess

ps_test = r"""
$statuePath = (Join-Path (Get-Location) 'assets\models3d\lenin_seattle\Lenin_Seattle_Bronze.gltf')
$pptx = (Join-Path (Get-Location) 'Triet_hoc_Mac_Lenin_Loi_chao.pptx')

$ppt = New-Object -ComObject PowerPoint.Application
$pres = $ppt.Presentations.Open($pptx)

$s1 = $pres.Slides.Item(1)
foreach ($shp in @($s1.Shapes)) {
    if ($shp.Name -like "*3D*" -or $shp.Name -like "*LENIN*") { $shp.Delete() }
}
$m1 = $s1.Shapes.Add3DModel($statuePath, 0, -1, 8.15 * 72, 0.25 * 72, 4.70 * 72, 6.60 * 72)
$m1.Name = "!!LENIN_SEATTLE_3D"
$m1.Model3D.RotationX = -90
$m1.Model3D.RotationY = 205
$m1.Model3D.RotationZ = 0

$out_png = (Join-Path (Get-Location) "preview_red\test_s1_clean.png")
$s1.Export($out_png, "PNG", 1920, 1080)
Write-Output "Exported test_s1_clean.png"

$pres.Close()
$ppt.Quit()
"""

with open("tools/test_s1_clean.ps1", "w", encoding="utf-8") as f:
    f.write(ps_test)

res = subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", "tools/test_s1_clean.ps1"], capture_output=True, text=True)
print(res.stdout)
