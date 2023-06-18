# Simple DICOM to NumPy

This short script reads dcm files and extracts CT or MR image data into a npy file. For any serious applications please visit [precision-medicine-toolbox [1]](https://github.com/primakov/precision-medicine-toolbox).

### Usage
Specify the input directory with `-i` flag. This directory contains individual dcm scan files. Alternatively specify the `-ird` flag which contains multiple directories each representing one scan. Each scan directory is mapped to one npy file.

### Limitations
This script is limited in functionality and should only be used in educational purposes. Keep in mind that the DICOM file contains a lot of additional information about the scan, the script only extracts the image data. Also pay attention to the datatype. The scan may contain data in form of unsigned integers while the real world measurement values can be negative. Such case will require additional processing.

### External resources
The script was tested on [[1]](https://github.com/primakov/precision-medicine-toolbox). The root folder was set to `precision-medicine-toolbox/data/dcms`. For full functionality please visit [[1]](https://github.com/primakov/precision-medicine-toolbox). 

Motivation for this script is [Mr. P Solver's "Python Image Segmentation Tutorial (2022)"](https://youtu.be/UIgaLDgb2fY) which lacked the original CT scan files.

### References
<a id="1">[1]</a>
Precision-medicine-toolbox: An open-source python package for facilitation of quantitative medical imaging and radiomics analysis;
Sergey Primakov and Elizaveta Lavrova and Zohaib Salahuddin and Henry C Woodruff and Philippe Lambin;
2022;
2202.13965;
arXiv