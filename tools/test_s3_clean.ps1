
$statuePath = (Join-Path (Get-Location) 'assets\models3d\lenin_seattle\Lenin_Seattle_Bronze.gltf')
$pptx = (Join-Path (Get-Location) 'Triet_hoc_Mac_Lenin_Loi_chao.pptx')

$ppt = New-Object -ComObject PowerPoint.Application
$pres = $ppt.Presentations.Open($pptx)

$s3 = $pres.Slides.Item(3)
foreach ($shp in @($s3.Shapes)) {
    if ($shp.Name -like "*3D*" -or $shp.Name -like "*LENIN*") { $shp.Delete() }
}
$m3 = $s3.Shapes.Add3DModel($statuePath, 0, -1, 8.15 * 72, 0.25 * 72, 4.70 * 72, 6.60 * 72)
$m3.Name = "!!LENIN_SEATTLE_3D"
$m3.Model3D.RotationX = -90
$m3.Model3D.RotationY = 265
$m3.Model3D.RotationZ = 0

foreach ($shp in @($s3.Shapes)) {
    if ($shp.Name -like "*BADGE*") {
        $shp.ZOrder(0) # msoBringToFront
    }
}

$out_png = (Join-Path (Get-Location) "preview_red\test_s3_clean.png")
$s3.Export($out_png, "PNG", 1920, 1080)
Write-Output "Exported test_s3_clean.png"

$pres.Close()
$ppt.Quit()
