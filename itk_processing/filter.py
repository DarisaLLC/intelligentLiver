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
def gaussian_filtering(sitk_image, kernel_size):
    """
    :param sitk_image:
    :param kernel_size:
    :return:
    """

    return