#------------------------------------------------------------------------------------------------------
#
#   Project - SXHX Hospital
#   Description:
#       Collections of Projects for SXHX Hospital
#   Author: huiliu.liu@gmail.com
#   Created 2020-01-04
#------------------------------------------------------------------------------------------------------

import os
import re
import shutil
import pydicom
import pandas as pd

from hi_projects.schx_hospital.config import dcm_anno_root, dcm_anno_root_tmp
from hi_projects.schx_hospital.config import liver_mr_seq
from hi_projects.schx_hospital.config import dicom_annotation_key as dak
from hi_pydicom.utils import read_patient_info, read_series_info
from hi_pydicom.utils import get_dcm_files, read_timing, read_series_offset_seconds
from hi_pydicom.utils import get_series_files_by_series_uid
from hi_pydicom.tags import TagEchoNumber, TagInstanceNumber

#------------------------------------------------------------------------------------------------------
#
def _copy_dicoms_unique_suid(to_dicom_root, rules):
    """
    :param to_dicom_root:
    :param rules:
    :return: number of slices
    """
    if not rules['valid']: return 0
    series_root = os.path.join(to_dicom_root, rules[dak.sub_code],
                               str(rules[dak.study_datetime]), rules[dak.series_anno_hl])
    os.makedirs(series_root, exist_ok=True)
    dcm_files = get_series_files_by_series_uid(rules[dak.series_dcm_root_from_hy], rules[dak.series_uid])
    for _dcm_file in dcm_files:
        _ds = pydicom.read_file(_dcm_file, stop_before_pixels=True, force=True)
        dcm_file = os.path.join(series_root, '{:06d}.dcm'.format(int(_ds[TagInstanceNumber].value)))
        shutil.copyfile(_dcm_file, dcm_file)
    return len(dcm_files)
#------------------------------------------------------------------------------------------------------
#
def _copy_dicoms_multicomponents(to_dicom_root, rules, components_tag, components_value, components_label):
    """
    :param to_dicom_root:
    :param rules:
    :param components_tag:
    :param components_label:
    :return: {label: number of slices, ...}
    """
    if not rules['valid']: return 0
    series_root = os.path.join(to_dicom_root, rules[dak.sub_code],
                               str(rules[dak.study_datetime]), components_label)
    os.makedirs(series_root, exist_ok=True)
    dcm_files = get_series_files_by_series_uid(rules[dak.series_dcm_root_from_hy], rules[dak.series_uid],
                                               tags=[components_tag], tag_values=[components_value])
    for _dcm_file in dcm_files:
        _ds = pydicom.read_file(_dcm_file, stop_before_pixels=True, force=True)
        dcm_file = os.path.join(series_root, '{:06d}.dcm'.format(int(_ds[TagInstanceNumber].value)))
        shutil.copyfile(_dcm_file, dcm_file)
    return len(dcm_files)

#------------------------------------------------------------------------------------------------------
#
def _create_inopp_phase_rules(df_row):
    """
    :param df_row:
    :return:
    """
    rules = {dak.sub_code: df_row[dak.sub_code],
             dak.study_datetime: df_row[dak.study_datetime],
             dak.series_anno_hl: df_row[dak.series_anno_hl],
             dak.series_dcm_root_from_hy: df_row[dak.series_dcm_root_from_hy],
             dak.series_uid: df_row[dak.series_uid],
             'valid': False}
    if 'fl2d2' in df_row[dak.sequence_name]: rules['valid'] = True
    return rules
#------------------------------------------------------------------------------------------------------
#
def copy_inopp_phase_dicom(to_dicom_root, anno_xlsx_file):
    """
    :param to_dicom_root:
    :param anno_xlsx_file:
    :return:
    """
    summary = {'sub_code': [], 'nb_in_phase': [], 'nb_opp_phase': []}
    df = pd.read_excel(anno_xlsx_file)
    total_counts = df.count()[dak.sub_code]
    for _i in range(total_counts):
        _df_row = df.iloc[_i]
        _rules = _create_inopp_phase_rules(_df_row)
        if _rules['valid'] == False: continue
        nb_slices_in = _copy_dicoms_multicomponents(to_dicom_root, _rules, TagEchoNumber, '2', 'in-phase')
        nb_slices_opp = _copy_dicoms_multicomponents(to_dicom_root, _rules, TagEchoNumber, '1', 'opp-phase')
        print('copying %s: %s - %s' % (_df_row[dak.sub_code], nb_slices_in, nb_slices_opp))
        summary['sub_code'].append(_df_row[dak.sub_code])
        summary['nb_in_phase'].append(nb_slices_in)
        summary['nb_opp_phase'].append(nb_slices_opp)
    return pd.DataFrame(summary)

#------------------------------------------------------------------------------------------------------
#
def _create_t2w_rules(df_row):
    """
    :param df_row:
    :return:
    """
    rules = {dak.sub_code: df_row[dak.sub_code],
             dak.study_datetime: df_row[dak.study_datetime],
             dak.series_anno_hl: df_row[dak.series_anno_hl],
             dak.series_dcm_root_from_hy: df_row[dak.series_dcm_root_from_hy],
             dak.series_uid: df_row[dak.series_uid],
             'valid': False}
    _valids = ('tse2d' in df_row[dak.sequence_name],
               't2w' in df_row[dak.series_anno_hl])
    if all(_valids): rules['valid'] = True
    return rules
#------------------------------------------------------------------------------------------------------
#
def copy_t2w_dicom(to_dicom_root, anno_xlsx_file):
    """
    :param to_dicom_root:
    :param anno_xlsx_file:
    :return:
    """
    summary = {'sub_code': [], 'nb_t2w': []}
    df = pd.read_excel(anno_xlsx_file)
    total_counts = df.count()[dak.sub_code]
    for _i in range(total_counts):
        _df_row = df.iloc[_i]
        _rules = _create_t2w_rules(_df_row)
        if _rules['valid'] == False: continue
        nb_slices = _copy_dicoms_unique_suid(to_dicom_root, _rules)
        print('copying %s: %s' % (_df_row[dak.sub_code], nb_slices))
        summary['sub_code'].append(_df_row[dak.sub_code])
        summary['nb_t2w'].append(nb_slices)
    return pd.DataFrame(summary)

#------------------------------------------------------------------------------------------------------
#
# TEST ENTRY
#
#------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    dcm_root_origin = 'F:\\Huaxi_Liver\\01_data'
    anno_xlsx_file = os.path.join(dcm_root_origin, 'participants_dcm_11.xlsx')

    # in-opp-phase
    #df = copy_inopp_phase_dicom(dcm_anno_root, anno_xlsx_file)
    #df.to_excel(os.path.join(dcm_anno_root, 'in-opp-phase.xlsx'))

    # t2w
    #df = copy_t2w_dicom(dcm_anno_root, anno_xlsx_file)
    #df.to_excel(os.path.join(dcm_anno_root, 't2w.xlsx'))

    #