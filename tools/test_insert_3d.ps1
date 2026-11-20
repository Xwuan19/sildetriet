
$ppt = New-Object -ComObject PowerPoint.Application
$ppt.Visible = 1
$pres = $ppt.Presentations.Add()

Write-Output "Testing Add3DModel with Lenin STL: C:/Users/ADMIN/Downloads/sildetriet/assets/models3d/thingiverse-573194/files/lenin.stl"
$slide1 = $pres.Slides.Add(1, 12) # ppLayoutBlank = 12
$shp1 = $slide1.Shapes.Add3DModel("C:/Users/ADMIN/Downloads/sildetriet/assets/models3d/thingiverse-573194/files/lenin.stl", 0, 1, 100, 100, 300, 300)
Write-Output ("Shape created: " + $shp1.Name + ", Type: " + $shp1.Type)

# Inspect Model3DFormat
$m3d = $shp1.Model3D
Write-Output ("Model3D properties: " + ($m3d | Get-Member | Select-Object -ExpandProperty Name))
Write-Output ("Initial RotationX: " + $m3d.RotationX + ", RotationY: " + $m3d.RotationY + ", RotationZ: " + $m3d.RotationZ)

# Set rotation
$m3d.RotationY = 45
Write-Output ("New RotationY: " + $m3d.RotationY)

# Add slide 2 and morph
$slide2 = $pres.Slides.Add(2, 12)
$shp2 = $slide2.Shapes.Add3DModel("C:/Users/ADMIN/Downloads/sildetriet/assets/models3d/thingiverse-573194/files/lenin.stl", 0, 1, 400, 100, 300, 300)
$shp2.Name = $shp1.Name # Match name for morph
$shp2.Model3D.RotationY = 180

# Configure Morph
$slide2.SlideShowTransition.EntryEffect = 3915 # Morph transition code
$slide2.SlideShowTransition.Duration = 2.0

$test_pptx = (Join-Path (Get-Location) "preview_red\test_3d_morph.pptx")
$pres.SaveAs($test_pptx)
$pres.Close()
$ppt.Quit()
Write-Output "Saved test presentation successfully!"
