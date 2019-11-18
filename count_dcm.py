
import os
import pandas as pd

xlsx_file = 'F:\\huaxi\\dcm_info_201911172325.xlsx'
org_xlsx_file = 'F:\\huaxi\\count_dcm.xlsx'



df = pd.read_excel(xlsx_file)
patient_nos = df['patient_no'].values
series_akas = df['series_aka'].values
conv2dcms = df['conv2dcm'].values

patients = []
patients_info = []
p_info = {'PRE': 0, 'AP': 0, 'PVP': 0, 'TP': 0, 'HBP': 0, 'T2W': 0,
          'in-phase': 0, 'opp-phase': 0, 'opp-in-phase': 0,
          'DWI': 0, 'ADC': 0}
for patient_no, series_aka, conv2dcm in zip(patient_nos, series_akas, conv2dcms):
    if patient_no not in patients:
        patients.append(patient_no)
        patients_info.append({'PRE': 0, 'AP': 0, 'PVP': 0, 'TP': 0, 'HBP': 0, 'T2W': 0,
                              'in-phase': 0, 'opp-phase': 0, 'opp-in-phase': 0,
                              'DWI': 0, 'ADC': 0})
    if conv2dcm == True:
        patients_info[-1][series_aka] += 1

p_dict = {'patient_no': [],
          'PRE': [], 'AP': [], 'PVP': [], 'TP': [], 'HBP': [], 'T2W': [],
          'in-phase': [], 'opp-phase': [], 'opp-in-phase': [],
          'DWI': [], 'ADC': []}
for patient, patient_info in zip(patients, patients_info):
    p_dict['patient_no'].append(patient)
    for key in patient_info.keys():
        p_dict[key].append(patient_info.get(key))

df = pd.DataFrame(p_dict)
df.to_excel(org_xlsx_file)