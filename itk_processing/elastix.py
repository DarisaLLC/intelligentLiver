#------------------------------------------------------------------------------------------------------
#
#   Project - itk processing
#   Description:
#       A python processing package using itk format
#   Author: huiliu.liu@gmail.com
#   Created 2019-09-20
#------------------------------------------------------------------------------------------------------

import os
import sys
import shutil
import subprocess

import SimpleITK as sitk

from glob import glob

ELASTIX_BIN_ROOT = os.path.join(os.path.dirname(__file__), 'elastix', 'bin')
ELASTIX_DB_ROOT = os.path.join(os.path.dirname(__file__), 'elastix', 'parsdb')

#------------------------------------------------------------------------------------------------------
#
def get_elastix_bin():
    """
    :return:
    """
    if sys.platform == 'win32': elastix_bin = os.path.join(ELASTIX_BIN_ROOT, 'elastix.exe')
    elif sys.platform == 'linux': elastix_bin = os.path.join(ELASTIX_BIN_ROOT, 'elastix')
    elif sys.platform == 'macos': elastix_bin = os.path.join(ELASTIX_BIN_ROOT, 'elastix')
    else: elastix_bin = ''
    return elastix_bin
#------------------------------------------------------------------------------------------------------
#
def get_transformix_bin():
    """
    :return:
    """
    if sys.platform == 'win32': transformix_bin = os.path.join(ELASTIX_BIN_ROOT, 'transformix.exe')
    elif sys.platform == 'linux': transformix_bin = os.path.join(ELASTIX_BIN_ROOT, 'transformix')
    elif sys.platform == 'macos': transformix_bin = os.path.join(ELASTIX_BIN_ROOT, 'transformix')
    else: transformix_bin = ''
    return transformix_bin
#-----------------------------------------------------------------------------------------------------
#
# parameter database
#
#-----------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------
#
def registration_par0000affine_brain(ref_nii_file, in_nii_file, out_nii_file):
    """
    :param ref_nii_file:
    :param in_nii_file:
    :param out_nii_file:
    :return:
    """
    outdir = os.path.dirname(out_nii_file)
    out_filename = os.path.basename(out_nii_file)
    par0000_file = os.path.join(ELASTIX_DB_ROOT, 'par0000affine.txt')
    devnull = open(os.devnull, 'w')
    subprocess.call([get_elastix_bin(),
                     '-f', ref_nii_file,
                     '-m', in_nii_file,
                     '-p', par0000_file,
                     '-out', outdir],
                    stdout=devnull, stderr=subprocess.STDOUT)

    # update filename
    result_mdh_file = os.path.join(outdir, 'result.0.mhd')
    if os.path.exists(result_mdh_file):
        sitk_image = sitk.ReadImage(result_mdh_file)
        sitk.WriteImage(sitk_image, os.path.join(outdir, out_filename))

    # remove tmp files
    tmp_files = glob(os.path.join(outdir, 'IterationInfo.*'))
    tmp_files += glob(os.path.join(outdir, 'result.*'))
    tmp_files += glob(os.path.join(outdir, 'TransformParameters.*'))
    for tmp_file in tmp_files: os.remove(tmp_file)
    return
#-----------------------------------------------------------------------------------------------------
#
def registration_par0000bspline_brain(ref_nii_file, in_nii_file, out_nii_file):
    """
    :param ref_nii_file:
    :param in_nii_file:
    :param out_nii_file:
    :return:
    """
    outdir = os.path.dirname(out_nii_file)
    out_filename = os.path.basename(out_nii_file)
    par0000_file = os.path.join(ELASTIX_DB_ROOT, 'par0000bspline.txt')
    devnull = open(os.devnull, 'w')
    subprocess.call([get_elastix_bin(),
                     '-f', ref_nii_file,
                     '-m', in_nii_file,
                     '-p', par0000_file,
                     '-out', outdir],
                    stdout=devnull, stderr=subprocess.STDOUT)

    # update filename
    result_mdh_file = os.path.join(outdir, 'result.0.mhd')
    if os.path.exists(result_mdh_file):
        sitk_image = sitk.ReadImage(result_mdh_file)
        sitk.WriteImage(sitk_image, os.path.join(outdir, out_filename))

    # remove tmp files
    tmp_files = glob(os.path.join(outdir, 'IterationInfo.*'))
    tmp_files += glob(os.path.join(outdir, 'result.*'))
    tmp_files += glob(os.path.join(outdir, 'TransformParameters.*'))
    for tmp_file in tmp_files: os.remove(tmp_file)
    return




