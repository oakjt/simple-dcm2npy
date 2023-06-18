import os, argparse
import numpy as np
import pydicom

parser = argparse.ArgumentParser(
            prog="dcm2npy",
            description="Script for converting DICOM files into NumPy arrays. Specify the root directory of multiple scan directories or directory of an individual scan."
            )
in_group = parser.add_mutually_exclusive_group(required=True)
in_group.add_argument("-i", "--input_dir",
                    help="The directory containing DICOM files.")
in_group.add_argument("-ird", "--input_root_dir",
                    help="The root directory containing scan directories.")
parser.add_argument("-o", "--output_dir",
                    required=True,
                    help="Output directory for resulting npy files.")
args = parser.parse_args()

if args.input_root_dir:
    # Scan all directories in root
    input_dir = args.input_root_dir
    _, dirs, _ = next(os.walk(input_dir))
else:
    # Take only one directory
    input_dir = args.input_dir
    input_dir, dirs = os.path.split(input_dir)
    dirs = [dirs]
output_dir = args.output_dir

for cur_dir in dirs:
    cur_dir_full = f"{input_dir}/{cur_dir}"
    # List all files in current dir
    _, _, files = next(os.walk(cur_dir_full))
    # Take only .dcm files
    files = filter(lambda f: f.split(".")[1] == "dcm", files)
    # Sort by file number
    dicoms = sorted(files)

    np_list = []
    for dicom in dicoms:
        dicom = pydicom.read_file(f"{cur_dir_full}/" + dicom)
        # Check whether the file contains image data we're interested in
        repval = dicom[(0x0008, 0x0016)].repval
        if repval == "CT Image Storage" or repval == "MR Image Storage":
            np_pixel_array = dicom.pixel_array
            np_list.append(np_pixel_array)

    # Write as NumPy array
    if np_list:
        npy = np.array(np_list)
        os.makedirs(output_dir, exist_ok=True)
        np.save(f"{output_dir}/{cur_dir}.npy", npy)
        print(f"Written {cur_dir}.npy")