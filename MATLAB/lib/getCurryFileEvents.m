function [events, evtimes, evtypes] = getCurryFileEvents( curr_file, nEvents)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%%% ARGUMENTS:
%       curr_file: Name of curry file [Type: string] 
%       nEvents: Number of events to return [Type: int] (Optional argument for truncating data)
%
%%% RETURN VALUES:
%       events: Array (Dim: number of events in block X 2) [Type: double]  
%           This contains a column of time stamps and a column of trigger codes for each event
%
%       evtimes: Array (Dim: number of events in block X 1) [Type: double] (Optional)
%           This contains a column of time stamps for each event
%
%       evtypes: Array (Dim: number of events in block X 1) [Type: double] (Optional)
%           This contains a column of trigger codes for each event 
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% boolean for truncating output
truncate = 1;

if nargin > 2
    error('Too many input arguments');
end 

if nargin == 1
    % dont truncate
    truncate = 0;
end 

if ~exist(curr_file,'file')
    error('%s : file does not exist',curr_file);
end

display(sprintf('Currently Parsing : %s',curr_file))

% load curry file
dat = load(curr_file);
fs = 500; % sample rate

% set time zero (subtract first time value divide by sample rate)
evtimes = (dat(:,1)-dat(1,1))/fs; 
% get trigger codes
evtypes = dat(:,3);

events = [evtypes, evtimes];

if nEvents > size(evtimes,1)
    nEvents = num2str(nEvents);
    display('Warning: In Function: getCurryFileEvents')
    display(sprintf('The number %s, exceeds number of events in the block. \n Output was not truncated',nEvents));
    truncate = 0; % do not truncate
end

% to truncate or not to truncate 
if truncate
    % truncate outputs
    events = events(1:nEvents, :);
    evtimes = evtimes(1:nEvents, :);
    evtypes = evtypes(1:nEvents, :);
end

end

