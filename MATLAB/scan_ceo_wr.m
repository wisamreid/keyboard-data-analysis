%% File Name: scan_ceo.m
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% for Duet task Curry file analysis
% Started: 2016 June 9 by Takako Fujioka
%
%
% Modified by  Wisam Reid 
% wisam@ccrma.stanford.edu
% December 2016
%
% The main purpose of this program is to read in the .ceo (actually the
% middle part only - converted by 'do_store_events.sh' to the files called
% _evt.txt for each block
%
% The most sought out information is which note is deviant for each trial
% and which trial is valid or not
%
% Also we want to know how many trials are made and whether that matches
% with the number of log-files recorded by the MAX/MSP program
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% CLEAN AND CLEAR

clc;
clear;
close all;

%% Utilities

%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Sets Matlab's current
% directory
%
% Adds all of the parent 
% folder's subdirectories
%%%%%%%%%%%%%%%%%%%%%%%%%%%
tmp = matlab.desktop.editor.getActive;
file = tmp.Filename;
clear tmp
cd(fileparts(file));
file(find(file=='/',1,'last'):end) = [];
addpath(genpath(file))
%%%%%%%%%%%%%%%%%%%%%%%%%%%

dataDirectory = 'data/';

%% Boolean flags

%% Start of Takako's Code

task = {'AA'; 'BC'};
nTask = size(task,1);

partner = {'Human';'Max'};
nPartner = size(partner,1);

order = {'odd';'even'};
norder = size(order,1);

player = {'SubA';'SubB'};

% number of conditions/blocks
nBlocks = 12;

pair = {
    'MH', 'CN'; % list subj#1 subj#2 in the order of the file
    'TD', 'NG';
    'IR', 'WR';
    'SM', 'RR';
    'XZ', 'CO';
    };

% number of pairs
nPair = size(pair,1);
% number of subjects
nSubj = 2 * nPair;

%% Grab a curry file
% each curry file contains a block of trials 
% 
curr_file = 'data/IR_WR/b01_evt.txt';

% FUNCTION DEF: getCurryFileEvents
% [events, evtimes, evtypes] = getCurryFileEvents( curr_file [string], nEvents [int]) 
% use a second argument to truncate output
% 
% For details see lib/getCurryFileEvents.m
[curry_file_events, curry_file_event_times, curry_file_event_trigger_codes] = getCurryFileEvents(curr_file);

%% find the time 0 of each trial
% last metronome click in the count in 
% 
TC233 = 233; % the metronome trigger code

event_time_stamps = curry_file_event_times(curry_file_event_trigger_codes == TC233); % time stamps for curr_ev
nCurry_events = length(event_time_stamps); % the number of logged events int the curry file (time stamps)

% We want to grab the idx for the beginning of the 
% trial (metronome tick just before the first note)
good_trial_idx = [];

% loop through timestamps for the current event type 
% (Trigger Code 233: Metronome)
% we are looking to find the trials with in the block
% THIS LOGIC WILL SKIP ALL SPURIOUS Trigger Codes (233)
% 
for ith_event_time_idx = 2:nCurry_events 
    
    % Check If:
    %
    %   1) ith_event_time_idx is with in the range of ncurry_events 
    %     &
    %   2) the current time stamp - the previous time stamp, is less than one second
    %     &
    %   3) the next time stamp - the current time stamp, is greater than 17 seconds
    %                                                                           
    if  ith_event_time_idx < nCurry_events & ...
        event_time_stamps(ith_event_time_idx) - event_time_stamps(ith_event_time_idx - 1) < 1 & ...
        (event_time_stamps(ith_event_time_idx + 1) - event_time_stamps(ith_event_time_idx) > 17 )

        % store event index
        good_trial_idx = [good_trial_idx;ith_event_time_idx]; 
    
    % Catch last trial
    %
    % Check If:
    %
    %   1) ith_event_time_idx is with in the range of ntime_stamps
    %     &
    %   2) the current time stamp - the previous time stamp, is less than one second
    %   
    elseif ith_event_time_idx == nCurry_events & ...
           event_time_stamps(ith_event_time_idx) - event_time_stamps(ith_event_time_idx - 1) < 1  
        
        % store event index
        good_trial_idx = [good_trial_idx; ith_event_time_idx]; 
        
    end
    
end

% during the actual trials, the metronomes come 500 ms and 17 sec
% alternatively, so if the trials are not separated by an index of 2, then it's
% not good
% 
% Wisam's Notes:
% If the index distance is greater than 2, this means that we skipped a
% SPURIOUS (Trigger Code 233's) in the loop above
% 
tmp = good_trial_idx;
good_trial_idx = tmp(find(tmp(2:end)-tmp(1:end-1)==2));
% % the last one is okay
% good_trial_idx = [good_trial_idx; good_trial_idx(length(good_trial_idx))];
% clean out redundant indices
good_trial_idx = unique(good_trial_idx);

% this is the metronome time just immediately before the player's notes
trial_time_stamps = event_time_stamps(good_trial_idx);
nTrials = length(trial_time_stamps);


%% Look for failed trials or practice trials
% We are looking for trigger codes that indicate errors
% Error Codes: 240 - 246 
% or
% Played Note - Practice Trial: 234
%
% Check If:
%
%   1) curry_file_event_trigger_code is between 240 - 246
%     &
%   2) curry_file_event_trigger_code is 234
%   
error_TC_time_stamps = curry_file_event_times(curry_file_event_trigger_codes >= 240 & ...
         curry_file_event_trigger_codes <= 246 | ...
         curry_file_event_trigger_codes == 234);

% store error trial indices
error_trial_idx =[];

% loop through the trials
for ith_trial = 2:nTrials
    
    % set the time range for the current trial
    curr_time0 = trial_time_stamps(ith_trial);
    prev_time0 = trial_time_stamps(ith_trial - 1);
    
    % loop over error trigger codes (time stamps)
    for iterror = 1:length(error_TC_time_stamps)
        
        % Check If:
        %
        %   1) error_TC_time_stamps is between prev_time0 and curr_time0
        % 
        if error_TC_time_stamps(iterror) > prev_time0 & ... 
           error_TC_time_stamps(iterror) < curr_time0
            
            % add error trial index
            error_trial_idx = [error_trial_idx;ith_trial-1];
        
        end
    end
end

% clear redundant 
error_trial_idx = unique(error_trial_idx);

%% Correct Trials

% keep only the good time stamps
good_trial_time_stamps = trial_time_stamps(setdiff(1:length(trial_time_stamps),error_trial_idx));
% keep only the good trial indices
good_trial_idx = good_trial_idx(setdiff(1:length(trial_time_stamps),error_trial_idx));

% store the number of good trials
nGoodTrials = length(good_trial_time_stamps);

%% Find deviant notes and IOIs

% grab the time stamps for all deviant notes in the block  
deviant_note_time_stamps = curry_file_event_times(curry_file_event_trigger_codes == 235 | ...
                                                  curry_file_event_trigger_codes == 239);
 
% grab the deviant note time indices
[~,deviant_note_time_idx] = ismember(deviant_note_time_stamps,curry_file_event_times);
% grab the times for the actual note trigger codes
deviant_note_time_idx = deviant_note_time_idx - 1;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Should I be using the 'deviant_note_time_stamps' to caluclate the IOI
% or should I use 'curry_file_event_times' indexed by the notes
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% store the deviant note positions for the odd and even player (1st or 3rd column)
% store the deviant note IOIs for the odd and even player (2nd or 4th column)
deviant_note_data = zeros(nTrials, 4);

% loop over all trials (good and bad)
for ith_trial = 2:nTrials

    % set the time range for the current trial
    curr_time0 = trial_time_stamps(ith_trial);
    prev_time0 = trial_time_stamps(ith_trial - 1);
    
    % grab the trigger codes for the current trial
    tmp = curry_file_event_trigger_codes((curry_file_event_times > prev_time0 & ...
                                         curry_file_event_times < curr_time0), :);
    % we are going to chop off the last measure
    % the data is too corrupted and the last measure 
    % does not have deviants
    tmp = tmp(1:48);
    
    % deviant note indexes
    deviant_idx = find(tmp == 235 | tmp == 239);
    % get the actual note numbers  
    deviant_note_numbers = int8(deviant_idx./2);
    
    % grab the event codes
    deviant_event_codes = tmp(deviant_idx - 1);
    
    if isempty(deviant_event_codes) 
        continue
    else
        
        % assert that there are exactly 2 deviant notes 
        assert(length(deviant_note_numbers) == 2, [' Each trial must have 2 deviant notes.  Currently there are ', ...
                      int2str(length(deviant_idx))])
        
        % loop through the deviant codes
        for ith_deviant = 1:length(deviant_event_codes)
            
            % deviant is in an odd phrase  
            if ismember(deviant_event_codes(ith_deviant), [54,55,64,65]) 
                 deviant_player = 1;
                 
                 deviant_note_data(ith_trial - 1, deviant_player) = deviant_note_numbers(ith_deviant);
                 deviant_note_data(ith_trial - 1, deviant_player + 1) = 0;
            else % deviant in an even phrase
                deviant_player = 2;

                deviant_note_data(ith_trial - 1, deviant_player + 1) = deviant_note_numbers(ith_deviant);
                deviant_note_data(ith_trial - 1, deviant_player + 2) = 0;
            end    
        end
    end
    
end

itrial_bad = find(deviant_note_data(:,1) == 0);

            