#------------------------------------------------------------------------------------------------------
#
#   Project - itk processing
#   Description:
#       A python processing package using itk format
#   Author: huiliu.liu@gmail.com
#   Created 2019-09-17
#------------------------------------------------------------------------------------------------------

import os

import numpy as np
import SimpleITK as sitk

#------------------------------------------------------------------------------------------------------
#
def z_score(sitk_image, sitk_mask=None, threshold_prob = 0.01):
    """
    :param sitk_image:
    :param sitk_mask:       if sitk_mask is None, > 1% is used
    :return:
    """
    np_image = sitk.GetArrayFromImage(sitk_image)
    if sitk_mask is not None:
        np_mask = sitk.GetArrayFromImage(sitk_mask)
        np_idx = np_mask > 0
    else:
        np_max = np.max(np_image)
        np_min = np.min(np_image)
        np_threshold = np_min + threshold_prob * (np_max - np_min)
        np_idx = np_image > np_threshold
    np_mean = np.mean(np_image[np_idx])
    np_std = np.std(np_image[np_idx])
    np_zscore = (np_image - np_mean) / np_std
    sitk_score = sitk.GetImageFromArray(np_zscore)
    sitk_score.SetOrigin(sitk_image.GetOrigin())
    sitk_score.SetSpacing(sitk_image.GetSpacing())
    sitk_score.SetDirection(sitk_image.GetDirection())
    return sitk_score, np_mean, np_std
#------------------------------------------------------------------------------------------------------
#
def scale_normal(sitk_image):
    """
    :param sitk_image:
    :return:
    """
    np_image = sitk.GetArrayFromImage(sitk_image)

    np_max = np.max(np_image)
    np_std = np.std(np_image)
    np_normal = np_image / np_max
    sitk_normal = sitk.GetImageFromArray(np_normal)
    sitk_normal.SetOrigin(sitk_image.GetOrigin())
    sitk_normal.SetSpacing(sitk_image.GetSpacing())
    sitk_normal.SetDirection(sitk_image.GetDirection())
    return sitk_normal, np_max, np_std
#------------------------------------------------------------------------------------------------------
#
def scale_by_mean(sitk_image):
    """
    :param sitk_image:
    :return:
    """
    np_image = sitk.GetArrayFromImage(sitk_image)

    np_mean = np.mean(np_image)
    np_normal = np_image / np_mean
    np_std = np.std(np_image)
    sitk_normal = sitk.GetImageFromArray(np_normal)
    sitk_normal.SetOrigin(sitk_image.GetOrigin())
    sitk_normal.SetSpacing(sitk_image.GetSpacing())
    sitk_normal.SetDirection(sitk_image.GetDirection())
    return sitk_normal, np_mean, np_std