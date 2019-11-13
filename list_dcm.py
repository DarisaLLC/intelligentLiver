
import os
import pydicom
import pandas as pd

from pydicom.misc import is_dicom

#--------------------------------------------------------------------------------------
#
def dump_dcminfo2xlsx(dcm_root):
    """
    :param dcm_root:
    :return:
    """
    d = {'patient_no': [], 'patient_id': [], 'patient_name': [], 'patient_level_comments': [],
         'series_description': [], 'series_rootname': []}
    patient_rootnames = os.listdir(dcm_root)
    for patient_rootname in patient_rootnames:
        #print(patient_rootname)
        patient_root = os.path.join(dcm_root, patient_rootname)
        series_rootnames = os.listdir(patient_root)
        patient_info = patient_rootname.split(' ')
        patient_no = patient_info[0]
        patient_level_comment = patient_info[-1]
        for series_rootname in series_rootnames:
            series_root = os.path.join(patient_root, series_rootname)
            dcm_files = []
            for sub_root, sub_dir, files in os.walk(series_root):
                for file in files:
                    a = os.path.join(sub_root, file)
                    if file.endswith('.dcm'): dcm_files.append(a)
                    if len(dcm_files) > 1: continue
                    if is_dicom(a): dcm_files.append(a)
                    if len(dcm_files) > 1: continue
            if len(dcm_files) < 1:
                print('..... failed - %s : %s' % (patient_rootname, series_rootname))
                continue
            dcm_file = dcm_files[0]
            ds = pydicom.read_file(dcm_file, force=True)
            try:
                success = False
                patient_id = ds.PatientID
                patient_name = ds.PatientName
                series_description = ds.SeriesDescription
                success = True
                if success:
                    d['patient_no'].append(patient_no)
                    d['patient_id'].append(patient_id)
                    d['patient_name'].append(patient_name)
                    d['patient_level_comments'].append(patient_level_comment)
                    d['series_description'].append(series_description)
                    d['series_rootname'].append(series_rootname)
            except:
                print('................ %s'%(dcm_file))
    info = pd.DataFrame(d)
    return info
#-----------------------------------------------------------------------------------------
#
# TEST PURPOSE
#
#-----------------------------------------------------------------------------------------
#
dcm_root = 'F:\\huaxi\\Liver-EOB-DCM'
df = dump_dcminfo2xlsx(dcm_root)
df.to_excel(os.path.join(dcm_root, 'info.xlsx'))