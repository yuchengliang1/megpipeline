import mne
import os
import glob
import numpy as np
from os.path import join
import scipy.io as sio
import random

class LoadData:
    def __init__(self,eeg_file_path: str):
        self.eeg_file_path = eeg_file_path

    def load_raw_data_gdf(self,file_to_load):
        self.raw_eeg_subject = mne.io.read_raw_gdf(self.eeg_file_path + '/' + file_to_load)
        return self

    def load_raw_data_mat(self,file_to_load):
        import scipy.io as sio
        self.raw_eeg_subject = sio.loadmat(self.eeg_file_path + '/' + file_to_load)

    def get_all_files(self,file_path_extension: str =''):
        if file_path_extension:
            return glob.glob(self.eeg_file_path+'/'+file_path_extension)
        return os.listdir(self.eeg_file_path)


ch_names_list = ["Fpz","Fp1","Fp2","AF3","AF4","AF7","AF8","Fz","F1","F2","F3","F4","F5",
              "F6","F7","F8","FCz","FC1","FC2","FC3","FC4","FC5","FC6","FT7","FT8","Cz",
              "C1","C2","C3","C4","C5","C6","T7","T8","CP1","CP2","CP3","CP4","CP5","CP6",
              "TP7","TP8","Pz","P3","P4","P5","P6","P7","P8","POz","PO3","PO4","PO5",
              "PO6","PO7","PO8","Oz","O1","O2"]

class loadSHU:
    def __init__(self,subject_id,data_path):
        self.id=subject_id
        self.path=data_path
        self.fs=250
    def get_epochs(self):
        data,labels=get_data(self.path,self.id)
        data=data.transpose(2,0,1)
        eeg_data = {'x_data': data,
                    'y_labels': labels-1,
                    'fs': self.fs,
                    'ch_names':ch_names_list}
        return eeg_data

def get_data(data_path,id):
    da=sio.loadmat(join(data_path,'S'+str(id).zfill(3)+'.mat'))
    data=da['data']
    labels=np.ravel(da['labels'])

    return data, labels

