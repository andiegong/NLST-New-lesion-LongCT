import os
import pandas as pd

def applyselectioncriteria(datadircsv, csvout):
    """
    Apply lesion selection criteria, as described in the Dataset description, section "Lesion Selection: Overview"
    
    Args:
        datadircsv (str): pathname to the directory of downloaded clinical data.
        csvout (str): path to the CSV file of selected lesions.
    
    Returns:
        Pandas DataFrame of selected lesion, merging both lesion-level and screening timepoint-level selection criteria.
    """
    ########################################
    ##### APPLY LESION LEVEL CRITERIA ######
    ########################################
    
    # CSV Clinical Datasets
    ctab_csv = os.path.join(datadircsv,'nlst_780_ctab_idc_20210527.csv') #Spiral CT Abnormalities dataset
    ctabc_csv = os.path.join(datadircsv,'nlst_780_ctabc_idc_20210527.csv') #Spiral CT Comparison Read Abnormalities dataset
    screen_csv = os.path.join(datadircsv,'nlst_780_screen_idc_20210527.csv') #Spiral CT Screening dataset
    prsn_csv = os.path.join(datadircsv,'nlst_780_prsn_idc_20210527.csv') #Participant dataset
    
    # Read CSVs as Pandas DataFrames
    dfab = pd.read_csv(ctab_csv)
    dfabc = pd.read_csv(ctabc_csv)
    dfscreen = pd.read_csv(screen_csv)
    dfprsn = pd.read_csv(prsn_csv)
    # Merge Spiral CT Abnormalities and Spiral CT Comparison Read Abnormalities datasets
    dfabmerge = dfab.merge(dfabc, how='outer') #combine

    # Select for abnormalities that included a marked CT slice number at study_yr 1 or at study_yr 2.
    dfmarkedslice = dfabmerge.dropna(subset=['sct_slice_num'])
    dfmarkedslicenew = dfmarkedslice[dfmarkedslice.study_yr==1][dfmarkedslice.study_yr==2]
    
    # Include only findings "preexist == no" i.e. those marked as new on comparison read
    dfmarkedslice_preexistno = dfmarkedslicenew[dfmarkedslicenew.sct_ab_preexist==1] #preexist no
    
    # Include only diagnostic-quality scans
    dfscreendx = dfscreen[dfscreen.ctdxqual==1].drop_duplicates(subset=['pid', 'study_yr'])
    dfmarkedslice_preexistno_dx = dfmarkedslice_preexistno.merge(dfscreendx)
    
    ##############################################################
    ####### APPLY CRITERIA FOR SCREENING TIMEPOINT RESULTS #######
    ##############################################################
    
    # Participant dataset includes results for the screening timeline. This does not break down results for individual lesions 
    # Include screening timepoints whose chanes are suspicious for malignancy at study_yr 1 or study_yr 2
    dfpos_changesus = dfprsn[dfprsn.scr_res1==4][dfprsn.scr_res2==4]
    
    ##################################################################################
    ####### INTERSECTION BETWEEN LESION-LEVEL AND SCREENING TIMEPPOINT CRITERIA ######
    ##################################################################################
    
    dfintersect = dfpos_changesus.merge(dfmarkedslice_preexistno_dx)
    
    # Save
    dfmarkedslice_preexistno_dx.sort_values(by=['pid', 'study_yr']).to_csv('dfmarkedslice_preexistno_dx.csv', index=False)
    dfintersect.sort_values(by=['pid', 'study_yr']).to_csv(csvout, index=False)
    
    return dfintersect

if __name__ == "__main__":
    datadir = 'nlstclinicaldata-download/'
    csvsavepath = 'nlstselectednewlesions.csv'
    applyselectioncriteria(datadir, csvsavepath)