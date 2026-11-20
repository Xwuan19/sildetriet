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
$q_bg.Fill.ForeColor.RGB = 6034200
$q_bg.Line.ForeColor.RGB = 7653858
$q_bg.Line.Weight = 1.0

# Bring to front
$q_bg.ZOrder(0)

$tb = $s.Shapes.AddTextbox(1, 9.20 * 72, 5.85 * 72, 3.75 * 72, 1.00 * 72)
$tb.TextFrame.Text = "Khong co ly luan cach mang thi khong co phong trao cach mang.`n- V. I. LENIN (1902)"
$tb.TextFrame.TextRange.Font.Size = 9
$tb.TextFrame.TextRange.Font.Color.RGB = 12117752
$tb.ZOrder(0)

$out_png = (Join-Path (Get-Location) "preview_red\test_quote_plaque_front.png")
$s.Export($out_png, "PNG", 1920, 1080)
Write-Output "Exported test_quote_plaque_front.png"

$pres.Close()
$ppt.Quit()
