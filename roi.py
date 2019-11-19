import os
from glob import glob
import gzip
import shutil
import SimpleITK as sitk

# ----------------------------------------------------------------------------------------------------
#
def parse_roi_nii_file(nii_file):
    """
    :param nii_file:
    :return:
    """
    nii_filename = os.path.basename(nii_file)
    sub_roi_name = nii_filename.split('_')[0]
    sub_roi_names = sub_roi_name.split('-')
    sub_name = 'sub-{:03d}'.format(int(sub_roi_names[0]))
    if len(sub_roi_names) == 3:
        roi_name = 'roi-{:02d}'.format(int(sub_roi_names[1]))
    else:
        roi_name = 'roi-{:02d}'.format(1)
    return sub_name, roi_name


# ----------------------------------------------------------------------------------------------------
#
if __name__ == '__main__':
    src_root = 'F:\\huaxi\\Liver-EOB-NII-ROI\\ROI-EOB'
    target_root = 'F:\\huaxi\\Liver-EOB-NII-ROI\\organized'
    nii_files = glob(os.path.join(src_root, '*HBP_Merge.nii'))
    print(len(nii_files))
    for nii_file in nii_files:
        sub_name, roi_name = parse_roi_nii_file(nii_file)
        #print(sub_name)
        sub_root = os.path.join(target_root, sub_name)
        os.makedirs(sub_root, exist_ok=True)
        roi_nii_file = os.path.join(sub_root, sub_name + '_' +  roi_name + '_HBP.nii.gz')
        sitk_roi= sitk.ReadImage(nii_file)
        sitk.WriteImage(sitk_roi, roi_nii_file)