% calc_diff_IOI_blocknum_ceo.m
% for Duet behavioural (MAX recorded log files) data
% 2016 April by Takako Fujioka
% 2016 June 13 by Takako Fujioka
% last modified 2016 Aug 9 by Takako Fujioka


%% definition of all the conditions
clear all
task = {'AA'; 'BC'};
ntask = size(task,1);

partner = {'Human';'Max'};
npartner = size(partner,1);

order = {'odd';'even'};
norder = size(order,1);

% I made this with scan_ceo.m (reading Curry ceo files and re-construct from triggers)
load('condition_block_blocknum.mat','player_file_all','partner_file_all', 'order_file_all', 'task_file_all')
% I made trigger coding system loaded here
load('ceo_trig_code_numbers.mat','trig','trial_trig','partner_code','task_code','order_code','devodd_code','deveven_code');


cond_subA =         [1,1,1,1,1,1,1,1,0,0,0,0];
cond_subB =         [0,0,0,0,1,1,1,1,1,1,1,1];

player_all = [1,1,1,1,3,3,3,3,2,2,2,2];


% 12 conditions are:
% 1: AA odd     SubA Max SubA Max
% 2: AA even    Max SubA Max SubA
% 3: BC odd     SubA Max SubA Max
% 4: BC even    Max SubA Max SubA
% 5: AA odd     SubA SubB SubA SubB
% 6: AA even    SubB SubA SubB SubA
% 7: BC odd     SubA SubB SubA SubB
% 8: BC even    SubB SubA SubB SubA
% 9: AA odd     Max SubB Max SubB
% 10: AA even   SubB Max SubB Max
% 11: BC odd    Max SubB Max SubB
% 12: BC even   SubB Max SubB Max

ncond = 12;
nblock = ncond;

pair = {    

    'MH', 'CN'; % list subj#1 subj#2 in the order of the file
    'TD', 'NG';
    'IR', 'WR';
    'SM', 'RR'; %
    'XZ', 'CO'};

% subject number: MH is 1, CN is 6

npair = size(pair,1);
nsubj = 2 * npair;

player = {'SubA';'SubB'};

% block2cond_mapping = [
%       [4,3,2,1,7,8,5,6,11,12,9,10];    % MH_CN from from Curry data 
%      % [4,3,2,1,8,7,6,5,11,12,9,10];       MH_CN      from block-order.txt
% 
%     %[2,1,4,3,6,5,8,7,10,9,12,11]; % TD_NG from the block-order.txt, but
%     [2,1,3,4,5,6,7,8,10,9,11,12]; % for TD_NG, this is the mapping from the Curry time stamps
%     %[2,1,4,3,5,6,7,8,9,10,12,11]; % IR_WR, block_order1 except the last two from block_order2
%     %[2,1,3,4,5,6,7,8,9,10,12,11];  % IR_WR, this is good for IR, but BC odd is strange for WR
%     [1,2,4,3,5,6,7,8,10,9,11,12]; % IR_WR from time stamp
%     %[1,2,3,4,6,5,8,7,9,10,11,12]; % RR_SM (but the Max log files are named SM_RR)
%     [3,4,1,2,7,8,5,6,11,12,9,10]; % SM_RR 
%     [2,1,3,4,6,5,8,7,9,10,11,12]; % XZ_CO
%     ];

% around phrase boundary, we are interested in the three ioi-s
npos = 3; % pb_pre, pb, pb_post
%% score information
score1_aa = load('Score_set1_AA.txt'); %score type 1
score1_bc = load('Score_set1_BC.txt'); %2
score2_aa = load('Score_set2_AA.txt'); %3
score2_bc = load('Score_set2_BC.txt'); %4

score_note_all = [score1_aa score1_bc score2_aa score2_bc];

note_nums_human = [1:31]';
note_nums_Max_HumanFirst = [1:6, 13:18, 25:31]';
note_nums_Max_MaxFirst = [7:12, 19:24 28:31]';

player_notes_1 = [1 1 1 1 1 1 2 2 2 2 2 2 1 1 1 1 1 1 2 2 2 2 2 2 1 1 1]; % note 1-27 to comapre against with Max log files
player_notes_2 = [2 2 2 2 2 2 1 1 1 1 1 1 2 2 2 2 2 2 1 1 1 1 1 1 2 2 2];

%% now read the data and store ioi-s of interest
% all the ioi data (mean for a condition at pre-phrase-border, phrase-border, and post-phrase-boarder) will be stored here
% first we look at the stuff for Human pair files
% second we look at the stuff for Human-Max/Max-Human pair files


%player_file_all = zeros(npair, nblock);
%partner_file_all = zeros(npair, nblock);
scoretype_file_all = zeros(npair,nblock);  % score type number 1-4

order_file_all = zeros(npair, nblock);
task_file_all = zeros(npair, nblock);
MaxPos_file_all=zeros(npair,nblock); % if Max goes 1st:1, Max playes 2nd:2

orderLog_all = zeros(npair, nblock); % this will store the order from Max log files

% to store updated order and task information for each block
order_revised_file_all = size(order_file_all);
task_revised_file_all = size(task_file_all);

% mean-ioi initialized
mioi_all = zeros(nsubj,npartner,ntask,norder,npos);
% number of ioi data
nioi_all = zeros(nsubj,npartner,ntask,norder,npos);

for ipair=1:npair
    sub={pair{ipair,1};pair{ipair,2}};
    pairname = sprintf('%s_%s', sub{1}, sub{2});
    
    %curr_block2cond_mapping = block2cond_mapping(ipair,:);
    
    subjA = sub(1);
    subjB = sub(2);
    isubjA = find(strcmp(pair,subjA)==1);
    isubjB = find(strcmp(pair,subjB)==1);
    
   
    % (1) Human pair Blocks
    % one block at a time -BEGIN
   
     for iblock =5:8    
        curr_dir = sprintf('./%s/trial-%2.2d_*.coll.txt',pairname,iblock);
        dd = dir(curr_dir);
        c = struct2cell(dd);
        cc = c(1,:);
        ncc = size(cc,2);
       
        ipartner = partner_file_all(ipair,iblock);
        iplayer = player_file_all(ipair,iblock);
        
        if iplayer ~= 3
            display('the file description does not match with the number of players');
            continue;
        end
        
        % initialized
        notes_all =[];
        player_notes_all=[];
        ioi_13_all = []; % phrase boundary 1 and 3 - from odd to even player
        ioi_24_all = []; % phrase boundary 2 and 4 - from even to odd player
        
        itrial=0;
        scoretype_all = [];
        init = 0;
        for icc = 1:ncc
            
            % load one trial data
            %filename = sprintf('./%s/trial-%2.2d_%2.2d.coll.txt',pairname,iblock, itrial);
            
            filename = cc{icc};
            %display(sprintf('Reading %s', filename));

            if ~isempty(strfind(filename, '-1.coll')) || ~isempty(strfind(filename, '-2.coll')) % skip the practice trials
                display(sprintf('%s - skipping practice trials',filename)); continue;
            end
                
            t1=load(sprintf('./%s/%s',pairname,filename));
            
            
            % x2 = t1(:,2); % the second column indicating IOI from the onset of the previous note
            
            if size(t1,1)~= 31
                %display(sprintf('pair %d , block %d, trial %d: file contains a wrong number of notes',ipair, iblock, itrial)); continue;
                display(sprintf('%s - Invarid trial - a wrong number of notes',filename))
                continue;end
            
            if init==0
                if sum(t1(1:27,3)'==player_notes_1)==27
                    prev_player_notes = player_notes_1;
                    init=1;
                elseif sum(t1(1:27,3)'==player_notes_2)==27
                    prev_player_notes = player_notes_2;
                    init=1;
                else
                    continue; end
            end
            
                
                
                % midi notes
                notes_all = [notes_all, t1(:,4)];
                
                
                % what is the score? the midi notes matching?
                 [mvalue,id]=max(corr(score_note_all(:,:), t1(:,4)));
                 scoretype_all=[scoretype_all,id];
                 
                %display(mvalue)
                
                if abs(1-mvalue)>0.2
                    continue; 
                % if the midi notes don't exactly match
                end
                
                if ismember(1,t1(:,3)) && ismember(2,t1(:,3))  && sum(t1(1:27,3)'==prev_player_notes) 
                        % good trial
                        % players
                        player_notes_all = [player_notes_all, t1(:,3)];
                
                else
                    continue; 
                end
                
                
                % count the trial because it's a correctly played trial
                itrial = itrial+1;

                
                
                % index for the phrase borders
                idx_13_pb=[1,3]*6+1; % phrase boundary happening from odd to even player
                idx_13_pb_pre = idx_13_pb-1;
                idx_13_pb_post = idx_13_pb+1;
                
                idx_24_pb=[2,4]*6+1; % even to odd player
                idx_24_pb_pre = idx_24_pb-1;
                idx_24_pb_post = idx_24_pb+1;
                
                % the IOI one before, across the border, and one after.
                ioi_13_pb = t1(idx_13_pb,2);
                ioi_13_pb_pre = t1(idx_13_pb_pre,2);
                ioi_13_pb_post = t1(idx_13_pb_post,2);
                
                ioi_24_pb = t1(idx_24_pb,2);
                ioi_24_pb_pre = t1(idx_24_pb_pre,2);
                ioi_24_pb_post = t1(idx_24_pb_post,2);
                
            
            ioi_13_all = [ioi_13_all;[ioi_13_pb_pre, ioi_13_pb, ioi_13_pb_post]];
            ioi_24_all = [ioi_24_all;[ioi_24_pb_pre, ioi_24_pb, ioi_24_pb_post]];
        end % icc
        ntrial=itrial; % store the number of trials which were included
        
        % now look at the ceo files
        curr_file = sprintf('./%s/b%2.2d_evt.txt',pairname,iblock); % made them through do_store_events.sh (awk only cut and store the trigger sequence part of the .ceo file)
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
        if ipartner_file == 1;
            iplayer_file = 3;
        else
            if iblock <5
                iplayer_file = 1;
            elseif iblock > 8
                iplayer_file = 2;
            end
        end
        
        % take most frequent score as this block, because there might
        % be test trials log files left and confusing
        iscoretype_file = mode(scoretype_all);
        if scoretype_file_all(ipair,iblock)==0
            scoretype_file_all(ipair,iblock)=iscoretype_file;
        end
        
        % what about ordering of players?
        for inote = 1:27
            tmp_player_notes(inote)=mode(player_notes_all(inote,:));
        end
        if sum(tmp_player_notes(1:27)==player_notes_1)==27
             tmp_player_order = 1;
        elseif sum(tmp_player_notes(1:27)==player_notes_2)==27
             tmp_player_order =2;
        end
        iorder_revised_file=iorder_file;
        % order info was mistaken in some blocks
%         if  ipair==4 && iblock ==5
%             iorder_revised_file =2;
%         end
        if iorder_file ~= tmp_player_order            
            iorder_revised_file=tmp_player_order;
        end
                    
        % ok, store them
        order_file_all(ipair,iblock)=iorder_file;
        task_file_all(ipair,iblock)=itask_file;
        scoretype_file_all(ipair,iblock)=iscoretype_file;       
        
        order_revised_file_all(ipair,iblock)=iorder_revised_file;
        
        
        
        % now compare the task and scoretype
        % if that does not match, follow the score
        % and make task_revised
        % thus,
        % scoretype 1,3-> 1
        % scoretype 2,4-> 2
        itask_revised_file = ~mod(iscoretype_file,2)+1;
        task_revised_file_all(ipair,iblock)=itask_revised_file;
        
        
        display(iblock)
        display(iorder_revised_file);
        display(itask_revised_file);
        display(iscoretype_file);
        
        if iorder_revised_file == 1 
            %subA serves as odd player, and responsible for the
            %phrase-border 2 and 4
            %subB serves as even player, and responsible for the
            %phrase-border 1 and 3
            myorderA = 1; % odd
            myorderB = 2; % even
            % mioi
            mioi_all(isubjA, ipartner_file, itask_revised_file, myorderA,:)= nanmean(ioi_24_all); % subA is responsible for the pb-ioi
            mioi_all(isubjB, ipartner_file, itask_revised_file, myorderB,:)= nanmean(ioi_13_all);
            % number of data
            nioi_all(isubjA, ipartner_file, itask_revised_file, myorderA,:)= size(ioi_24_all,1); % subA is responsible for the pb-ioi
            nioi_all(isubjB, ipartner_file, itask_revised_file, myorderB,:)= size(ioi_13_all,1);
            
        else
            %subA serves as even player, and responsible for the
            %phrase-border 1 and 3
            %subB serves as odd player, and responsible for the
            %phrase-border 2 and 4
            myorderA = 2; % odd
            myorderB = 1; % even
            % mioi
            mioi_all(isubjA, ipartner_file, itask_revised_file, myorderA,:)= nanmean(ioi_13_all);
            mioi_all(isubjB, ipartner_file, itask_revised_file, myorderB,:)= nanmean(ioi_24_all);
            % number of data
            nioi_all(isubjA, ipartner_file, itask_revised_file, myorderA,:)= size(ioi_13_all,1);
            nioi_all(isubjB, ipartner_file, itask_revised_file, myorderB,:)= size(ioi_24_all,1);
            
        end
        %display(mean(ioi_13_all));
        %display(mean(ioi_24_all));
        
    end % iblock
    
    % (2) Max Blocks
    % one block at a time -BEGIN
    for iblock =[1:4,9:12] %
        
        curr_dir = sprintf('./%s/trial-%2.2d_*.coll.txt',pairname,iblock);
        dd = dir(curr_dir);
        c = struct2cell(dd);
        cc = c(1,:);
        ncc = size(cc,2);
        
        ipartner = partner_file_all(ipair,iblock);
        iplayer = player_file_all(ipair, iblock);
        
        %         if ~any(itask*ipartner*iorder)
        %             continue;
        %         end
        if iplayer == 3
            display('the file description does not match with the number of players');
            continue;
        end
        
        % initialized
        ioi_13_all = []; % phrase boundary 1 and 3 - from odd to even player
        ioi_24_all = []; % phrase boundary 2 and 4 - from even to odd player
        notes_all =[];
        
        itrial=0;
        scoretype_all=[];
        for icc = 1:ncc
            
            % load one trial data
            %filename = sprintf('./%s/trial-%2.2d_%2.2d.coll.txt',pairname,iblock, itrial);
            
            filename = cc{icc};
            %%display(sprintf('Reading %s', filename));
            
            if ~isempty(strfind(filename, '-1.coll')) || ~isempty(strfind(filename, '-2.coll')) % skip the practice trials
                display(sprintf('%s - skipping practice trials',filename)); continue;
            end
            
            t2=load(sprintf('./%s/%s',pairname,filename));
            
            
            if ~(size(t2,1)== 16 || size(t2,1)==19) % because MAX part is absent
                display(sprintf('%s - Invarid trial - a wrong number of notes',filename));
                continue;
            else
                
                t1 = zeros(31,6); % fill the other line
                % fill the Max part
                for ir = 1:31
                    t1(ir,1)=ir;
                    t1(ir,2)=500;
                end
                % now real data
                for ir=1:size(t2,1)
                    t1(t2(ir,1),:)=t2(ir,:);
                end
                
                if size(t2,1)==16 && t2(1,1)==7
                    maxp = 1;
                    MaxPos_file_all(ipair,iblock)=maxp;
                elseif size(t2,1)==19 && t2(1,1)==1
                    maxp = 2;
                    MaxPos_file_all(ipair,iblock)=maxp;
                else
                    % do nothing
                end
                
                % now if MaxPos is not matching with order, revise order
                % for player1, the order number and MaxPos is always
                % opposite.
                % on the other hand, for player2, the order number and
                % MaxPos should be same.
                % If that is not the case, follow MaxPos, and make
                % 'order_revised_file_all'
                
                % player 1
                if cond_subA(iblock)
                    iorder_revised_file = ~(maxp-1)+1;
                    % player 2
                elseif cond_subB(iblock)
                    iorder_revised_file = maxp;
                end
                
                
                % x2 = t1(:,2); % the second column indicating IOI from the onset of the previous note
                
                
                % midi notes
                notes_all = [notes_all, t1(:,4)];
                
                indx=t2(:,1);
                
                % what is the score? the midi notes matching?
                [mvalue,id]=max(corr(score_note_all(indx,:), t1(indx,4)));
                scoretype_all = [scoretype_all, id];
                
                
                
                if abs(1-mvalue)>0.2
                    continue;
                    % if the midi notes don't exactly match
                end
                
                
                % count the trial because it's a correctly played trial
                itrial = itrial+1;
                
                
                % index for the phrase borders
                idx_13_pb=[1,3]*6+1; % phrase boundary happening from odd to even player
                idx_13_pb_pre = idx_13_pb-1;
                idx_13_pb_post = idx_13_pb+1;
                
                idx_24_pb=[2,4]*6+1; % even to odd player
                idx_24_pb_pre = idx_24_pb-1;
                idx_24_pb_post = idx_24_pb+1;
                
                % the IOI one before, across the border, and one after.
                ioi_13_pb = t1(idx_13_pb,2);
                ioi_13_pb_pre = t1(idx_13_pb_pre,2);
                ioi_13_pb_post = t1(idx_13_pb_post,2);
                
                ioi_24_pb = t1(idx_24_pb,2);
                ioi_24_pb_pre = t1(idx_24_pb_pre,2);
                ioi_24_pb_post = t1(idx_24_pb_post,2);
                
            end % if
            ioi_13_all = [ioi_13_all;[ioi_13_pb_pre, ioi_13_pb, ioi_13_pb_post]];
            ioi_24_all = [ioi_24_all;[ioi_24_pb_pre, ioi_24_pb, ioi_24_pb_post]];
        end % icc
        ntrial=itrial; % store the number of trials which were included
        
        % now look at the ceo files
        curr_file = sprintf('./%s/b%2.2d_evt.txt',pairname,iblock); % made them through do_store_events.sh (awk only cut and store the trigger sequence part of the .ceo file)
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
        if ipartner_file == 1;
            iplayer_file = 3;
        else
            if iblock <5
                iplayer_file = 1;
            elseif iblock > 8
                iplayer_file = 2;
            end
        end
        
        % take most frequent score as this block, because there might
        % be test trials log files left and confusing
        iscoretype_file = mode(scoretype_all);
        if scoretype_file_all(ipair,iblock)==0
            scoretype_file_all(ipair,iblock)=iscoretype_file;
        end
        
        
        
        % ok, store them
        order_file_all(ipair,iblock)=iorder_file;
        task_file_all(ipair,iblock)=itask_file;
        scoretype_file_all(ipair,iblock)=iscoretype_file;
        
        order_revised_file_all(ipair,iblock)=iorder_revised_file;
        
        % now compare the task and scoretype
        % if that does not match, follow the score
        % and make task_revised
        % thus,
        % scoretype 1,3-> 1
        % scoretype 2,4-> 2
        itask_revised_file = ~mod(iscoretype_file,2)+1;
        task_revised_file_all(ipair,iblock)=itask_revised_file;
        
        display(iblock)
        display(iorder_revised_file);
        display(itask_revised_file);
        display(iscoretype_file);
        
        %display(iblock)
        if cond_subA(iblock) % whether this is the real player, the other one is MAX (as subB)
            %display([iorder,isubjA])
            if iorder_revised_file == 1 
                %subA serves as odd player, and responsible for the
                %phrase-border 2 and 4
                %subB serves as even player, and responsible for the
                %phrase-border 1 and 3
                % but this case subB is Max
                myorderA = 1; % odd
               
                %display(mean(ioi_24_all));
                mioi_all(isubjA, ipartner_file, itask_revised_file, myorderA,:)= nanmean(ioi_24_all);
                nioi_all(isubjA, ipartner_file, itask_revised_file, myorderA,:)= size(ioi_24_all,1);
                
            else
                %subA serves as even player, and responsible for the
                %phrase-border 1 and 3
                %subB serves as odd player, and responsible for the
                %phrase-border 2 and 4
                % but this case subB is Max 
                myorderA = 2; % even
                %display(mean(ioi_13_all));
                mioi_all(isubjA, ipartner_file, itask_revised_file, myorderA,:)= nanmean(ioi_13_all);
                nioi_all(isubjA, ipartner_file, itask_revised_file, myorderA,:)= size(ioi_13_all,1);
            end
        elseif cond_subB(iblock) % whether this is the real player, the other one is MAX (as subA)
                
            
            %display([iorder,isubjB])
            if iorder_revised_file == 1 % subA serves as odd player,subB serves even player
                %subA serves as odd player, and responsible for the
                %phrase-border 2 and 4
                %subB serves as even player, and responsible for the
                %phrase-border 1 and 3
                % but this case subA is Max 
                myorderB = 2; % even
                %display(ioi_13_all');
                mioi_all(isubjB, ipartner_file, itask_revised_file, myorderB,:)= nanmean(ioi_13_all);
                nioi_all(isubjB, ipartner_file, itask_revised_file, myorderB,:)= size(ioi_13_all,1);
            else % subA serves as even player, subB serves odd player
                %subA serves as even player, and responsible for the
                %phrase-border 1 and 3
                %subB serves as odd player, and responsible for the
                %phrase-border 2 and 4
                % but this case subA is Max 
                myorderB = 1; % odd
                %display(ioi_24_all');
                mioi_all(isubjB, ipartner_file, itask_revised_file, myorderB,:)= nanmean(ioi_24_all);
                nioi_all(isubjB, ipartner_file, itask_revised_file, myorderB,:)= size(ioi_24_all,1);
            end
        end
        
    end % iblock
    
    
end % pair

save('calc_diff_IOI_data');

%% do stats
%%  (1) comparison between AA and BC
do_stats1 =1;
if do_stats1 == 1
ssubj = [1,2,4,5,6,7,8,9]; % CO (10) didnot finish 1 of Max blocks 
nssubj = size(ssubj,2);
% hypothesis  
% 1) pb in AA <  pb in BC 
%   bar plot of means with error-bar (SEM standard error of mean)

% partnered with human
tmpAA_h = nanmean(mioi_all(ssubj,1,1,:,2),4);
tmpBC_h = nanmean(mioi_all(ssubj,1,2,:,2),4);

% partnered with MAX
tmpAA_m = nanmean(mioi_all(ssubj,2,1,:,2),4);
tmpBC_m = nanmean(mioi_all(ssubj,2,2,:,2),4);

% draw
Means=[nanmean(tmpAA_h),nanmean(tmpAA_m);nanmean(tmpBC_h),nanmean(tmpBC_m)];
SEMs=[nanstd(tmpAA_h)/sqrt(length(tmpAA_h)),nanstd(tmpAA_m)/sqrt(length(tmpAA_m));
   nanstd(tmpBC_h)/sqrt(length(tmpBC_h)),nanstd(tmpBC_m)/sqrt(length(tmpBC_m))];
errorbar_groups(Means, SEMs) ;
legend('AA','BC')
xlabel('Human-partner vs. Max-partner');
ylabel('IOI at the phrase boundary before the players 1st note');

% anova
score_all = [tmpAA_h; tmpBC_h; tmpAA_m; tmpBC_m];

partner_index = [];
task_index = [];
subj_index = [];
for ipartner = 1:npartner
for itask=1:2
    for isubj = 1:nssubj       
        partner_index = [partner_index;ipartner];
        task_index = [task_index; itask];
        subj_index = [subj_index;isubj];
    end
end
end


% prepare data matrix 
X = [score_all, partner_index, task_index, subj_index];
display('IV1 is Human vs. Max')
display('IV2 is AA vs. BC')


    
rmaov2(X);
% subj 1-9
% IV1 is Human vs. Max
% % IV2 is AA vs. BC
% IV1 is Human vs. Max
% IV2 is AA vs. BC
% The number of IV1 levels are: 2
% 
% The number of IV2 levels are: 2
% 
% The number of subjects are: 9
% 
% Repeated Measures Two-Way Analysis of Variance Table.
% ---------------------------------------------------------------------------
% SOV                  SS          df           MS             F        P
% ---------------------------------------------------------------------------
% Subjects         3236.354         8        404.544[        2.568   0.0352]
% 
% IV1              2868.691         1       2868.691        14.685   0.0050
% 
% Error(IV1)       1562.827         8        195.353
% 
% IV2                15.728         1         15.728         0.080   0.7843
% 
% Error(IV2)       1570.473         8        196.309
% 
% IV1xIV2           105.639         1        105.639         1.305   0.2864
% 
% Error(IV1xIV2)    647.748         8         80.969
% 
% [Error           3781.048        24        157.544]
% 
% Total           10007.460        35
% 
% ---------------------------------------------------------------------------
% If the P results are smaller than 0.05
% the corresponding Ho's tested result statistically significant. Otherwise, are not significative.
% [Generally speaking, no Mean Square is computed for the variable "subjects" since it is assumed
% that subjects differ from one another thus making a significance test of "subjects" superfluous.
% However, for all the interested people we are given it anyway].
%   
% The percentage of the variability in the DV associated with the IV1 (eta squared) is 64.73
% (After the effects of individual differences have been removed).
%   
% The percentage of the variability in the DV associated with the IV2 (eta squared) is 0.99
% (After the effects of individual differences have been removed).

% subj 1,2,4,5,6,7,8,9
% IV1 is Human vs. Max
% IV2 is AA vs. BC
% The number of IV1 levels are: 2
% 
% The number of IV2 levels are: 2
% 
% The number of subjects are: 8
% 
% Repeated Measures Two-Way Analysis of Variance Table.
% ---------------------------------------------------------------------------
% SOV                  SS          df           MS             F        P
% ---------------------------------------------------------------------------
% Subjects         3099.079         7        442.726[        2.613   0.0416]
% 
% IV1              2571.729         1       2571.729        11.522   0.0115
% 
% Error(IV1)       1562.410         7        223.201
% 
% IV2                17.734         1         17.734         0.079   0.7866
% 
% Error(IV2)       1568.466         7        224.067
% 
% IV1xIV2           214.416         1        214.416         3.515   0.1029
% 
% Error(IV1xIV2)    426.989         7         60.998
% 
% [Error           3557.866        21        169.422]
% 
% Total            9460.824        31
% 
% ---------------------------------------------------------------------------

%  post-hoc ttest 

end % if do_stats


%% (1.2) adding the order (which (odd/even) phrase you are in) -> if you
%% are odd player you are the leader.


do_stats2 =1;
if do_stats2 == 1
ssubj = [1,2,4,5,6,7,8,9]; % CO (10) didnot finish 1 Max block & WR(8)'s Max -1 block strange 
nssubj = size(ssubj,2);
% hypothesis  
% 1) pb in AA <  pb in BC 
%   bar plot of means with error-bar (SEM standard error of mean)

% partnered with human
tmpAA_h1 = nanmean(mioi_all(ssubj,1,1,1,2),4);
tmpAA_h2 = nanmean(mioi_all(ssubj,1,1,2,2),4);
tmpBC_h1 = nanmean(mioi_all(ssubj,1,2,1,2),4);
tmpBC_h2 = nanmean(mioi_all(ssubj,1,2,2,2),4);

% partnered with MAX
tmpAA_m1 = nanmean(mioi_all(ssubj,2,1,1,2),4);
tmpAA_m2 = nanmean(mioi_all(ssubj,2,1,2,2),4);
tmpBC_m1 = nanmean(mioi_all(ssubj,2,2,1,2),4);
tmpBC_m2 = nanmean(mioi_all(ssubj,2,2,2,2),4);

% draw
Means=[nanmean(tmpAA_h1),nanmean(tmpAA_h2),nanmean(tmpAA_m1),nanmean(tmpAA_m2);nanmean(tmpBC_h1),nanmean(tmpBC_h2),nanmean(tmpBC_m1),nanmean(tmpBC_m2)];
SEMs=[nanstd(tmpAA_h1)/sqrt(length(tmpAA_h1)),nanstd(tmpAA_h2)/sqrt(length(tmpAA_h2)),nanstd(tmpAA_m1)/sqrt(length(tmpAA_m1)),nanstd(tmpAA_m2)/sqrt(length(tmpAA_m2));
   nanstd(tmpBC_h1)/sqrt(length(tmpBC_h1)),nanstd(tmpBC_h2)/sqrt(length(tmpBC_h2)),nanstd(tmpBC_m1)/sqrt(length(tmpBC_m1)),nanstd(tmpBC_m2)/sqrt(length(tmpBC_m2))];
errorbar_groups(Means, SEMs) ;
legend('AA','BC')
xlabel('Human-partner (leader, follower) vs. Max-partner (leader, follower)');
ylabel('IOI at the phrase boundary before the players 1st note');

% anova
score_all = [tmpAA_h1; tmpAA_h2; tmpBC_h1; tmpBC_h2;tmpAA_m1; tmpAA_m2;tmpBC_m1;tmpBC_m2];

partner_index = [];
task_index = [];
role_index = [];
subj_index = [];
for ipartner = 1:npartner
for itask=1:2 % melody
    for irole = 1:2
        
        for isubj = 1:nssubj       
            partner_index = [partner_index;ipartner];
            task_index = [task_index; itask];
            role_index = [role_index;irole];
            subj_index = [subj_index;isubj];
        end
    end
end
end


% prepare data matrix 
X = [score_all, partner_index, task_index, role_index, subj_index];
display('IV1 is Human vs. Max')
display('IV2 is AA vs. BC')
display('IV3 is leader vs. follower')

    
rmaov33(X);
% IV1 is Human vs. Max
% IV2 is AA vs. BC
% IV3 is leader vs. follower
%    
% The number of IV1 levels are: 2
% The number of IV2 levels are: 2
% The number of IV3 levels are: 2
% The number of subjects are:    9
% 
% Three-Way Analysis of Variance With Repeated Measures on Three Factors (Within-Subjects) Table.
% ---------------------------------------------------------------------------------------------------
% SOV                             SS          df           MS             F        P      Conclusion
% ---------------------------------------------------------------------------------------------------
% Between-Subjects            6472.708         8
% 
% Within-Subjects            18591.597        63
% IV1                         5737.381         1       5737.381        14.685   0.0050        S
% Error(IV1)                  3125.655         8        390.707
% 
% IV2                           31.455         1         31.455         0.080   0.7843       NS
% Error(IV2)                  3140.946         8        392.618
% 
% IV3                            5.700         1          5.700         0.040   0.8474       NS
% Error(IV3)                  1153.978         8        144.247
% 
% IV1xIV2                      211.278         1        211.278         1.305   0.2864       NS
% Error(IV1xIV2)              1295.496         8        161.937
% 
% IV1xIV3                       88.839         1         88.839         0.733   0.4169       NS
% Error(IV1xIV3)               969.894         8        121.237
% 
% IV2xIV3                      182.710         1        182.710         0.891   0.3729       NS
% Error(IV2-IV3)              1640.647         8        205.081
% 
% IV1xIV2xIV3                  156.202         1        156.202         1.639   0.2364       NS
% Error(IV1-IV2-IV3)           762.577         8         95.322
% ---------------------------------------------------------------------------------------------------
% Total                      24975.466        71
% ---------------------------------------------------------------------------------------------------
% With a given significance level of: 0.05
% The results are significant (S) or not significant (NS).

% %  post-hoc ttest 
% [h, p, ci, stats]=ttest(tmpAA_h, tmpBC_h)
% [nanmean(tmpAA_h), nanmean(tmpBC_h)] 
% 
% 
% [h, p, ci, stats]=ttest(tmpAA_m, tmpBC_m)
% [nanmean(tmpAA_m), nanmean(tmpBC_m)] 
% 
% 
% % interaction
% [h, p, ci, stats]=ttest(tmpAA_h-tmpBC_h, tmpAA_m-tmpBC_m)
% [nanmean(tmpAA_h-tmpBC_h), nanmean(tmpAA_m-tmpBC_m)]  

end % if do_stats

 [h,p,ci,stats]=ttest(tmpAA_m1, tmpAA_m2)
% 
% h =
% 
%      1
% 
% 
% p =
% 
%     0.0163
% 
% 
% ci =
% 
%   -13.7186
%    -1.8628
% 
% 
% stats = 
% 
%     tstat: -3.0306
%        df: 8
%        sd: 7.7119

%% (1.3)
 
tmpAA_h_pb=mioi_all(ssubj,1,1,1,2);
tmpAA_h_postpb=mioi_all(ssubj,1,1,1,3);

tmpBC_h_pb=mioi_all(ssubj,1,2,1,2);
tmpBC_h_postpb=mioi_all(ssubj,1,2,1,3);

tmpAA_m_pb=mioi_all(ssubj,2,1,1,2);
tmpAA_m_postpb=mioi_all(ssubj,2,1,1,3);

tmpBC_m_pb=mioi_all(ssubj,2,2,1,2);
tmpBC_m_postpb=mioi_all(ssubj,2,2,1,3);



% anova
score_all = [tmpAA_h_pb; tmpAA_h_postpb; tmpBC_h_pb; tmpBC_h_postpb;tmpAA_m_pb; tmpAA_m_postpb; tmpBC_m_pb; tmpBC_m_postpb];

partner_index = [];
task_index = [];
pos_index=[]
subj_index = [];
for ipartner = 1:npartner
for itask=1:2
    for ipos=1:2
    for isubj = 1:nssubj       
        partner_index = [partner_index;ipartner];
        task_index = [task_index; itask];
        pos_index = [pos_index;ipos];
        subj_index = [subj_index;isubj];
    end
end
end
end



% prepare data matrix 
X = [score_all, partner_index, task_index, pos_index,subj_index];
display('IV1 is Human vs. Max')
display('IV2 is AA vs. BC')
display('IV3 is position (pb, and post-pb')

    
rmaov33(X);
% The number of IV1 levels are: 2
% The number of IV2 levels are: 2
% The number of IV3 levels are: 2
% The number of subjects are:    9
% 
% Three-Way Analysis of Variance With Repeated Measures on Three Factors (Within-Subjects) Table.
% ---------------------------------------------------------------------------------------------------
% SOV                             SS          df           MS             F        P      Conclusion
% ---------------------------------------------------------------------------------------------------
% Between-Subjects            3043.233         8
% 
% Within-Subjects            21481.864        63
% IV1                         4651.151         1       4651.151        15.025   0.0047        S
% Error(IV1)                  2476.416         8        309.552
% 
% IV2                           77.801         1         77.801         0.151   0.7076       NS
% Error(IV2)                  4118.129         8        514.766
% 
% IV3                         3663.604         1       3663.604        16.334   0.0037        S
% Error(IV3)                  1794.302         8        224.288
% 
% IV1xIV2                      266.491         1        266.491         1.122   0.3204       NS
% Error(IV1xIV2)              1900.133         8        237.517
% 
% IV1xIV3                        3.532         1          3.532         0.026   0.8763       NS
% Error(IV1xIV3)              1093.087         8        136.636
% 
% IV2xIV3                      279.860         1        279.860        14.425   0.0053        S
% Error(IV2-IV3)               155.206         8         19.401
% 
% IV1xIV2xIV3                  114.681         1        114.681         1.038   0.3381       NS
% Error(IV1-IV2-IV3)           883.941         8        110.493
% ---------------------------------------------------------------------------------------------------
% Total                      24521.565        71
% ---------------------------------------------------------------------------------------------------
% With a given significance level of: 0.05
% The results are significant (S) or not significant (NS).


[mean(tmpAA_h_pb), mean(tmpAA_h_postpb)]
[mean(tmpBC_h_pb), mean(tmpBC_h_postpb)]

[mean(tmpAA_m_pb), mean(tmpAA_m_postpb)]
[mean(tmpBC_m_pb), mean(tmpBC_m_postpb)]

[h,p,ci,stats]=ttest(tmpAA_h_pb, tmpAA_h_postpb)
[h,p,ci,stats]=ttest(tmpBC_h_pb, tmpBC_h_postpb)

[h,p,ci,stats]=ttest(tmpAA_m_pb, tmpAA_m_postpb)
[h,p,ci,stats]=ttest(tmpBC_m_pb, tmpBC_m_postpb)
% IV2xIV3
% at each position (IV3), compare two melody task condition (IV2)
for ipos=1:2
    indx1=find(X(:,4)==ipos & X(:,3)==1);
    v1=X(indx1);
    indx2=find(X(:,4)==ipos & X(:,3)==2);
    v2=X(indx2);
     curr_pos = ipos;
    display(curr_pos)
    display([mean(v1),mean(v2)])
    [h,p,ci,stats]=ttest(v1,v2) % one-sample
end
% curr_pos =
% 
%      1
% 
% 
% ans =
% 
%   495.7771  497.6412
% 
% 
% h =
% 
%      0
% 
% 
% p =
% 
%     0.7201
% 
% 
% ci =
% 
%   -12.6580
%     8.9299
% 
% 
% stats = 
% 
%     tstat: -0.3644
%        df: 17
%        sd: 21.7056
% 
% 
% curr_pos =
% 
%      2
% 
% 
% ans =
% 
%   485.4537  479.4316
% 
% 
% h =
% 
%      0
% 
% 
% p =
% 
%     0.2208
% 
% 
% ci =
% 
%    -3.9732
%    16.0174
% 
% 
% stats = 
% 
%     tstat: 1.2711
%        df: 17
%        sd: 20.0996

% IV2xIV3
% at each of melody task conditions, compare two positions
for itask=1:2
    indx1=find(X(:,4)==1 & X(:,3)==itask);
    v1=X(indx1);
    indx2=find(X(:,4)==2 & X(:,3)==itask);
    v2=X(indx2);
    curr_task = itask;
    display(curr_task)
    display([mean(v1),mean(v2)])
    [h,p,ci,stats]=ttest(v1,v2) % one-sample
end
% curr_task =
% 
%      1
% 
% 
% ans =
% 
%   495.7771  485.4537
% 
% 
% h =
% 
%      1
% 
% 
% p =
% 
%    4.3347e-04
% 
% 
% ci =
% 
%     5.3190
%    15.3279
% 
% 
% stats = 
% 
%     tstat: 4.3522
%        df: 17
%        sd: 10.0636
% 
% 
% curr_task =
% 
%      2
% 
% 
% ans =
% 
%   497.6412  479.4316
% 
% 
% h =
% 
%      1
% 
% 
% p =
% 
%    9.4389e-04
% 
% 
% ci =
% 
%     8.5851
%    27.8341
% 
% 
% stats = 
% 
%     tstat: 3.9918
%        df: 17
%        sd: 19.3540




%% (2) variation across the three ioi positions 
% might be less in the AA compared to BC

%% (3) variation across the three ioi positions 
% might be less in the Max compared to Human 


