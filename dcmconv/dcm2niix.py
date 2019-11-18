#------------------------------------------------------------------------------------------------------
#
#   Project - dicom convert
#   Description:
#       A python processing package for　converting dicom into nifti, png, jpg format
#   Author: huiliu.liu@gmail.com
#   Created 2019-11-17
#------------------------------------------------------------------------------------------------------

import os
import sys
import subprocess

DCM2NIIX_ROOT = os.path.join(os.path.dirname(__file__), 'dcm2niix')

#-----------------------------------------------------------------------------------------------------
#
def get_dcm2niix_bin():
    """
    :return:
    """
    if sys.platform == 'win32': dcm2niix_bin = os.path.join(DCM2NIIX_ROOT, 'dcm2niix_win.exe')
    elif sys.platform == 'linux': dcm2niix_bin = os.path.join(DCM2NIIX_ROOT, 'dcm2niix_lnx')
    elif sys.platform == 'macos': dcm2niix_bin = os.path.join(DCM2NIIX_ROOT, 'dcm2niix_mac')
    else: dcm2niix_bin = ''
    return dcm2niix_bin
#-----------------------------------------------------------------------------------------------------
#
def conv_series2nii(dcm_series_root, nii_rootname, nii_filename, zipped=True):
    """
    :param dcm_series_root:
    :param nii_rootname:
    :param nii_filename:
    :param zipped:
    :return:
    """

    dcm2niix_bin = get_dcm2niix_bin()
    if dcm2niix_bin == '': raise ValueError('there is no dcm2niix exist.')
    zip_y = 'y'
    if not zipped: zip_y = 'n'

    devnull = open(os.devnull, 'w')
    subprocess.call([dcm2niix_bin, '-b', 'y', '-z', zip_y,
                     '-f', nii_filename,
                     '-o', nii_rootname,
                     '-w', '1',
                     dcm_series_root],
                    stdout=devnull, stderr=subprocess.STDOUT)

    return
