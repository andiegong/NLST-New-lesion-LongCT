# NLST-New-lesion-LongCT
## New Lung Lesions in Low-dose CT: a newly annotated longitudinal dataset derived from the National Lung Screening Trial

### Introduction
+ Please refer to the National Lung Screening Trial (NLST) Dataset available on the The Cancer Imaging Archive. [https://doi.org/10.7937/TCIA.HMQ8-J677]. 
+ This repository complements a dataset derived from NLST, titled NLST-New-lesion-LongCT. *New Lung Lesions in Low-dose CT: a newly annotated longitudinal dataset derived from the National Lung Screening Trial*
+ Please cite both https://doi.org/10.7937/TCIA.HMQ8-J677 and [NLST-New-lesion-LongCT doi placeholder].

### Download TCIA clinical and CT image datasets
+ Download Clinical Datasets as CSV https://www.cancerimagingarchive.net/collection/nlst/
+ Data Dictionaries are available at: https://cdas.cancer.gov/datasets/nlst/ and https://www.cancerimagingarchive.net/collection/nlst/
+ Download CT Image Data as DICOM files

### Apply lesion selection criteria
Apply lesion-level and screening timepoint-level selection criteria using NLST clinical data
```
selectscans.py
```

### Example of preprocessing and registering CT image data
+ Read and preprocess DICOM images, convert to NIfTI files.
```
preprocess.py
```

+ Given a pair of CT scans that correspond to baseline and follow-up scans for a given patient, perform image registration. Save result image and transformation maps.
```
registerpair.py
```