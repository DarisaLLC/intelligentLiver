#------------------------------------------------------------------------------------------------------
#
#   Project - itk processing
#   Description:
#       A python processing package using itk format
#   Author: huiliu.liu@gmail.com
#   Created 2019-09-17
#------------------------------------------------------------------------------------------------------

import numpy as np
import SimpleITK as sitk

#------------------------------------------------------------------------------------------------------
# resample sitk_image to referenced sitk_image
def resample_sitk_image_by_reference(reference, sitk_image):
    """
    :param reference:
    :param sitk_image:
    :return:
    """
    resampler = sitk.ResampleImageFilter()
    resampler.SetInterpolator(sitk.sitkNearestNeighbor)
    resampler.SetReferenceImage(reference)
    return resampler.Execute(sitk_image)
