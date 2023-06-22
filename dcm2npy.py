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
    dicoms = sorted(files, key=lambda f: int(f.split(".")[0]))

    np_list = []
    details = []
    for dicom_filename in dicoms:
        with pydicom.dcmread(f"{cur_dir_full}/{dicom_filename}") as dcm:
            # Check whether the file contains image data we're interested in
            repval = dcm["SOPClassUID"].repval
            if repval in ["CT Image Storage", "MR Image Storage"]:
                if not details:
                    details = dcm["SliceThickness"], dcm["WindowCenter"], dcm["WindowWidth"]
                pix = dcm.pixel_array
                # Convert to Hounsfield units
                pix = pydicom.pixel_data_handlers.util.apply_modality_lut(pix, dcm)
                # np.can_cast() is very slow, manually check casting options
                if np.max(pix) <= np.iinfo("int16").max and np.min(pix) >= np.iinfo("int16").min:
                    pix = np.array(pix, dtype="int16")
                np_list.append(pix)

    # Write as NumPy array
    if np_list:
        npy = np.array(np_list)
        os.makedirs(output_dir, exist_ok=True)
        np.save(f"{output_dir}/{cur_dir}.npy", npy)
        print(f"Written {cur_dir}.npy")
        if details:
            print(f"Additional details from last slice: {details=}")