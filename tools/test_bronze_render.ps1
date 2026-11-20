
$path_gltf = (Join-Path (Get-Location) "assets\models3d\lenin_seattle\Lenin_Seattle_Bronze.gltf")
$ppt = New-Object -ComObject PowerPoint.Application
$pres = $ppt.Presentations.Add()
$s1 = $pres.Slides.Add(1, 12)

try {
    $shp = $s1.Shapes.Add3DModel($path_gltf, 0, -1, 150, 40, 450, 580)
    $shp.Model3D.RotationX = -90
    $shp.Model3D.RotationY = 25
    $shp.Model3D.RotationZ = 0
    
    $out_png = (Join-Path (Get-Location) "preview_red\test_bronze_render.png")
    $s1.Export($out_png, "PNG", 1920, 1080)
    Write-Output "Exported test_bronze_render.png!"
} catch {
    Write-Output ("Error: " + $_.Exception.Message)
}

$pres.Close()
$ppt.Quit()
