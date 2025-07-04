#SHU Dataset for FBCSP algorithm
#Original algorithm link is  https://fbcsptoolbox.github.io/publications
#filter bank parameter:
#Number of filters :  a filter bank consisting of 9 bandpass filters, Frequency bands : 4-8Hz, 8-12Hz, 12-16Hz, 16-20Hz, 20-24Hz, 24-28Hz, 28-32Hz, 32-36Hz, 36-40Hz, Filter design: 4th order Butterworth filter


from bin.MLEngine import MLEngine
import scipy.io as sio
import os

if __name__ == "__main__":

    result=[]
    for subj in range(1,157):

            '''Example for loading SHU Dataset '''
            dataset_details={
                'data_path' : r'SHU_Dataset',
                'file_to_load': subj,
                'ntimes': 1,
                'kfold':10,
                'm_filters':4,
                'window_details':{'tmin':0.5,'tmax':4-0.004}
            }

            ML_experiment = MLEngine(**dataset_details)
            result.append(ML_experiment.experiment())
sio.savemat('result.mat',{'res':result})
with open (r'results.txt','w') as f:
    f.writelines(str(result))