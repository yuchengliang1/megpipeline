function varargout = process_synth_gradiometer_window( varargin )
% PROCESS_NOTCH: Remove one or more sinusoids from a signal
%
% USAGE:      sProcess = process_synth_gradiometer_window('GetDescription')
%               sInput = process_gradiometer_window('Run',     sProcess, sInput)
%                    x = process_gradiometer_window('Compute', x, sfreq, FreqList, Method, bandWidth=1)

% @=============================================================================
% This function is part of the Brainstorm software:
% https://neuroimage.usc.edu/brainstorm
% 
% Copyright (c) University of Southern California & McGill University
% This software is distributed under the terms of the GNU General Public License
% as published by the Free Software Foundation. Further details on the GPLv3
% license can be found at http://www.gnu.org/copyleft/gpl.html.
% 
% FOR RESEARCH PURPOSES ONLY. THE SOFTWARE IS PROVIDED "AS IS," AND THE
% UNIVERSITY OF SOUTHERN CALIFORNIA AND ITS COLLABORATORS DO NOT MAKE ANY
% WARRANTY, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO WARRANTIES OF
% MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE, NOR DO THEY ASSUME ANY
% LIABILITY OR RESPONSIBILITY FOR THE USE OF THIS SOFTWARE.
%
% For more information type "brainstorm license" at command prompt.
% =============================================================================@
%
% Authors: Sebastian Peng, 2023-
% 
% The "hnotch" filter is implemented based on: 
% Mitra, Sanjit Kumar, and Yonghong Kuo. Digital signal processing: a computer-based approach. Vol. 2. New York: McGraw-Hill, 2006.
%
% The older code inspired from MatlabCentral post:
% http://www.mathworks.com/matlabcentral/newsreader/view_thread/292960

eval(macro_method);
end


%% ===== GET DESCRIPTION =====
function sProcess = GetDescription() %#ok<DEFNU>
    % Description the process
    sProcess.Comment     = 'synth_gradiometer_window';
    sProcess.FileTag     = 'synth_gradiometer_window';
    sProcess.Category    = 'Filter';
    sProcess.SubGroup    = 'Pre-process';
    sProcess.Index       = 777;
    sProcess.Description = 'https://neuroimage.usc.edu/brainstorm/Tutorials/ArtifactsFilter#Filter_specifications:_Notch';
    
    % Definition of the input accepted by this process
    sProcess.InputTypes  = {'data', 'results', 'raw', 'matrix'};
    sProcess.OutputTypes = {'data', 'results', 'raw', 'matrix'};
    sProcess.nInputs     = 1;
    sProcess.nMinFiles   = 1;
    sProcess.processDim  = 1;   % Process channel by channel

    % === Sensor types
    sProcess.options.sensortypes.Comment = 'Sensor types or names (empty=all): ';
    sProcess.options.sensortypes.Type    = 'text';
    sProcess.options.sensortypes.Value   = 'MEG';
    sProcess.options.sensortypes.InputTypes = {'data', 'raw'};

    % === Ref Sensor types
    sProcess.options.refsensortypes.Comment = 'Ref Sensor types or names';
    sProcess.options.refsensortypes.Type    = 'text';
    sProcess.options.refsensortypes.Value   = 'MEG REF';
    sProcess.options.refsensortypes.InputTypes = {'data', 'raw'};

    % === Ref Filter
    sProcess.options.filter_ref.Comment = 'Ref Filter(Hz)';
    sProcess.options.filter_ref.Type = 'text';
    sProcess.options.filter_ref.Value = '2,20; 20,80';

    % === Derivatives
    sProcess.options.derivatives.Comment = 'Derivatives';
    sProcess.options.derivatives.Type = 'checkbox';
    sProcess.options.derivatives.Value = 1;

    % === Win Size
    sProcess.options.winsize.Comment = 'WinSize(s)';
    sProcess.options.winsize.Type = 'text';
    sProcess.options.winsize.Value = '100';

    % === Read All Flag
    sProcess.options.read_all.Comment = 'Load All Data into Buffer';
    sProcess.options.read_all.Type = 'checkbox';
    sProcess.options.read_all.Value = 1;
    sProcess.options.read_all.Group = 'input';

end

%% ===== FORMAT COMMENT =====
function Comment = FormatComment(sProcess) %#ok<DEFNU>
    if isempty(sProcess.options.refsensortypes.Value(1))
        Comment = 'Synth Gradiometer: No MEG REF Channel Selected';
    else
        Comment = ['Synth Gradiometer: ',sProcess.options.refsensortypes.Value(1:end)];
    end
end



%% ===== RUN =====
function sInput = Run(sProcess, sInput, sInput_Ref, BlockSizeRow) %#ok<DEFNU>
    
    % Initialize FieldTrip
    [isInstalled, errMsg] = bst_plugin('Install', 'fieldtrip');
    if ~isInstalled
        bst_report('Error', sProcess, [], errMsg)
        return;
    end
    bst_plugin('SetProgressLogo', 'fieldtrip');


    % Get options
    ch_ref = sProcess.options.refsensortypes.Value;
    fid = fopen('gradiometer.txt', 'w'); % 打开文件，'w'表示写入模式
    fprintf(fid, '%s', sInput_Ref);
    fclose(fid);
    if isempty(ch_ref) | isempty(sInput_Ref)
        
        bst_report('Error', sProcess, [],'No MEG REF Channel in input.');
        
        sInput = [];        

    end
    % FieldTrip config struct to collect information of processing
    cfg0 = [];
    cfg0.winsize = str2double(sProcess.options.winsize.Value);
    
    if sProcess.options.derivatives.Value == 1
        cfg0.deriatives = 'yes'; 
    else
        cfg0.deriatives = 'no';
    end

    cfg0.filter_ref = str2num(sProcess.options.filter_ref.Value);


    

    % Channel Mat and get all channels
    ChannelMat = in_bst_channel(sInput.ChannelFile);

    iREFs = [];
    for i = 1 : size(ChannelMat.Channel, 2)
        disp(ChannelMat.Channel(i).Type)
        if strcmp(ChannelMat.Channel(i).Type, 'MEG REF')
            iREFs = vertcat(iREFs, i);
        end
    end

    if sInput.iBlockRow == 1

    iChannels = [iREFs; sInput.iRowProcess]';
    
    else

    iMEGs = sInput.iRowProcess+(sInput.iBlockRow-1)*BlockSizeRow;
    
    iChannels = [iREFs; iMEGs]';

    end
    DataMat = [sInput_Ref;sInput.A];

    % Error: All channels tagged as bad
    if isempty(iChannels)
        bst_report('Error', sProcess, sInput, 'All the selected channels are tagged as bad.');
        return;
    end

    ftData = xmag_out_fieldtrip_data(DataMat, sInput.TimeVector, ChannelMat, iChannels, 0);

    
    cfg = [];
    cfg.channel = vertcat(ft_channelselection_opm('MEG', ftData));
    cfg.refchannel = vertcat(ft_channelselection_opm('MEGREF', ftData));
    cfg.return_all = 'no';
    cfg.winsize = cfg0.winsize;
    cfg.filter_ref = cfg0.filter_ref;
    cfg.derivative = cfg0.deriatives;

    data_synth_grad = xmag_opm_synth_gradiometer_window(cfg, ftData);


    % Plot PSD
    cfg                 = [];
    cfg.channel         = vertcat(ft_channelselection_opm('MEG',ftData));
    cfg.trial_length    = 10;
    cfg.method          = 'tim';
    cfg.foi             = [2 80];
    cfg.plot            = 'yes';
    cfg.plot_chans      = 'yes';
    cfg.plot_ci         = 'no';
    cfg.plot_legend     = 'yes';
    cfg.transparency    = 0.3;
    [pow freq]          = ft_opm_psd_compare(cfg, ftData, data_synth_grad);
    title('Synth Grad Gain')


    sInput.A = data_synth_grad.trial{1};
    
    
    if isfield(sInput, 'Std') && ~isempty(sInput.Std)
        sInput.Std = [];
    end

end


%% ===== EXTERNAL CALL =====
% USAGE:  Mr = process_synth_gradiometer('Compute', M , Ref)
function Mr = Compute(M, Ref)

    % get the reference channel data
    reference = Ref';
    
    clear Ref
    
    drefer = diff(reference);
    drefer = [drefer(1,:); drefer];
    reference = [drefer, reference];

    % doing synth gradiometer regression 
    beta = pinv(reference)*M';
    Mr = (M'-reference*beta)';

end