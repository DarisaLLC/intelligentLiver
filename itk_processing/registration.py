#------------------------------------------------------------------------------------------------------
#
#   Project - itk processing
#   Description:
#       A python processing package using itk format
#   Author: huiliu.liu@gmail.com
#   Created 2019-09-17
#------------------------------------------------------------------------------------------------------

import os
import subprocess

import SimpleITK as sitk

#------------------------------------------------------------------------------------------------------
# requiring the flirt
def registration_flirt(reference_nii_file, in_nii_file, out_nii_file):
    """
    :param reference_nii_file:
    :param in_nii_file:
    :param out_nii_file:
    :return:
    """
    # alignment
    subprocess.call(['flirt',
                     '-in', in_nii_file,
                     '-out', out_nii_file,
                     '-ref', reference_nii_file,
                     '-bins', '64',
                     '-dof', '6'])
    # non-rigid registration
    subprocess.call(['flirt',
                     '-in', out_nii_file,
                     '-out', out_nii_file,
                     '-ref', reference_nii_file,
                     '-bins', '256',
                     '-dof', '12'])
    return
