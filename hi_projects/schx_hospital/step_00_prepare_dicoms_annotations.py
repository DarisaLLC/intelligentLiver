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
import pydicom
import pandas as pd

from hi_projects.schx_hospital.config import liver_mr_seq
from hi_projects.schx_hospital.config import dicom_annotation_key as dak
from hi_pydicom.utils import read_patient_info, read_series_info
from hi_pydicom.utils import get_dcm_files, read_timing, read_series_offset_seconds
from hi_pydicom.utils import get_series_1th_file

#------------------------------------------------------------------------------------------------------
#
def _parser_patient_anno_code(dcm_patient_anno_code_from_hanyu):
    """
    :param dcm_patient_anno_code_from_hanyu:
    :return:
    """
    sub_d = re.findall('\d*\d+', dcm_patient_anno_code_from_hanyu)
    if len(sub_d) < 1: return dcm_patient_anno_code_from_hanyu
    sub_code = 'sub-{:03d}'.format(int(sub_d[0]))
    sub_id = 'id-' + str(sub_d[1])
    sub_s = re.findall('[0-9][a-z ]+[0-9]', dcm_patient_anno_code_from_hanyu)
    if len(sub_s) < 1: return dcm_patient_anno_code_from_hanyu
    sub_name = sub_s[0][2:-2]
    sub_c = re.findall('-.*', dcm_patient_anno_code_from_hanyu)
    if len(sub_c) < 1: sub_comment = 'no comments'
    else: sub_comment = str(sub_c[0][:].replace('-', ' '))
    return sub_name, sub_code, sub_id, sub_comment
#------------------------------------------------------------------------------------------------------
#
def _parser_series_anno_code(dcm_series_anno_code_from_hanyu):
    """
    :param dcm_series_code_from_hanyu:
    :return:
    """
    series_anno_code = dcm_series_anno_code_from_hanyu.replace(' ', '-')
    if len(re.findall('[pP][rR][eE]$', series_anno_code)) > 0: return liver_mr_seq.seq_name_pre
    if len(re.findall('[aA][pP]$', series_anno_code)) > 0: return liver_mr_seq.seq_name_ap
    if len(re.findall('[pP][vV][pP]$', series_anno_code)) > 0: return liver_mr_seq.seq_name_pvp
    if len(re.findall('[tT][pP]$', series_anno_code)) > 0: return liver_mr_seq.seq_name_tp
    if len(re.findall('[hH][bB][pP]$', series_anno_code)) > 0: return liver_mr_seq.seq_name_hbp
    if len(re.findall('[tT]2[wW]', series_anno_code)) > 0: return liver_mr_seq.seq_name_t2w
    if len(re.findall('[dD][wW][iI]$', series_anno_code)) > 0: return liver_mr_seq.seq_name_dwi
    if len(re.findall('[iI][nN]-[pP][hH][aA][sS][eE]$', series_anno_code)) > 0: return liver_mr_seq.seq_name_in_phase
    if len(re.findall('[oO][pP][pP]-[pP][hH][aA][sS][eE]$', series_anno_code)) > 0: return liver_mr_seq.seq_name_opp_phase
    if len(re.findall('[iI][nN][pP][hH][aA][sS][eE]$', series_anno_code)) > 0: return liver_mr_seq.seq_name_in_phase
    if len(re.findall('[oO][pP][pP][pP][hH][aA][sS][eE]$', series_anno_code)) > 0: return liver_mr_seq.seq_name_opp_phase
    return series_anno_code
#------------------------------------------------------------------------------------------------------
#
def _parser_merge_nii_anno_code(merge_anno_code_from_hanyu):
    """
    :param merge_anno_code_from_hanyu:
    :return:
    """
    if not merge_anno_code_from_hanyu.endswith('_Merge.nii'): return None
    sub_d = re.findall('\d*\d+', merge_anno_code_from_hanyu)
    if len(sub_d) < 1: print('failed to %s.' % (merge_anno_code_from_hanyu))
    sub_code = 'sub-{:03d}'.format(int(sub_d[0]))
    series_anno_code = merge_anno_code_from_hanyu.replace('_Merge.nii', '')
    series_anno_code = series_anno_code.replace(sub_d[0] + '-', '')
    series_anno_code = _parser_series_anno_code(series_anno_code)
    return series_anno_code
#------------------------------------------------------------------------------------------------------
#
def _parser_dcm_file(ds):
    """
    :param dcm_file:
    :return: patient_id, patient_name, series_id, series_description, seq_name,
             series_nb_slices, series_offset_time
    """
    patient_name, patient_id, _, _, _ = read_patient_info(ds)
    study_datetime, s_acq_datetime = read_timing(ds)
    s_uid, seq_name, s_description, s_id, s_slices = read_series_info(ds)
    series_offset_time = read_series_offset_seconds(ds)
    return patient_id, patient_name, study_datetime, s_acq_datetime, s_uid, seq_name, s_description, \
           s_id, series_offset_time
#------------------------------------------------------------------------------------------------------
#
def _parse_series(series_root):
    """
    :param series_root:
    :return:
    """
    series_info = {dak.patient_name: [], dak.patient_id: [],
                   dak.series_number: [], dak.series_description: [], dak.sequence_name: [],
                   dak.series_anno_hy: [], dak.series_anno_hl: [],
                   dak.series_nii_anno: [], dak.number_of_series_same_root: [],
                   dak.study_datetime: [], dak.series_acq_datetime: [], dak.series_offset_time: [],
                   dak.series_uid: [],
                   dak.series_dcm_root_from_hy: []}
    sub_series_root_names = os.listdir(series_root)
    for sub_series_root_name in sub_series_root_names:
        sub_series_root = os.path.join(series_root, sub_series_root_name)
        # find all dcm files within sub_series_root
        for sub_series_root_r, _, files in os.walk(sub_series_root):
            if len(files) <= 0: continue
            # parse merge file annotation code
            merge_code = 'no nii'
            for file in files:
                _merge_code = _parser_merge_nii_anno_code(file)
                if _merge_code != None:
                    merge_code = _merge_code
                    break
            dcm_files = get_dcm_files(sub_series_root_r)
            if len(dcm_files) <= 0: continue
            # parse series annotation code
            series_root_codes_from_hanyu = os.path.relpath(sub_series_root_r, series_root).split(os.path.sep)
            s_r_c_code = 'no annotation'
            for s_r_c_f_hy in series_root_codes_from_hanyu:
                _s_r_c_code = _parser_series_anno_code(s_r_c_f_hy)
                if _s_r_c_code != s_r_c_f_hy:
                    s_r_c_code = _s_r_c_code
                    break
            # parse dicom file
            suid_dict = get_series_1th_file(dcm_files)
            nb_series_in_same_root = len(suid_dict.keys())
            for suid in suid_dict.keys():
                # parser the dicom info from the first dicom information in the series root
                dcm_file = suid_dict.get(suid)
                ds = pydicom.read_file(dcm_file, stop_before_pixels=True, force=True)
                p_id, p_name, study_datetime, s_acq_datetime, s_uid, seq_name, s_description, \
                s_id, series_offset_time = _parser_dcm_file(ds)
                series_info[dak.patient_name].append(p_name)
                series_info[dak.patient_id].append(p_id)
                series_info[dak.dak.series_number].append(s_id)
                series_info[dak.series_description].append(s_description)
                series_info[dak.sequence_name].append(seq_name)
                series_info[dak.series_anno_hy].append(s_r_c_code)
                series_info[dak.series_anno_hl].append(s_r_c_code)
                series_info[dak.series_nii_anno].append(merge_code)
                series_info[dak.number_of_series_same_root].append(nb_series_in_same_root)
                series_info[dak.study_datetime].append(study_datetime)
                series_info[dak.series_acq_datetime].append(s_acq_datetime)
                series_info[dak.series_offset_time].append(series_offset_time)
                series_info[dak.series_uid].append(suid)
                series_info[dak.series_dcm_root_from_hy].append(sub_series_root_r)
    return series_info
#------------------------------------------------------------------------------------------------------
#
def parse_dcm_root(dcm_root_from_hanyu):
    """
    :param dcm_root_from_hanyu:
    :return:
    """
    dfs = []
    sub_root_names = os.listdir(dcm_root_from_hanyu)
    for i, sub_root_name in enumerate(sub_root_names):
        print('working on %s-th: %s'%(i + 1, sub_root_name))
        try:
            sub_df_i = {dak.sub_code: [], dak.sub_name: [], dak.sub_id: [], dak.sub_comment: []}
            sub_root = os.path.join(dcm_root_from_hanyu, sub_root_name)
            sub_name, sub_code, sub_id, sub_comment = _parser_patient_anno_code(sub_root_name)
            series_info = _parse_series(sub_root)
            sn = 0
            for series_key in series_info.keys():
                sub_df_i[series_key] = series_info[series_key]
                sn = len(series_info[series_key])
            sub_df_i[dak.sub_code] = [sub_code, ]*sn
            sub_df_i[dak.sub_name] = [sub_name, ]*sn
            sub_df_i[dak.sub_id] = [sub_id, ]*sn
            sub_df_i[dak.sub_comment] = [sub_comment, ]*sn
            df_i = pd.DataFrame(sub_df_i)
            dfs.append(df_i)
        except:
            print('... failed in reading %s'%(sub_code))
    df = pd.concat(dfs, axis=0)
    return df

#------------------------------------------------------------------------------------------------------
#
# TEST ENTRY
#
#------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    dcm_root_origin = 'F:\\Huaxi_Liver\\01_data\\Liver-EOB-DCM'
    df = parse_dcm_root(dcm_root_origin)
    df.to_excel(os.path.join(os.path.dirname(dcm_root_origin), 'participants_dcm_xx.xlsx'))