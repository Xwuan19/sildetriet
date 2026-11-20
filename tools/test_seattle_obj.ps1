
$path_obj = (Join-Path (Get-Location) "assets\models3d\lenin_seattle\Lenin_Seattle.obj")
$ppt = New-Object -ComObject PowerPoint.Application
$pres = $ppt.Presentations.Add()
$s1 = $pres.Slides.Add(1, 12)

try {
    Write-Output "Adding 3D model from OBJ: $path_obj"
    $shp = $s1.Shapes.Add3DModel($path_obj, 0, -1, 100, 50, 400, 500)
    Write-Output ("Shape created: " + $shp.Name + ", Type: " + $shp.Type)
    $m3d = $shp.Model3D
    Write-Output ("RotationX: " + $m3d.RotationX + ", RotationY: " + $m3d.RotationY + ", RotationZ: " + $m3d.RotationZ)
    
    # Let's adjust rotation if needed
    $s1.Export((Join-Path (Get-Location) "preview_red\test_obj_render.png"), "PNG", 1920, 1080)
    Write-Output "Exported test_obj_render.png!"
} catch {
    Write-Output ("Error: " + $_.Exception.Message)
}

$pres.Close()
$ppt.Quit()
