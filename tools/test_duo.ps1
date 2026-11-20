
$path_marx = (Join-Path (Get-Location) "assets\models3d\thingiverse-4390524\files\Marx_Bust.stl")
$path_lenin = (Join-Path (Get-Location) "assets\models3d\thingiverse-573194\files\lenin.stl")

$ppt = New-Object -ComObject PowerPoint.Application
$pres = $ppt.Presentations.Open((Join-Path (Get-Location) "preview_red\test_deck_with_3d.pptx"))
$s1 = $pres.Slides.Item(1)

# Remove current 3D shapes on s1
foreach ($shp in $s1.Shapes) {
    if ($shp.Name -like "*3D*") { $shp.Delete(); break }
}

# Add Marx behind/left, Lenin in front/right
$shp_marx = $s1.Shapes.Add3DModel($path_marx, 0, -1, 7.5 * 72, 1.2 * 72, 3.8 * 72, 5.5 * 72)
$shp_marx.Name = "!!MARX_3D"
$shp_marx.Model3D.RotationY = -15
$shp_marx.Model3D.RotationX = 8

$shp_lenin = $s1.Shapes.Add3DModel($path_lenin, 0, -1, 9.2 * 72, 0.6 * 72, 4.0 * 72, 6.4 * 72)
$shp_lenin.Name = "!!LENIN_3D"
$shp_lenin.Model3D.RotationY = 25
$shp_lenin.Model3D.RotationX = 10

$s1.Export((Join-Path (Get-Location) "preview_red\test_duo_3d.png"), "PNG", 1920, 1080)

$pres.Close()
$ppt.Quit()
