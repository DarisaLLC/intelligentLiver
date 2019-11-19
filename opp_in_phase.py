
import os
import shutil

import numpy as np
import SimpleITK as sitk

from glob import glob

#-----------------------------------------------------------------------------------------------------
#
def discrim_opp_in_phases(phase_nii_file_0, phase_nii_file_1):
    """
    :param phase_nii_files:
    :return:
    """
    np_mean_0 = np.mean(sitk.GetArrayFromImage(sitk.ReadImage(phase_nii_file_0)))
    np_mean_1 = np.mean(sitk.GetArrayFromImage(sitk.ReadImage(phase_nii_file_1)))
    in_phase = phase_nii_file_0
    opp_phase = phase_nii_file_1
    if np_mean_0 > np_mean_1:
        in_phase = phase_nii_file_1
        opp_phase = phase_nii_file_0
    return in_phase, opp_phase
#-----------------------------------------------------------------------------------------------------
#
def sort_opp_in_phases(phase_nii_files):
    """
    :param phase_nii_files:
    :return:
    """
    np_means = []
    for phase_nii_file in phase_nii_files:
        np_means.append(np.mean(sitk.GetArrayFromImage(sitk.ReadImage(phase_nii_file))))
    np_idx = np.argsort(np.array(np_means))
    opp_phase_nii_file = phase_nii_files[np_idx[0]]
    in_phase_nii_file = phase_nii_files[np_idx[-1]]
    if np_means[np_idx[0]] < np_means[np_idx[-1]]: valid = True
    else: valid = False
    return in_phase_nii_file, opp_phase_nii_file, valid
#----------------------------------------------------------------------------------------------------
#
if __name__ == '__main__':
    root = 'F:\\huaxi\\Liver-EOB-NII'
    for sub_root, sub_dir, files in os.walk(root):
        sub_name = os.path.basename(sub_root)
        """
        try:
            if len(files) < 1: continue
            opp_in_phase_nii_files = glob(os.path.join(sub_root, 'sub-*-phase*.gz'))
            in_phase_nii_file, opp_phase_nii_file, valid = sort_opp_in_phases(opp_in_phase_nii_files)

            if not valid:
                print('failed to sort %s'%(sub_name))
                continue

            new_in_phase_nii_file = os.path.join(sub_root, sub_name + '_in-pha.nii.gz')
            new_in_phase_json_file = os.path.join(sub_root, sub_name + '_in-pha.json')
            if os.path.exists(new_in_phase_nii_file) and os.path.exists(new_in_phase_json_file): continue
            shutil.copyfile(in_phase_nii_file, new_in_phase_nii_file)
            shutil.copyfile(in_phase_nii_file.replace('.nii.gz', '.json'), new_in_phase_json_file)

            new_opp_phase_nii_file = os.path.join(sub_root, sub_name + '_opp-pha.nii.gz')
            new_opp_phase_json_file = os.path.join(sub_root, sub_name + '_opp-pha.json')
            if os.path.exists(new_opp_phase_nii_file) and os.path.exists(new_opp_phase_json_file): continue
            shutil.copyfile(opp_phase_nii_file, new_opp_phase_nii_file)
            shutil.copyfile(opp_phase_nii_file.replace('.nii.gz', '.json'), new_opp_phase_json_file)

            print('successfully running opp-in-phase for %s' % (sub_name))
        except:
            print('failed to sort %s'%(sub_name))
        """
        """
        opp_in_phase_nii_files = glob(os.path.join(sub_root, 'sub-*-phase*json'))
        for opp_in_phase_nii_file in opp_in_phase_nii_files:
            os.remove(opp_in_phase_nii_file)
        print('successfully delete opp-in-phase for %s' % (sub_name))
        """