#------------------------------------------------------------------------------------------------------
#
#   Project - itk processing
#   Description:
#       A python processing package using itk format
#   Author: huiliu.liu@gmail.com
#   Created 2019-09-18
#------------------------------------------------------------------------------------------------------

import os

import numpy as np
import SimpleITK as sitk

#------------------------------------------------------------------------------------------------------
#
def sitk_divide(sitk_dividend, sitk_divider):
    """
    :param sitk_dividend:
    :param sitk_divider:
    :return:
    """
    origin = sitk_dividend.GetOrigin()
    spacing = sitk_dividend.GetSpacing()
    direction = sitk_dividend.GetDirection()

    np_dividend = sitk.GetArrayFromImage(sitk_dividend)
    np_divider = sitk.GetArrayFromImage(sitk_divider)
    np_result = np.true_divide(np_dividend, np_divider)
    sitk_result = sitk.GetImageFromArray(np_result)
    sitk_result.SetOrigin(origin)
    sitk_result.SetSpacing(spacing)
    sitk_result.SetDirection(direction)
    return sitk_result
