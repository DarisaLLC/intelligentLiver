#------------------------------------------------------------------------------------------------------
#
#   Project - SXHX Hospital
#   Description:
#       Collections of Projects for SXHX Hospital
#   Author: huiliu.liu@gmail.com
#   Created 2020-01-04
#------------------------------------------------------------------------------------------------------
import sys

# window platform
if sys.platform == 'win32': from hi_projects.schx_hospital.config_win import *

# linux platform
if sys.platform == 'linux': from hi_projects.schx_hospital.config_lnx import *

# macos platform
if sys.platform == 'macos': from hi_projects.schx_hospital.config_macos import *

class Liver_MR_Sequence(object):
    # definition of MR sequences used for Liver Scan
    def __init__(self):
        super().__init__()
        self.seq_name_pre = 'pre'
        self.seq_name_ap = 'ap'
        self.seq_name_pvp = 'pvp'
        self.seq_name_tp = 'tp'
        self.seq_name_hbp = 'hbp'
        self.seq_name_t2w = 't2w'
        self.seq_name_in_phase = 'in-phase'
        self.seq_name_opp_phase = 'opp-phase'
        self.seq_name_dwi = 'dwi'
        self.seq_name_adc = 'adc'
        self.seq_name_others = 'others'

liver_mr_seq = Liver_MR_Sequence()

class DICOM_Annotation_Key(object):
    # definition of annotation keys for dataframe
    def __init__(self):
        super().__init__()
        self.sub_code = 'sub_code_hanyu'
        self.sub_name = 'sub_name_hanyu'
        self.sub_id = 'sub_id_hanyu'
        self.sub_comment = 'sub_comment_hanyu'
        self.patient_name = 'patient_name'
        self.patient_id = 'patient_id'
        self.series_number = 'series_number'
        self.series_description = 'series_description'
        self.sequence_name = 'sequence_name'
        self.series_anno_hy = 'series_anno_from_hanyu'
        self.series_anno_hl = 'series_anno_from_hliu'
        self.series_nii_anno = 'series_merge_code'
        self.nb_series = 'number_of_series_same_root'
        self.nb_slices = 'number_of_slices'
        self.study_datetime = 'study_datetime'
        self.series_acq_datetime = 'series_acq_datetime'
        self.series_offset_time = 'series_offset_time'
        self.series_uid = 'series_uid'
        self.series_dcm_root_from_hy = 'series_dcm_root_from_hanyu'

dicom_annotation_key = DICOM_Annotation_Key()