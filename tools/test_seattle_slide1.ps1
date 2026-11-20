
$path_gltf = (Join-Path (Get-Location) "assets\models3d\lenin_seattle\Lenin_Seattle_Bronze.gltf")
$pptx_in = (Join-Path (Get-Location) "Triet_hoc_Mac_Lenin_Loi_chao.pptx")

$ppt = New-Object -ComObject PowerPoint.Application
$ppt.Visible = 1
$pres = $ppt.Presentations.Open($pptx_in)

$s1 = $pres.Slides.Item(1)
# Delete existing !!LENIN_HERO or 3D models
foreach ($shp in @($s1.Shapes)) {
    if ($shp.Name -like "*LENIN*" -or $shp.Name -like "*3D*") {
        $shp.Delete()
    }
}

# Add Seattle Lenin 3D Statue
# Widescreen 16:9 is 13.33 x 7.5 inches. (Inches * 72 = points)
# Left = 7.8 * 72, Top = 0.5 * 72, Width = 5.2 * 72, Height = 6.6 * 72
$m1 = $s1.Shapes.Add3DModel($path_gltf, 0, -1, 7.8 * 72, 0.5 * 72, 5.2 * 72, 6.6 * 72)
$m1.Name = "!!LENIN_SEATTLE_3D"
$m1.Model3D.RotationX = -90
$m1.Model3D.RotationY = 215
$m1.Model3D.RotationZ = 0

$out_png = (Join-Path (Get-Location) "preview_red\test_seattle_on_slide1.png")
$s1.Export($out_png, "PNG", 1920, 1080)
Write-Output "Exported test_seattle_on_slide1.png!"

$pres.Close()
$ppt.Quit()
