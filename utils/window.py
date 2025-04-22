import SimpleITK as sitk

def window(img_pre, HUwindow=(-1000,1000)):
    """
    Apply CT windowing to a ITK image object.
    
    Args:
        img_pre (ITK image object): input image
        HUwindow (tup, optional): CT window minimum and maximum values in Hounsfield Units, default (-1000, 1000).
        
    Returns:
        img_post (ITK image object): output image, after applying the specified CT window to the input.
    """
    wmin = HUwindow[0]
    wmax = HUwindow[1]
    windowfilter = sitk.IntensityWindowingImageFilter()
    windowfilter.SetWindowMaximum(wmax)
    windowfilter.SetWindowMinimum(wmin)

    windowfilter.SetOutputMaximum(wmax)
    windowfilter.SetOutputMinimum(wmin)
    img_post = windowfilter.Execute(img_pre)
    
    return img_post