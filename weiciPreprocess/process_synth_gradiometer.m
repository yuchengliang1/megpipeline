function varargout = process_synth_gradiometer( varargin )
% PROCESS_NOTCH: Remove one or more sinusoids from a signal
%
% USAGE:      sProcess = process_gradiometer('GetDescription')
%               sInput = process_gradiometer('Run',     sProcess, sInput)
%                    x = process_gradiometer('Compute', x, sfreq, FreqList, Method, bandWidth=1)

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
    sProcess.Comment     = 'synth_gradiometer';
    sProcess.FileTag     = 'synth_gradiometer';
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
function sInput = Run(sProcess, sInput, sInput_Ref) %#ok<DEFNU>
    
    % Get options
    ch_ref = sProcess.options.refsensortypes.Value;

    if isempty(ch_ref) | isempty(sInput_Ref)
        
        bst_report('Error', sProcess, [],'No MEG REF Channel in input.');
        
        sInput = [];        

    end


    sInput.A = Compute(sInput.A, sInput_Ref);
    
    
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