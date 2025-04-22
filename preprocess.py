import os
import numpy as np

import pandas as pd
import SimpleITK as sitk

import utils.window as window
import utils.resample as resample

def dcmtonii(dcmdirpath, HUwindow=(-1000,1000), overwrite_existing=False, resample_set=False):
    """
    Convert a single DICOM image to a NIfTI file of the same name. Apply CT windowing.
    
    Args:
        dcmdirpath (str): pathname to a single DICOM image directory
        HUwindow (tup, optional): CT window minimum and maximum values in Hounsfield Units, default (-1000, 1000).
        overwrite_existing (bool, optional): Bool to indiate whether to overwrite an existing NIfTI file, default False. If False, skip the given DICOM image and return None.
        resample_set (bool, optional): Bool for resampling the image to 1x1x1 Voxels, default False.
        
    Returns:
        pathname to the saved NIfTI file or None if the file already existed and DICOM image was skipped.
    """
    # NIfTI savepath
    savepath = dcmdirpath + '.nii.gz'
    
    if os.path.exists(savepath) and not overwrite_existing:
        print(f'{savepath} file already exists.')
        return
    else:
        if os.path.exists(savepath) and overwrite_existing:
            print(f'{savepath} file already exists. Overwriting this file.')
        
        reader = sitk.ImageSeriesReader()
        dicom_names = reader.GetGDCMSeriesFileNames(dcmdirpath)
        reader.SetFileNames(dicom_names) # defualt direction (1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0)
        image = reader.Execute()
        
        # Specify Image Direction. Modify if a non-standard image direction is desired.
        direction = (1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0) # default direction
        image.SetDirection(direction)
        
        # Apply CT Windowing
        image = window.window(image, HUwindow=HUwindow)
        
        # Optionally, resample the NIfTI image to 1x1x1mm voxels.
        if resample_set:
            image = resample.resample_img(image)
        
        # Save NIfTI
        sitk.WriteImage(image, savepath)
        return savepath
    
if __name__ == "__main__":
    # Download NLST CT Image Data to local directory using the NBIA Data Retriever as described on TCIA
    datadir_alldcm = 'nlstCTdata-download/'
    
    for singledcmdir in datadir_alldcm:
        dcmtonii(singledcmdir)