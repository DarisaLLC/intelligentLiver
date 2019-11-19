#------------------------------------------------------------------------------------------------------
#
#   Project - itk processing
#   Description:
#       A python processing package using itk format
#   Author: huiliu.liu@gmail.com
#   Created 2019-09-18
#------------------------------------------------------------------------------------------------------

import os
import json

import numpy as np
import SimpleITK as sitk

from itk_template import MNI152_PD_AAL_MASK_ISO2MM_NII_FILE
from itk_template import MNI152_BS_AAL_MASK_ISO2MM_NII_FILE, MNI152_BS_AAL_MASK_ISO2MM_JSON_FILE
#----------------------------------------------------------------------------------------
#
def get_pd_aal_labels():
    """
    :return:
    """
    label_names = ['Precentral_L', 'Precentral_R', 'Supp_Motor_Area_L', 'Supp_Motor_Area_R',
                   'Caudate_L', 'Caudate_R', 'Putamen_L', 'Putamen_R', 'Pallidum_L',
                   'Pallidum_R', 'Thalamus_L', 'Thalamus_R', 'Cerebelum_Crus1_L',
                   'Cerebelum_Crus1_R', 'Cerebelum_Crus2_L', 'Cerebelum_Crus2_R',
                   'Cerebelum_3_L', 'Cerebelum_3_R', 'Cerebelum_4_5_L', 'Cerebelum_4_5_R',
                   'Cerebelum_6_L', 'Cerebelum_6_R', 'Cerebelum_7b_L', 'Cerebelum_7b_R',
                   'Cerebelum_8_L', 'Cerebelum_8_R', 'Cerebelum_9_L', 'Cerebelum_9_R',
                   'Cerebelum_10_L', 'Cerebelum_10_R']
    label_ids = [2001, 2002, 2401, 2402, 7001, 7002, 7011, 7012, 7021, 7022, 7101,
                 7102, 9001, 9002, 9011, 9012, 9021, 9022, 9031, 9032, 9041, 9042,
                 9051, 9052, 9061, 9062, 9071, 9072, 9081, 9082]
    return sitk.ReadImage(MNI152_PD_AAL_MASK_ISO2MM_NII_FILE), label_ids, label_names
#----------------------------------------------------------------------------------------
#
def get_values_from_aal_labels(sitk_image, sitk_label, label_ids):
    """
    :param sitk_image:
    :param sitk_label:
    :param label_ids:
    :return:
    """
    np_label = sitk.GetArrayFromImage(sitk_label)
    np_image = sitk.GetArrayFromImage(sitk_image)
    means = []
    maxs = []
    for label_id in label_ids:
        if np_image[np_label==label_id] != []:
            means.append(np.mean(np_image[np_label==label_id]))
            maxs.append(np.max(np_image[np_label==label_id]))
        else:
            means.append('NA')
            maxs.append('NA')
    return means, maxs
#---------------------------------------------------------------------------------------
#
def batch_get_pd_aal_values(sitk_image_files):
    """
    :param sitk_image_files:
    :return:
    """
    mmm = {}
    sitk_label, label_ids, label_names = get_pd_aal_labels()
    for label_name in label_names:
        mmm[label_name + '_mean'] = []
        mmm[label_name + '_max'] = []
    for file in sitk_image_files:
        sitk_image = sitk.ReadImage(file)
        means, maxs = get_values_from_aal_labels(sitk_image, sitk_label, label_ids)
        for label_name, mean_s, max_s in zip(label_names, means, maxs):
            mmm[label_name + '_mean'].append(mean_s)
            mmm[label_name + '_max'].append(max_s)
    return mmm
#----------------------------------------------------------------------------------------
#
def batch_get_aal_values(nii_files,
                         aal_nii_file=MNI152_BS_AAL_MASK_ISO2MM_NII_FILE,
                         aal_json_file=MNI152_BS_AAL_MASK_ISO2MM_JSON_FILE):
    """
    :param nii_files:
    :param aal_nii_file:
    :param aal_json_file:
    :return:
    """
    sitk_label = sitk.ReadImage(aal_nii_file)
    with open(aal_json_file, mode='r', encoding='utf-8') as f_json:
        aal_labels = json.load(f_json)
    label_ids = []
    label_names = []
    for aal_label in aal_labels:
        label_ids.append(aal_label['Label_ID'])
        label_names.append(aal_label['Label_Name'])
    mmm = {}
    for label_name in label_names:
        mmm[label_name + '_max'] = []
    for nii_file in nii_files:
        sitk_image = sitk.ReadImage(nii_file)
        means, max_vs = get_values_from_aal_labels(sitk_image, sitk_label, label_ids)
        for label_name, max_v in zip(label_names, max_vs):
            mmm[label_name + '_max'].append(max_v)
    return mmm