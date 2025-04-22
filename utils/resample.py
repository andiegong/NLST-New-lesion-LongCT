import numpy as np
import SimpleITK as sitk

def resample_img(itk_image, out_spacing=[1.0, 1.0, 1.0], is_label=False):
    """
    Resample an ITK image object to specified voxel size.
    ref https://gist.github.com/mrajchl/ccbd5ed12eb68e0c1afc5da116af614a
    
    Args:
        itk_image (ITK image object): input image.
        out_spacing (list of three floats, optional): voxel dimensions of the output image in millimeters, default [1.0, 1.0, 1.0].
        is_label (bool, optional): Bool to indicate if the itk_image is an image label, default False. If True, this function will use the NearestNeighbor interpolator for an image label. If False, this function will use the BSpline interpolator for a CT image.
    
    Returns:
        resampled ITK image object of the specified voxel size.
    """
    original_spacing = itk_image.GetSpacing()
    original_size = itk_image.GetSize()

    out_size = [
        int(np.round(original_size[0] * (original_spacing[0] / out_spacing[0]))),
        int(np.round(original_size[1] * (original_spacing[1] / out_spacing[1]))),
        int(np.round(original_size[2] * (original_spacing[2] / out_spacing[2])))]

    resample = sitk.ResampleImageFilter()
    resample.SetOutputSpacing(out_spacing)
    resample.SetSize(out_size)
    resample.SetOutputDirection(itk_image.GetDirection())
    resample.SetOutputOrigin(itk_image.GetOrigin())
    resample.SetTransform(sitk.Transform())
    resample.SetDefaultPixelValue(itk_image.GetPixelIDValue())

    if is_label:
        resample.SetInterpolator(sitk.sitkNearestNeighbor)
    else:
        resample.SetInterpolator(sitk.sitkBSpline)

    return resample.Execute(itk_image)