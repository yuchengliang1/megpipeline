megdataFilePath = "C:\Users\yu\Desktop\FBCSP\FBCSP\1.mat";

% load(megdataFilePath);


% bst文件获取其文件详情里的mat文件地址 使用megAnalysis.m中代码将其信息加载到raw_data中
% 使用generateMegLabelData.m中代码将原始数据和record中的label信息转换为同一的格式

recordFilePath = 'C:\Users\yu\Desktop\FBCSP\FBCSP\record.txt';
row97 = raw_data(97, :);
eventIndex = find(diff(row97) > 0.4) + 1;
trimmedEvents = eventIndex(4:end-1);
blocksNumber = length(trimmedEvents) / 93;
selectedEvents = [];

for i = 1:blocksNumber
    block_first_index = (i - 1) * 93 + 1;
    block_first_label_index = block_first_index + 1;
    middleIndices = block_first_label_index:3:(block_first_label_index + 3*29);
    selectedEvents = [selectedEvents, trimmedEvents(middleIndices)];
end

% beforeTrialLabels = [250,7,8];
% trialLabels = convertedArray(recordFilePath);
% afterTrialLabels = [243,9,242,251];
% eventLabels = [beforeTrialLabels, trialLabels', afterTrialLabels];

channels = 1:64;
n_channels = length(channels);
all_trial_event_numbers = length(selectedEvents);
window_size = 7500;
data = zeros(n_channels, window_size, all_trial_event_numbers);

% 提取每个事件前后的数据
for i = 1:all_trial_event_numbers
    event_idx = selectedEvents(i);
    
    % 计算时间窗口（确保不超出数据边界）
    start_idx = max(1, event_idx - 2000);
    end_idx = min(size(raw_data, 2), event_idx + 5500);
    
    % 处理边界情况：如果窗口不足7500点，则用零填充
    if (end_idx - start_idx + 1) < window_size
        warning('待提取数据点数不足7500');
    else
        % 窗口足够大，直接提取
        window_data = raw_data(channels, (event_idx-2000):(event_idx+5499));
    end
    
    % 保存到结果数组
    data(:, :, i) = window_data;
end

% 显示结果信息
fprintf('提取的数据维度: %dx%dx%d\n', size(data));

labels = convertedLabels(recordFilePath);

matFilePath = fullfile(fileparts(recordFilePath), 'converted_meg_data.mat');
save(matFilePath, 'data', 'labels', '-v7');