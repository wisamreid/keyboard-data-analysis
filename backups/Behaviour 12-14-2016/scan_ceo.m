% scan_ceo.m
% for Duet task Curry file analysis
% 2016 June 9 by Takako Fujioka

% the main purpose of this program is to read in the .ceo (actually the
% middle part only - converted by 'do_store_events.sh' to the files called
% _evt.txt for each block

% the most sought out information is which note is deviant for each trial
% and which trial is valid or not

% also we want to know how many trials are made and whether that matches
% with the number of log-files recorded by the MAX/MSP program

% ceo_file_list={ 
% 'CN_AA_1.ceo';
% 'CN_AA_2.ceo';
% 'CN_BC_1.ceo';
% 'CN_BC_2.ceo';
% 'MH_AA_1.ceo';
% 'MH_AA_2.ceo';
% 'MH_BC_1.ceo';
% 'MH_BC_2.ceo';
% 'MH_CN_AA_1.ceo';
% 'MH_CN_AA_2.ceo';
% 'MH_CN_BC_1.ceo';
% 'MH_CN_BC_2.ceo';
% };
clear all

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

player = {'SubA';'SubB'};


% loop for pairs
% store what condition for each block for each pair
partner_file_all = zeros(npair, nblock);
order_file_all = zeros(npair, nblock);
task_file_all = zeros(npair, nblock);
for ipair=1:npair
    sub={pair{ipair,1};pair{ipair,2}};
    pairname = sprintf('%s_%s', sub{1}, sub{2});
   
    subjA = sub(1);
    subjB = sub(2);
    isubjA = find(strcmp(pair,subjA)==1);
    isubjB = find(strcmp(pair,subjB)==1);
    
    partner_comb = {char(subjA);pairname; char(subjB)};
    npartner_comb = size(partner_comb,1);
ib=1;
for ipartner_comb = 1:npartner_comb
    
    subname = partner_comb{ipartner_comb};
    for itask=1:ntask
        for iorder=1:norder
            taskname = char(task(itask));
            
            
            curr_file = sprintf('./%s/%s_%s_%d_evt.txt',pairname,subname,taskname,iorder); % made them through do_store_events.sh (awk only cut and store the trigger sequence part of the .ceo file)
            display(curr_file)
            if ~exist(curr_file)
                display(sprintf('%s : file is missing',curr_file)); continue;
            end
            
            dat=load(curr_file);
            fs= 500;
            
            evsample = dat(:,1);
            evtime = (dat(:,1)-dat(1,1))/fs;
            evtype = dat(:,3);
            
            dat0 = [evtype, evtime];
            dat1 = dat0(1:40, :);
            ntrial = 50;
            
            uevtype = unique(evtype);
            nuevtype = size(uevtype,1);
            
            
            % find the condition of this block
            tmp=evtype(evtype<233 & evtype > 200);
            if size(tmp(tmp>=201 & tmp<=204),1)>round(ntrial/2) % sprurious trigger messes up this if using ~isempty              
                ipartner_file = 1; % human=1, max=2
                iorder_file = 1;  % p1 odd = 1, p1 even = 2
                itask_file = 1; % AA = 1, BC=2;
            elseif size(tmp(tmp>=205 & tmp<=208),1)>round(ntrial/2)
                ipartner_file = 1; % human=1, max=2
                iorder_file = 2;  % p1 odd = 1, p1 even = 2
                itask_file = 1; % AA = 1, BC=2
            elseif size(tmp(tmp>=209 & tmp<=212),1)>round(ntrial/2)  
                ipartner_file = 1; % human=1, max=2
                iorder_file = 1;  % p1 odd = 1, p1 even = 2
                itask_file = 2; % AA = 1, BC=2;
            elseif size(tmp(tmp>=213 & tmp<=216),1)>round(ntrial/2) 
                ipartner_file = 1; % human=1, max=2
                iorder_file = 2;  % p1 odd = 1, p1 even = 2
                itask_file = 2; % AA = 1, BC=2;
            elseif  size(tmp(tmp>=217 & tmp<=220),1)>round(ntrial/2) 
                ipartner_file = 2; % human=1, max=2
                iorder_file = 1;  % p1 odd = 1, p1 even = 2
                itask_file = 1; % AA = 1, BC=2;
            elseif size(tmp(tmp>=221 & tmp<=224),1)>round(ntrial/2) 
                ipartner_file = 2; % human=1, max=2
                iorder_file = 2;  % p1 odd = 1, p1 even = 2
                itask_file = 1; % AA = 1, BC=2
            elseif size(tmp(tmp>=225 & tmp<=228),1)>round(ntrial/2)
                ipartner_file = 2; % human=1, max=2
                iorder_file = 1;  % p1 odd = 1, p1 even = 2
                itask_file = 2; % AA = 1, BC=2;
            elseif size(tmp(tmp>=229 & tmp<=232),1)>round(ntrial/2) 
                ipartner_file = 2; % human=1, max=2
                iorder_file = 2;  % p1 odd = 1, p1 even = 2
                itask_file = 2; % AA = 1, BC=2;
            end
            % ok, store them
            partner_file_all(ipair, ib)= ipartner_file;
            order_file_all(ipair,ib)=iorder_file;
            task_file_all(ipair,ib)=itask_file;
            ib=ib+1;
        end % order
    end % task
end % partner_comb
end % pair
save('condition_block.mat')


% for each evt. txt file
%% find the time 0 of each trial
% last metronome click in the count in 
curr_ev = 233;
tmp=evtime(evtype ==curr_ev);

% select the right one as the last click before people play the notes
it_good = [];
for it = 2:length(tmp)
    if  it < length(tmp) & tmp(it)-tmp(it-1) <1 & (tmp(it+1)-tmp(it) > 17 )
        it_good = [it_good;it]; 
    elseif it==length(tmp) & tmp(it)-tmp(it-1) <1  % last trial
        it_good = [it_good;it]; 
    end
end
% during the actual trials, the metronomes comes 500ms and 17second
% alternatively, so if the trial number separates not by 2, then it's
% not good
tmp2 = it_good;
it_good2= tmp2(find(tmp2(2:end)-tmp2(1:end-1)==2));
% also the last one is OK
it_good2 =[it_good2; it_good(length(it_good))];

% this is the metronome time just immediately before the player's notes
trial_time0=tmp(it_good2);
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

            