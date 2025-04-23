# NLST-New-lesion-LongCT
### Introduction
+ NLST-New-lesion-LongCT is a medical imaging dataset that is derived from the [The National Lung Screening Trial (NLST) Dataset](https://doi.org/10.7937/TCIA.HMQ8-J677) available on the The Cancer Imaging Archive (TCIA).
+ Please refer to our dataset and description *New Lung Lesions in Low-dose CT: a newly annotated longitudinal dataset derived from the National Lung Screening Trial*, available on TCIA at [NLST-New-lesion-LongCT](placeholderurl) (link to be updated).

### Cite
If you find our dataset NLST-New-lesion-LongCT or the associated code useful in your work, please cite both:
* The parent dataset: [The National Lung Screening Trial (NLST)](https://doi.org/10.7937/TCIA.HMQ8-J677)
* Our derivative dataset: [NLST-New-lesion-LongCT](placeholderurl)

### Download TCIA clinical and CT image datasets
+ Download Clinical Datasets as CSV https://www.cancerimagingarchive.net/collection/nlst/
+ Data Dictionaries are available at: https://cdas.cancer.gov/datasets/nlst/ and https://www.cancerimagingarchive.net/collection/nlst/
+ Download CT Image Data as DICOM files

### Apply lesion selection criteria
We identify new lesions of interest by applying lesion-level and screening timepoint-level selection criteria using NLST clinical data as demonstrated here:
```
selectscans.py
```

### Example of preprocessing and registering CT image data
A brief example of our preprocessing and registration pipeline.
+ Read and preprocess DICOM images and convert to NIfTI files.
    ```
    preprocess.py
    ```

+ Upon identifying a new lung lesion of interest, register the scan (follow-up) with a CT from the same patient at a prior timepoint (baseline). The following example registers a pair of CT scans, and saves the transformation maps.
    ```
    registerpair.py
    ```