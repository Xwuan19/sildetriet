
$ppt = New-Object -ComObject PowerPoint.Application
$pres = $ppt.Presentations.Add()
$pres.PageSetup.SlideWidth = 13.333 * 72
$pres.PageSetup.SlideHeight = 7.50 * 72

$models = @("Dark_Bronze", "Warm_Bronze_Gold", "Deep_Antique_Bronze", "Ivory_Marble")
for ($i = 0; $i -lt $models.Count; $i++) {
    $name = $models[$i]
    $s = $pres.Slides.Add($i + 1, 12)
    # Set background crimson
    $bg = $s.Shapes.AddShape(1, 0, 0, 13.333 * 72, 7.50 * 72)
    $bg.Fill.Solid()
    $bg.Fill.ForeColor.RGB = 0x14126B # #6B1214 BGR
    $bg.Line.Visible = 0
    
    $m_path = (Join-Path (Get-Location) "preview_red\test_$name.gltf")
    $m = $s.Shapes.Add3DModel($m_path, 0, -1, 8.15 * 72, 0.25 * 72, 4.70 * 72, 6.60 * 72)
    $m.Model3D.RotationX = -90
    $m.Model3D.RotationY = 205
    $m.Model3D.RotationZ = 0
    
    $out_png = (Join-Path (Get-Location) "preview_red\test_col_$name.png")
    $s.Export($out_png, "PNG", 1920, 1080)
}

$pres.Close()
$ppt.Quit()
Write-Output "Done testing 4 colors!"
