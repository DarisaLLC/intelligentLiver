#------------------------------------------------------------------------------------------------------
#
#   Project - itk processing
#   Description:
#       A python processing package using itk format
#   Author: huiliu.liu@gmail.com
#   Created 2019-09-16
#------------------------------------------------------------------------------------------------------

import os

import numpy as np
import SimpleITK as sitk

#------------------------------------------------------------------------------------------------------
#
def reset_spatial_origin(template_nii_file, nii_files):
    """
    :param template_nii_file:
    :param nii_files:
    :return:
    """
    sitk_template = sitk.ReadImage(template_nii_file)
    sitk_origin = sitk_template.GetOrigin()
    for nii_file in nii_files:
        sitk_image = sitk.ReadImage(nii_file)
        sitk_image.SetOrigin(sitk_origin)
        sitk.WriteImage(sitk_image, nii_file)
    return