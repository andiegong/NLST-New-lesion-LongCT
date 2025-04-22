"""
MODIFIED FROM /Users/Amanda/Dropbox/temp-server-copy/3d-patch-classifier/nlst/dcmtonii/convert.py

the original dcmtonii() accepts a single timepoint as input
the modified dcmtonii_mod() accepted a single dcmdir as input
"""
import os
import sys
import time
import logging
import numpy as np
from argparse import ArgumentParser

import pandas as pd
import matplotlib.pyplot as plt
import SimpleITK as sitk

import utils.window as window

def dcmtonii_mod(dcmdirpath, overwrite_existing=False):
    """check hu values at each step of conversion. feb 2023"""
    print()
    print('dcmdirpath', dcmdirpath) #a single dicom directory
    #out
    savepath = dcmdirpath + '.nii.gz' #abspath
    logpath = dcmdirpath + 'dcmtonii.log'
    logging.basicConfig(filename=logpath)
    
    if os.path.exists(savepath) and not overwrite_existing:
        print(f'{savepath} already exists. Edit "overwrite_existing" variable and rerun if you would like to overwrite this file.')
    
    else:
        #this will run for all files that do not exist AND for any files that you would like to overwrite.
                
        if os.path.exists(savepath) and overwrite_existing:
            print(f'Overwriting the existing file {savepath}')
        
        #read lst of DICOM slices
        reader = sitk.ImageSeriesReader()
        dicom_names = reader.GetGDCMSeriesFileNames(dcmdirpath)
        # reader.SetFileNames(dicom_names) # defualt direction (1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0)

        ###rev direction of dicom slices###
        dicom_names_rev = os.listdir(dcmdirpath)
        dicom_names_rev.sort()
        dicom_names_rev = [os.path.join(dcmdirpath, name) for name in dicom_names_rev]

        reader.SetFileNames(dicom_names_rev)
        image = reader.Execute()
        size = image.GetSize()
        ###rev direction of dicom slices###

        #write nii file
        direction = (1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, -1.0) #set direction to (1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, -1.0). to match deeplesion data
        image.SetDirection(direction)
        image = window.window(image) #-1000, 1000 for saving
        
        try:
            print("Attempting to write image:", savepath)
            sitk.WriteImage(image, savepath)
            print("Image saved:", savepath)
        except Exception as e:
            print(f'Error with dcmtonii conversion for \n{dcmdirpath}\nlog: {logpath}')
            logging.exception(f'Exception occurred when attemping dcmtonii conversion for \n{dcmdirpath}', repr(e))
    
if __name__ == "__main__":
    start = time.time()
    plotpng = True
    
    parser = ArgumentParser(description="dicom directory path")
    parser.add_argument("dcmdirpath", type=str,)
    args = parser.parse_args()
    dcmdirpath = args.dcmdirpath
    
    #test with single
    # dcmdirpath = '/radraid/apps/personal/ajgong/nlst/manifest-NLST_allCT/NLST/100069/01-02-2000-NLST-LSS-61587'
    # dcmdirpath = '/radraid/apps/personal/ajgong/nlst/manifest-NLST_allCT/NLST/100793/01-02-2000-NLST-LSS-58210'
    
    dcmtonii_mod(dcmdirpath, plotpng)
    
    end = time.time()
    runtime = end - start
    # print("Total Time of execution {} s = {} min = {} hours".format(runtime, runtime/60, runtime/60/60))