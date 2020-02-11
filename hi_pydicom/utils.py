#------------------------------------------------------------------------------------------------------
#
#   Project - hI pydicom
#   Description:
#       An extension to pydicom
#   Author: huiliu.liu@gmail.com
#   Created 2020-01-04
#------------------------------------------------------------------------------------------------------

import os
import pydicom
import difflib

from glob import glob
from datetime import datetime
from pydicom.misc import is_dicom

from hi_pydicom.tags import TagSeriesUID, TagStudyUID
from hi_pydicom.tags import TagPatientID, TagPatientName, TagPatientSex, TagPatientAge, TagPatientWeight
from hi_pydicom.tags import TagStudyDate, TagStudyTime, TagAcquisitionDate, TagAcquisitionTime
from hi_pydicom.tags import TagSequenceName, TagSeriesDescription, TagSeriesNumber, TagSeriesNbSlices

#------------------------------------------------------------------------------------------------------
#
def diff_datetime_tag(datetime_tag_0, datetime_tag_1):
    """
    :param datetime_tag_0: '20190322143502'
    :param datetime_tag_1: '20190322143502'
    :return:
    """
    d_0 = datetime.strptime(datetime_tag_0, '%Y%m%d%H%M%S')
    d_1 = datetime.strptime(datetime_tag_1, '%Y%m%d%H%M%S')
    delta_time = d_1 - d_0
    return delta_time.seconds
#------------------------------------------------------------------------------------------------------
#
def read_timing(ds):
    """
    :param ds:
    :return:
    """
    default_datetime = datetime.fromordinal(1).strftime('%Y%m%d%H%M%S')
    study_date = default_datetime[:8] if ds.get(TagStudyDate) is None else ds.get(TagStudyDate).value
    study_time = default_datetime[8:] if ds.get(TagStudyTime) is None else ds.get(TagStudyTime).value[:6]
    acq_date = default_datetime[:8] if ds.get(TagAcquisitionDate) is None else ds.get(TagAcquisitionDate).value
    acq_time = default_datetime[8:] if ds.get(TagAcquisitionTime) is None else ds.get(TagAcquisitionTime).value[:6]
    return study_date + study_time, acq_date + acq_time
#------------------------------------------------------------------------------------------------------
#
def read_series_offset_seconds(ds):
    """
    :param ds:
    :return:
    """
    study_datetime, acq_datetime = read_timing(ds)
    return diff_datetime_tag(study_datetime, acq_datetime)
#------------------------------------------------------------------------------------------------------
#
def read_patient_info(ds):
    """
    :param ds:
    :return:
    """
    patient_name = 'patient name' if ds.get(TagPatientName) is None else ds.get(TagPatientName).value
    patient_id = 'patient id' if ds.get(TagPatientID) is None else ds.get(TagPatientID).value
    patient_age = 0 if ds.get(TagPatientAge) is None else ds.get(TagPatientAge).value[:3]
    patient_sex = 'sex' if ds.get(TagPatientSex) is None else ds.get(TagPatientSex).value
    patient_weight = 0.0 if ds.get(TagPatientWeight) is None else ds.get(TagPatientWeight).value
    return patient_name, patient_id, patient_age, patient_sex, patient_weight
#------------------------------------------------------------------------------------------------------
#
def read_study_info(ds):
    """
    :param ds:
    :return:
    """
    study_uid = ds[TagStudyUID].value
    default_datetime = datetime.fromordinal(1).strftime('%Y%m%d%H%M%S')
    study_date = default_datetime[:8] if ds.get(TagStudyDate) is None else ds.get(TagStudyDate).value
    study_time = default_datetime[8:] if ds.get(TagStudyTime) is None else ds.get(TagStudyTime).value[:6]
    return study_uid, study_date + study_time
#------------------------------------------------------------------------------------------------------
#
def read_series_info(ds):
    """
    :param dcm_file:
    :return:
    """
    s_uid = ds.get(TagSeriesUID).value
    seq_name = 'sequence name' if ds.get(TagSequenceName) is None else ds.get(TagSequenceName).value
    s_description = 'series description' if ds.get(TagSeriesDescription) is None else ds.get(TagSeriesDescription).value
    s_series_id = 0 if ds.get(TagSeriesNumber) is None else ds.get(TagSeriesNumber).value
    s_nb_slices = 0 if ds.get(TagSeriesNbSlices) is None else int(ds.get(TagSeriesNbSlices).value)
    return s_uid, seq_name, s_description, s_series_id, s_nb_slices
#------------------------------------------------------------------------------------------------------
#
def get_dcm_files(series_root):
    """
    :param series_root:
    :return:
    """
    dcm_files = glob(os.path.join(series_root, '*.dcm'))
    if len(dcm_files) != 0: return dcm_files
    files = [os.path.join(series_root, f) for f in os.listdir(series_root)
             if os.path.isfile(os.path.join(series_root, f))]
    for file in files:
        if is_dicom(file): dcm_files.append(file)
    return dcm_files
#------------------------------------------------------------------------------------------------------
#
def get_series_files_by_series_uid(series_root, suid, tags=None, tag_values=None):
    """
    :param series_root:
    :param suid:
    :return:
    """
    out_files = []
    files = [os.path.join(series_root, f) for f in os.listdir(series_root)
             if os.path.isfile(os.path.join(series_root, f))]
    for _file in files:
        if not is_dicom(_file): continue
        _ds = pydicom.read_file(_file, stop_before_pixels=True, force=True)
        _suid = _ds[TagSeriesUID].value
        _valid = [suid == _suid]
        if tags is not None: _valid += [str(_ds[tag].value) == str(tag_value) for tag, tag_value in zip(tags, tag_values)]
        if all(_valid): out_files.append(_file)
    return out_files
#------------------------------------------------------------------------------------------------------
#
def get_1n_dcm_files(dcm_files, by='FILEID'):
    """
    :param series_root:
    :param by:          'FILEID', 'ACQDATETIME'
    :return:
    """
    if by is 'FILEID':
        dcm_filenames = []
        for dcm_file in dcm_files: dcm_filenames.append(os.path.basename(dcm_file))
        dcm_filenames.sort()
        dcm_filename_0 = dcm_filenames[0]
        dcm_filename_n = dcm_filenames[-1]
    elif by is 'ACQDATETIME':
        dcms = {}
        for dcm_file in dcm_files:
            ds = pydicom.read_file(dcm_file, stop_before_pixels=True)
            acq_datetime = ds.get(TagAcquisitionDate).value + ds.get(TagAcquisitionTime.value[:6])
            if dcms.get(acq_datetime) is None: dcms[acq_datetime] = []
            dcms[acq_datetime].append(os.path.basename(dcm_file))
        acqs = sorted(dcms.keys())
        dcm_filename_0 = dcms[acqs[0]][0]
        dcm_filename_n = dcms[acqs[-1]][0]
    else:
        dcm_filename_0 = None
        dcm_filename_n = None
    return dcm_filename_0, dcm_filename_n
#------------------------------------------------------------------------------------------------------
#
def get_series_1th_file(dcm_files):
    """
    :param dcm_files:
    :return: {'series_uid': 1st_dcm_file, ...}
    """
    suid_dict = {}
    for _dcm_file in dcm_files:
        _ds = pydicom.read_file(_dcm_file, stop_before_pixels=True, force=True)
        suid = _ds[TagSeriesUID].value
        if suid_dict.get(suid) is None: suid_dict[suid] = _dcm_file
    return suid_dict
#-------------------------------------------------------------------------------------------------------
#
def print_diff_tags(ds_1, ds_2):
    """
    :param ds_1:
    :param ds_2:
    :return:
    """
    rep = []
    for dataset in (ds_1, ds_2):
        lines = str(dataset).split("\n")
        lines = [line + "\n" for line in lines]  # add the newline to end
        rep.append(lines)

    diff = difflib.Differ()

    for line in diff.compare(rep[0], rep[1]):
        if line[0] != "?":
            print(line)
    return