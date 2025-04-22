import numpy as np
import os

import pandas as pd
import SimpleITK as sitk

import utils.window as window
import utils.abbrev as abbrev

def register_pair(baselinepath, followuppath, regsavedir, registration_pmap='trans_affine', wmin=-1000, wmax=1000, abbrev_fname=True):
    """
    Register a pair of CT images in NIfTI files (i.e. Baseline and Follow-up image pair) using a subset of Simple ITK's pre-defined registration parameter maps. This function saves the transformation maps that define the registration.
    We set the baseline scan as the Moving Image and follow-up scan as the Fixed Image in order to avoid introducting registration artifiacts / image distortion into new lesions that are identified on follow-up.
    
    Args:
        baselinepath (str): path to moving image in NIfTI file.
        followuppath (str): path to fixed image in NIfTI file.
        regsavedir (str): path to a directory in which output files generated from this image registration will be saved.
        registration_pmap (str): {'trans_affine', 'trans_affine_bspline'}, default 'trans_affine'. Set sequential registration parameter maps using pre-defined registration parameter maps from Simple ITK. Translation, Affine, and B-Spline transforamtions.
        wmin (integer, optional): Minimum Hounsefield Unit value when applying a CT window to the Moving Image, default -1000.
        wmax (integer, optional): Maximum Hounsefield Unit value when applying a CT window to the Moving Image, default, 1000.
        abbrev_fname (bool, optional): Use abbreviated baseline and follow up scan file names for registration output files, default True.
    
    Returns:
        ITK image object, the registered moving (baseline) image.
        
    Raises:
        TODO
    """
    
    # Optionally abbreviate output filenames
    if abbrev_fname:
        bimgfname = abbrev.abbrev_fname(bimgfname)
        fuimgfname = abbrev.abbrev_fname(fuimgfname)
    else:
        bimgfname = os.path.splitext(os.path.basename(bimgfname))[0]
        fuimgfname = os.path.splitext(os.path.basename(fuimgfname))[0]

    # Set output file savepaths
    imgsavepath = os.path.join(regsavedir, f'baseline_registered_{registration_pmap}_humin{wmin}_humax{wmax}_B{bimgfname}_{fuimgfname}.nii.gz')
    transpmapdir = os.path.join(regsavedir, 'reg_transform_pmap_' + registration_pmap)
    os.makedirs(regsavedir, exist_ok=True)
    os.makedirs(transpmapdir, exist_ok=True)
    
    # Define Registration Parameter Maps
    elastixImageFilter = sitk.ElastixImageFilter()
    if registration_pmap=='trans_affine':
        pmap = sitk.GetDefaultParameterMap('translation')
        elastixImageFilter.SetParameterMap(pmap)
        elastixImageFilter.AddParameterMap(sitk.GetDefaultParameterMap('affine'))
    elif registration_pmap=='trans_affine_bspline':
        pass # SITK default registration parameter map is trans_affine_bspline
    else:
        print(f'registration_pmap {registration_pmap} not supported')
        #TODO Raise custom error 
        return
    
    # Set follow-up scan as the Fixed Image
    fixedImage = sitk.ReadImage(followuppath)
    fixedImage = window.window(fixedImage, wmin, wmax) # Apply CT Windowing
    elastixImageFilter.SetFixedImage(fixedImage)
    # Set baseline scan as the Moving Image
    movingImageorig = sitk.ReadImage(baselinepath)
    movingImage = window.window(movingImageorig, wmin, wmax) # Apply CT Windowing
    elastixImageFilter.SetMovingImage(movingImage)

    # Execute Registration
    elastixImageFilter.LogToFileOn()
    elastixImageFilter.SetOutputDirectory(transpmapdir) # Save Transformation Maps
    elastixImageFilter.Execute()
    
    # Save Result Image
    resultImage = elastixImageFilter.GetResultImage()
    sitk.WriteImage(resultImage, imgsavepath)
    return resultImage
    
if __name__ == "__main__":
    
    baselineCTpath = 'baselinescan.nii.gz'
    followupCTpath = 'followupscan.nii.gz'
    regoutdir = 'regoutdirpath/'
    registration_pmap = 'trans_affine'
    
    register_pair(baselineCTpath, followupCTpath, regoutdir, registration_pmap)