
$pptx = (Join-Path (Get-Location) "preview_red\test_mat.pptx")
$ppt = New-Object -ComObject PowerPoint.Application
$pres = $ppt.Presentations.Add()
$s1 = $pres.Slides.Add(1, 12)
$shp = $s1.Shapes.Add3DModel((Join-Path (Get-Location) "preview_red\test_red_mat.gltf"), 0, -1, 150, 40, 450, 580)
$s1.Export((Join-Path (Get-Location) "preview_red\test_red_render.png"), "PNG", 1920, 1080)
$pres.Close()
$ppt.Quit()
Write-Output "Done test red"
