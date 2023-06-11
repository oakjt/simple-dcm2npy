This is a short Jupyter notebook which reads dcm files and extracts CT image data into a npy file.

To use it set the INPUT_ROOT_DIR to the root directory containing all of the scan directories (e.g. LUNG1-001_20180209_CT). Each scan directory should contain dcm files relevant to that scan.

Keep in mind that the DICOM file contains a lot of additional information about the scan, the script only extracts the image data.

The notebook was tested on [precision-medicine-toolbox](https://github.com/primakov/precision-medicine-toolbox). The root folder was set to
`precision-medicine-toolbox/data/dcms`

Motivation for the notebook is [Mr. P Solver's "Python Image Segmentation Tutorial (2022)"](https://youtu.be/UIgaLDgb2fY) which lacked the original CT scan files.
