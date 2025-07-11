bst_mne_init('Initialize', 1);
py.importlib.import_module('mne');
mneObj = out_mne_data('E:\brainStorm_db\zhangxuanxuan\data\NewSubject\@rawsession001\data_0raw_session001.mat', 'Raw');
py_data = mneObj.get_data();
raw_data = double(py.numpy.array(py_data));


% mneObj.save('your_filename.fif', overwrite=True)
% data_type = char(py.str(py_data.dtype));  % 先转为Python字符串，再转为MATLAB字符
% data_shape = py.tuple(py_data.shape);  % 获取形状元组
% disp(['原始数据类型: ', data_type]);
% disp(['原始数据形状: ', char(py.str(data_shape))]);
%whos raw_data  % 显示数据大小和类型
%py.numpy.save('D:\wuzhanjie\meg_data1.npy', py.numpy.array(raw_data));
%times = double(py.numpy.array(mneObj.times));
%py.numpy.save('D:\wuzhanjie\meg_times1.npy', py.numpy.array(times));
%sfreq = double(mneObj.info{'sfreq'});
%ch_names = cell(mneObj.info{'ch_names'});
%str_array = string(ch_names).';
%writetable(table(str_array), 'D:\wuzhanjie\ch_names.csv');
%writecell([{'SamplingFrequency'}, {sfreq}], 'D:\wuzhanjie\metadata.csv');
