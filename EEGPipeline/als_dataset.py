import numpy as np
import mne
import os

def load_start_times(file_path):
    # 读取标签文件，获取每个标签的起始时间
    with open(file_path, 'r') as f:
        start_times = [float(line.strip()) for line in f.readlines()]
    return start_times


def extract_epochs_from_edf(edf_file, start_times, duration=4, sfreq=1000):
    # 读取EDF文件
    raw = mne.io.read_raw_edf(edf_file, preload=True)

    # 获取通道数据
    data = raw.get_data()  # 数据形状 (通道数, 时间点数)

    # 计算每段数据需要的时间点数
    n_samples = int(duration * sfreq)  # 每段数据的样本数

    epochs = []

    # 遍历每个起始时间并切割对应的片段
    for start_time in start_times:
        # 计算起始时间的样本点数
        start_sample = int((start_time + 2.5) * sfreq)
        # 切割数据片段
        epoch_data = data[:, start_sample:start_sample + n_samples]
        epochs.append(epoch_data)

    # 将数据转为numpy数组
    return np.array(epochs)


def create_epochs(edf_file, txt_files, output_dir):
    # 创建保存结果的目录
    os.makedirs(output_dir, exist_ok=True)

    # 用于保存所有片段数据和标签
    all_epochs = []
    all_labels = []

    # 存储每个标签的起始时间和对应的片段数据
    start_times_and_epochs = []

    # 循环处理每个标签文件
    for label, txt_file in enumerate(txt_files, 1):  # 从1开始为标签编号
        # 读取起始时间
        start_times = load_start_times(txt_file)
        # 提取脑电片段
        epochs = extract_epochs_from_edf(edf_file, start_times)

        # 将标签和对应的起始时间存储在一起
        for epoch, start_time in zip(epochs, start_times):
            start_times_and_epochs.append((epoch, start_time, label))  # 添加起始时间和标签

        print(f"处理标签 {label} 的片段，数据形状: {epochs.shape}")

    # 根据起始时间进行排序
    start_times_and_epochs.sort(key=lambda x: x[1])  # 按最早的起始时间排序

    # 提取排序后的片段数据和标签
    for epoch, _, label in start_times_and_epochs:
        all_epochs.append(epoch)
        all_labels.append(label)

    # 将所有片段数据合并成一个大的numpy数组，确保它是三维的
    all_epochs = np.stack(all_epochs, axis=0)  # 将列表中的数组按第一个维度（样本）堆叠成三维数组
    all_labels = np.array(all_labels)

    # 保存所有片段和标签
    np.save(os.path.join(output_dir, 'all_epochs.npy'), all_epochs)
    np.save(os.path.join(output_dir, 'all_labels.npy'), all_labels)
    print(f"保存总的all_epochs.npy，数据形状: {all_epochs.shape}")
    print(f"保存总的all_labels.npy，数据形状: {all_labels.shape}")


# 输入路径
edf_file = 'D:/xw002/XW002 EEG/ALS数据/gaojuan1.edf'
txt_files = ['C:/Users/lenovo/Desktop/lable/1.txt', 'C:/Users/lenovo/Desktop/lable/2.txt', 'C:/Users/lenovo/Desktop/lable/3.txt', 'C:/Users/lenovo/Desktop/lable/4.txt']
output_dir = 'output_epochs'

# 执行主程序
create_epochs(edf_file, txt_files, output_dir)
