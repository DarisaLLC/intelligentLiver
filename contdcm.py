import os
import pandas as pd
from dcmconv.dcm2niix import conv_series2nii

xlsx_file = 'F:\\huaxi\\dcm_info_201911172325.xlsx'
df = pd.read_excel(xlsx_file)
patient_nos = df['patient_no'].values
series_akas = df['series_aka'].values
conv2dcms = df['conv2dcm'].values
series_roots = df['series_root'].values
nii_root = 'F:\\huaxi\\nii'
for patient_no, series_aka, conv2dcm, series_root in zip(patient_nos, series_akas, conv2dcms, series_roots):
    sub_name = 'sub-' + '{:03d}'.format(int(patient_no))
    sub_root = os.path.join(nii_root, sub_name)
    os.makedirs(sub_root, exist_ok=True)
    if not conv2dcm == True: continue
    series_filename = sub_name + '_' + series_aka
    nii_file = os.path.join(sub_root, series_filename + '.nii.gz')
    if os.path.exists(nii_file): continue
    try:
        print('working on %s - %s' % (sub_name, series_filename))
        conv_series2nii(series_root, sub_root, series_filename, zipped=True)
    except:
        print('....... failed to convert %s - %s' % (sub_name, series_filename))