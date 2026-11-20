
$statuePath = (Join-Path (Get-Location) 'assets\models3d\lenin_seattle\Lenin_Seattle_Bronze.gltf')
$pptx = (Join-Path (Get-Location) 'Triet_hoc_Mac_Lenin_Loi_chao.pptx')

$ppt = New-Object -ComObject PowerPoint.Application
$pres = $ppt.Presentations.Open($pptx)

$s2 = $pres.Slides.Item(2)
foreach ($shp in @($s2.Shapes)) {
    if ($shp.Name -like "*3D*" -or $shp.Name -like "*LENIN_SEATTLE*") { $shp.Delete() }
}

# Adjust statue position
$m2 = $s2.Shapes.Add3DModel($statuePath, 0, -1, 8.80 * 72, 0.15 * 72, 4.30 * 72, 6.80 * 72)
$m2.Name = "!!LENIN_SEATTLE_3D"
$m2.Model3D.RotationX = -90
$m2.Model3D.RotationY = 235
$m2.Model3D.RotationZ = 0

# Adjust quote box position & bring to front
foreach ($shp in @($s2.Shapes)) {
    if ($shp.Name -eq "!!LENIN_QUOTE_BG") {
        $shp.Left = 8.70 * 72
        $shp.Top = 5.45 * 72
        $shp.Width = 4.35 * 72
        $shp.Height = 1.30 * 72
        $shp.ZOrder(0)
    }
    if ($shp.Name -eq "!!LENIN_QUOTE_BOX") {
        $shp.Left = 8.70 * 72
        $shp.Top = 5.45 * 72
        $shp.Width = 4.35 * 72
        $shp.Height = 1.30 * 72
        $shp.ZOrder(0)
    }
}

$out_png = (Join-Path (Get-Location) "preview_red\test_s2_pedestal.png")
$s2.Export($out_png, "PNG", 1920, 1080)
Write-Output "Exported test_s2_pedestal.png"

$pres.Close()
$ppt.Quit()
