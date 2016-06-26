%% File Name: scan_ceo.m
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% for Duet task Curry file analysis
% 2016 June 9 by Takako Fujioka
%
%
% Modified by  Wisam Reid 
% wisam@ccrma.stanford.edu
% June 2016
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
%%%%%%%%%%%%%%%%%%%%%%%%%%%

clc;
clear;
close all;

%% Utilities

% runHere(); % For Wisam (persistent script)

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
ntask = size(task,1);

partner = {'Human';'Max'};
npartner = size(partner,1);

order = {'odd';'even'};
norder = size(order,1);

player = {'SubA';'SubB'};

ncond = 12;
nblock = ncond;

pair = {
    'MH', 'CN'; % list subj#1 subj#2 in the order of the file
    'TD', 'NG';
    'IR', 'WR';
    'SM', 'RR';
    'XZ', 'CO';
    };
        
npair = size(pair,1);
nsubj = 2 * npair;

%% Grab a curry file
% each curry file contains a block of trials 

curr_file = 'data/MH_CN/MH_CN_BC_2_evt.txt';

[ev, evtime, evtype] = getCurryFileEvents(curr_file,1000);

%% find the time 0 of each trial
% last metronome click in the count in 

curr_ev = 233; % the current event type (trigger code)
time_stamps = evtime(evtype == curr_ev); % time stamps for curr_ev
ntime_stamps = length(time_stamps); % number of time stamps

% select the right one as the last click before people play the notes
it_good = [];

% loop through timestamps for the current event type (Trigger Code 233: Metronome)
% we are looking to find the trials with in the block
% THIS LOGIC WILL SKIP ALL SPURIOUS (Trigger Code 233's)
for ith_event_time = 2:ntime_stamps % chop off first 2 (If we want to process files in batches, this is not general enough)
    
    % Check If:
    %
    %   1) ith_event_time is with in the range of ntime_stamps 
    %     &
    %   2) the current time stamp - the previous time stamp, is less than one second
    %     &
    %   3) the next time stamp - the current time stamp, is greater than 17 seconds
    %                                                                           
    if  ith_event_time < ntime_stamps & time_stamps(ith_event_time) - time_stamps(ith_event_time - 1) < 1 & (time_stamps(ith_event_time + 1) - time_stamps(ith_event_time) > 17 )

        % store event index
        it_good = [it_good;ith_event_time]; 
    
    % Catch last trial
    %
    % Check If:
    %
    %   1) ith_event_time is with in the range of ntime_stamps
    %     &
    %   2) the current time stamp - the previous time stamp, is less than one second
    %   
    elseif ith_event_time == ntime_stamps & time_stamps(ith_event_time)-time_stamps(ith_event_time-1) < 1  
        
        % store event index
        it_good = [it_good;ith_event_time]; 
        
    end
    
end

% during the actual trials, the metronomes comes 500 ms and 17 sec
% alternatively, so if the trials are not separated by an index of 2, then it's
% not good
% 
% Wisam's Notes:
% If the index distance is greater than 2, this means that we skipped a
% SPURIOUS (Trigger Code 233's) in the loop above
tmp2 = it_good;
it_good2 = tmp2(find(tmp2(2:end)-tmp2(1:end-1)==2));
% also the last one is OK
it_good2 = [it_good2; it_good(length(it_good))];

% this is the metronome time just immediately before the player's notes
trial_time0 = time_stamps(it_good2);
ntrial = length(trial_time0);


%% ok, now find 'failure trial' code between the trials or practice trial
terror=evtime(evtype >= 240 & evtype <= 246 | evtype == 234);

itrial_err =[];
for itrial = 2:ntrial
    curr_time0 = trial_time0(itrial);
    prev_time0 = trial_time0(itrial-1);
    
    for iterror = 1:length(terror)
        if terror(iterror)> prev_time0 & terror(iterror) < curr_time0
            itrial_err = [itrial_err;itrial-1];
        end
    end
end
itrial_err = unique(itrial_err);

%% now find 'deviant note' code between them and find which note was deviant
 
tdev=evtime(evtype == 235 | evtype == 239);

dev_pos=zeros(ntrial,2); % store all the deviant note position for the odd and even player (1st or 2nd column)

for itrial = 2:ntrial
    curr_time0 = trial_time0(itrial);
    prev_time0 = trial_time0(itrial-1);
    
    tmp=evtype((evtime>prev_time0 & evtime<curr_time0), :);
    itdev=find(tmp == 235 | tmp == 239);
    evdev = tmp(itdev-1);
    if isempty(evdev) continue
    else
        
    for iev = 1:length(evdev)
        if ismember(evdev(iev), [54,55,64,65]) % odd number phrase get a deviant
             player_dev = 1;
             if evdev(iev) < 60
                 note_dev = mod(evdev(iev),10); % 1st phrase
             else
                 note_dev= mod(evdev(iev),10)+ 12; % 3rd phrase
             end
             dev_pos(itrial-1, player_dev) = note_dev;
        else % even number phrase get a deviant
            player_dev = 2;
            if evdev(iev) < 160
                 note_dev = mod(evdev(iev),10)+ 6;
             else
                 note_dev= mod(evdev(iev),10)+ 18;
            end
            dev_pos(itrial-1, player_dev) = note_dev;
        end    
    end
    end
    
end

itrial_bad = find(dev_pos(:,1) == 0);

            