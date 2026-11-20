
$path_marx = "C:\Users\ADMIN\Downloads\sildetriet\assets\models3d\thingiverse-4390524\files\Marx_Bust.stl"
$path_lenin2 = "C:\Users\ADMIN\Downloads\sildetriet\assets\models3d\thingiverse-5150309\lenin.stl"

$ppt = New-Object -ComObject PowerPoint.Application
$pres = $ppt.Presentations.Add()

$slide1 = $pres.Slides.Add(1, 12)
$shp_m = $slide1.Shapes.Add3DModel($path_marx, 0, -1, 100, 100, 350, 350)
$shp_m.Model3D.RotationY = 30
$slide1.Export((Join-Path (Get-Location) "preview_red\test_marx_render.png"), "PNG", 1920, 1080)

$slide2 = $pres.Slides.Add(2, 12)
$shp_l2 = $slide2.Shapes.Add3DModel($path_lenin2, 0, -1, 100, 100, 350, 350)
$shp_l2.Model3D.RotationY = 30
$slide2.Export((Join-Path (Get-Location) "preview_red\test_lenin2_render.png"), "PNG", 1920, 1080)

$pres.Close()
$ppt.Quit()
