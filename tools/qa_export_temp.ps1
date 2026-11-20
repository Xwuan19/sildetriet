
        $ppt = New-Object -ComObject PowerPoint.Application
        try {
            $pres = $ppt.Presentations.Open('C:\Users\ADMIN\Downloads\sildetriet\Triet_hoc_Mac_Lenin_Loi_chao.pptx', $true, $false, $false)
            $pres.Export('C:\Users\ADMIN\Downloads\sildetriet\preview_red\qa_slides_export', 'PNG', 1920, 1080)
            $pres.Close()
        } finally {
            $ppt.Quit()
        }
        