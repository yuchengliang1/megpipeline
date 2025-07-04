import scipy.io as sio
import os
import numpy as np

data_path  = os.path.join('F:\Doctor\data\FBCNet_data\class4_data\S001.mat')
raw_data = sio.loadmat(data_path)
labels = raw_data.get('labels')
# label = np.transpose(labels).tolist()
label = labels.tolist()
data = raw_data.get('data')

for i,j in enumerate(label):
    if j == 3:
        a = i

labels_index = label.index.all(3)
