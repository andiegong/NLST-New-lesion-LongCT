import os

def abbrev_fname(filename, keepext=False):
    """
    Given a default DICOM file name (default upon download from the TCIA NLST collection: https://doi.org/10.7937/TCIA.HMQ8-J677) return an abbreviated file name that includes includes the includes the first and last 5 digits of the DICOM file names, which matches the last 5 digits of the scan's SeriesInstanceUID and an integeter than indicates the CT reconstruction.
    e.g.
    2.000000-0OPASEVZOOMB50f280212080.040.0null-18239, where '18239' are the last 5 digits of the scan's SeriesInstanceUID. The filename is abbreviated to
    2-18239
    
    Args:
        filename (str): input filename, with or without file extension
        keepext (bool, optional): Keep or remove original file extension, if available in the input filename, default False will remove the extension.
    Returns:
        A string containting the abbreviated filename.
    """
    
    # Manage the file extension in the output
    fname,ext = os.path.splitext(fname)
    
    pieces = fname.split('-')
    last5_SeriesInstanceUID = pieces[-1]
    reconstruction_integer_label = pieces[0].split('.')[0]
    fname_abb = '-'.join([reconstruction_integer_label, last5_SeriesInstanceUID])
    
    if keepext:
        fname_abb =+ ext
    
    return fname_abb