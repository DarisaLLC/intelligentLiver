import os
import numpy as np
import SimpleITK as sitk

from glob import glob
from PIL import Image

from itk_processing.resample import resample_sitk_image_by_reference
#-------------------------------------------------------------------------------------------
#
def save_nii_roi_png(nii_file, roi_nii_files, output_root):
    """
    :param nii_file:
    :param roi_nii_files:
    :return:
    """
    sitk_image = sitk.ReadImage(nii_file)
    np_image = sitk.GetArrayFromImage(sitk_image)
    np_image_shape = np_image.shape
    for roi_nii_file in roi_nii_files:
        sitk_roi = sitk.ReadImage(roi_nii_file)
        sitk_roi = resample_sitk_image_by_reference(sitk_image, sitk_roi)
        np_roi = sitk.GetArrayFromImage(sitk_roi)
        np_roi_xyz = np.transpose(np.nonzero(np_roi))
        try:
            z_idx = np_roi_xyz[0][0]
            np_image_z = np_image[z_idx, ::] + 100 * np_roi[z_idx, ::]
            roi_nii_filename = os.path.basename(roi_nii_file)
            png_file = os.path.join(output_root, roi_nii_filename.replace('.nii.gz', '.png'))
            im_r = np_image_z.astype(np.int)
            im_r = np.fliplr(im_r)
            im_r = np.flipud(im_r)
            im_r = (im_r - np.min(im_r)) / (np.max(im_r) - np.min(im_r))
            im = Image.fromarray((im_r * 255).astype(np.uint8))
            im.save(png_file)
        except:
            print('failed to print %s' % (roi_nii_file))

    return

nii_root = 'D:\\data\\demo\\Liver-EOB-NII'
roi_root = 'D:\\data\\demo\\Liver-EOB-NII-ROI'
png_root = 'D:\\data\\demo\\Liver-EOB-NII-JPG'
for sub_root, sub_dirs, files in os.walk(nii_root):
    sub_name = os.path.basename(sub_root)
    if not sub_name.startswith('sub-'): continue
    HBP_nii_file = os.path.join(sub_root, sub_name + '_HBP.nii.gz')
    if not os.path.exists(HBP_nii_file):
        print('failed to nii2jpn for %s.'%(sub_name))
        continue
    else: print('working on %s.'%(sub_name))
    roi_HBP_nii_files = glob(os.path.join(roi_root, str(int(sub_name[-3:])) + '-*-HBP_Merge.nii'))
    save_nii_roi_png(HBP_nii_file, roi_HBP_nii_files, png_root)
