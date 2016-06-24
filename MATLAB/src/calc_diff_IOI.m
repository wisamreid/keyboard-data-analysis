% calc_diff_IOI.m
% for Duet behavioural (MAX recorded log files) data
% 2016 April by Takako Fujioka
% last modified 2016 June 12 by Takako Fujioka


%% definition of all the conditions
clear all
task = {'AA'; 'BC'};
ntask = size(task,1);

partner = {'Human';'Max'};
npartner = size(partner,1);

order = {'odd';'even'};
norder = size(order,1);

% I made this with scan_ceo.m (reading Curry ceo files and re-construct from triggers)
load('condition_block.mat','partner_file_all', 'order_file_all', 'task_file_all')


cond_subA =         [1,1,1,1,1,1,1,1,0,0,0,0];
cond_subB =         [0,0,0,0,1,1,1,1,1,1,1,1];


% condition 1-12 means:
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

block2cond_mapping = [
    [4,3,2,1,8,7,6,5,11,12,9,10]; % MH_CN from block-order.txt
    %[2,1,4,3,6,5,8,7,10,9,12,11]; % TD_NG from the block-order.txt, but
    [2,1,4,3,6,5,8,7,9,10, 11,12]; % for TD_NG, this is the correct mapping
    %[2,1,4,3,5,6,7,8,9,10,12,11]; % IR_WR, block_order1 except the last two from block_order2
    [2,1,3,4,5,6,7,8,9,10,12,11];  % IR_WR, this is good for IR, but BC odd is strange for WR
    %[1,2,3,4,6,5,8,7,9,10,11,12]; % RR_SM (but the Max log files are named SM_RR)
    [1,2,3,4,6,5,8,7,10,9,11,12]; % SM_RR (this is the correct one)
    [2,1,3,4,6,5,8,7,9,10,11,12]; % XZ_CO
    ];

% around phrase boundary, we are interested in the three ioi-s
npos = 3; % pb_pre, pb, pb_post



%% now read the data and store ioi-s of interest
% all the ioi data (mean for a condition) will be stored here
% first we look at the stuff for Human pair files
% second we look at the stuff for Max-Human pair files

% mean-ioi initialized
mioi_all = zeros(nsubj,npartner,ntask,norder,npos);
% number of ioi data
nioi_all = zeros(nsubj,npartner,ntask,norder,npos);
for ipair=5%:npair
    sub={pair{ipair,1};pair{ipair,2}};
    pairname = sprintf('%s_%s', sub{1}, sub{2});
    
    curr_block2cond_mapping = block2cond_mapping(ipair,:);
    
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
        ntrial = ncc-2;  % this many trials collected in this particluar block without -1 and -2 (practice trials)
        icond=curr_block2cond_mapping(iblock);
        itask = task_file_all(ipair, icond);
        iorder = order_file_all(ipair,icond);
        ipartner = partner_file_all(ipair,icond);
        
        % initialized
        ioi_13_all = []; % phrase boundary 1 and 3 - from odd to even player
        ioi_24_all = []; % phrase boundary 2 and 4 - from even to odd player
        for itrial = 1:ntrial
            
            % load one trial data
            filename = sprintf('./%s/trial-%2.2d_%2.2d.coll.txt',pairname,iblock, itrial);
            %%display(sprintf('Reading %s', filename));
            
            if ~exist(filename)
                display(sprintf('pair %d , block %d, trial %d: file missing',ipair, iblock, itrial)); continue;
            end
            
            t1=load(filename);
            % x2 = t1(:,2); % the second column indicating IOI from the onset of the previous note
            
            if size(t1)~= [31,6]
                display(sprintf('pair %d , block %d, trial %d: file contains a wrong number of notes',ipair, iblock, itrial)); continue;
            else
                % index
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
        end % trial
        
        %display(iblock)
        if iorder == 1 %subA serves as odd player,
            % mioi
            mioi_all(isubjA, ipartner, itask, iorder,:)= nanmean(ioi_24_all); % subA is responsible for the pb-ioi
            mioi_all(isubjB, ipartner, itask, iorder,:)= nanmean(ioi_13_all);
            % number of data
            nioi_all(isubjA, ipartner, itask, iorder,:)= size(ioi_24_all,1); % subA is responsible for the pb-ioi
            nioi_all(isubjB, ipartner, itask, iorder,:)= size(ioi_13_all,1);
            
        else % subA serves as even player
            % mioi
            mioi_all(isubjA, ipartner, itask, iorder,:)= nanmean(ioi_13_all);
            mioi_all(isubjB, ipartner, itask, iorder,:)= nanmean(ioi_24_all);
            % number of data
            nioi_all(isubjA, ipartner, itask, iorder,:)= size(ioi_13_all,1);
            nioi_all(isubjB, ipartner, itask, iorder,:)= size(ioi_24_all,1);
            
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
        ntrial = ncc-2;  % this many trials collected in this particluar block without -1 and -2 (practice trials)
        
        icond=curr_block2cond_mapping(iblock);
        itask = task_file_all(ipair, icond);
        iorder = order_file_all(ipair,icond);
        ipartner = partner_file_all(ipair,icond);

        % initialized
        ioi_13_all = []; % phrase boundary 1 and 3 - from odd to even player
        ioi_24_all = []; % phrase boundary 2 and 4 - from even to odd player
        for itrial = 1:ntrial
            
            % load one trial data
            filename = sprintf('./%s/trial-%2.2d_%2.2d.coll.txt',pairname,iblock, itrial);
            %%display(sprintf('Reading %s', filename));
            if ~exist(filename)
                display(sprintf('pair %d , block %d, trial %d: file missing',ipair, iblock, itrial));continue;
            end
            if itrial ==1
                display(iblock);
                display(iorder);
                t2=load(filename);
            end
            
            if size(t2)~= [16,6] % because MAX part is absent
                display(sprintf('pair %d , block %d, trial %d: file contains a wrong number of notes',ipair, iblock, itrial)); continue;
            else
                
                t1 = zeros(31,6); % fill the other line
                % fill the Max part
                for ir = 1:31
                    t1(ir,1)=ir;
                    t1(ir,2)=500;
                end
                % now real data
                for ir=1:16
                    t1(t2(ir,1),:)=t2(ir,:);
                end
                
                % index
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
        end % trial
        
        %display(iblock)
        if cond_subA(iblock) % whether this is the real player, the other one is MAX (as subB)
            %display([iorder,isubjA])
            if iorder == 1 % subA serves as odd player,
                %display(mean(ioi_24_all));
                mioi_all(isubjA, ipartner, itask, iorder,:)= nanmean(ioi_24_all);
                nioi_all(isubjA, ipartner, itask, iorder,:)= size(ioi_24_all,1);
                
            else % subA serves as even player
                %display(mean(ioi_13_all));
                mioi_all(isubjA, ipartner, itask, iorder,:)= nanmean(ioi_13_all);
                nioi_all(isubjA, ipartner, itask, iorder,:)= size(ioi_13_all,1);
            end
        elseif cond_subB(iblock) % whether this is the real player, the other one is MAX (as subA)
            %display([iorder,isubjB])
            if iorder == 1 % subA serves as odd player,subB serves even player
                display(ioi_13_all');
                mioi_all(isubjB, ipartner, itask, iorder,:)= nanmean(ioi_13_all);
                nioi_all(isubjB, ipartner, itask, iorder,:)= size(ioi_13_all,1);
            else % subA serves as even player, subB serves odd player
                display(ioi_24_all');
                mioi_all(isubjB, ipartner, itask, iorder,:)= nanmean(ioi_24_all);
                nioi_all(isubjB, ipartner, itask, iorder,:)= size(ioi_24_all,1);
            end
        end
        
    end % iblock
    
    
end % pair

%% do stats
%%  (1) comparison between AA and BC

ssubj = [1,2,3,4,5,6,7,9]; % CO (10) didnot finish 1 Max block & WR(8)'s Max -1 block broken 
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
% IV1 is Human vs. Max
% IV2 is AA vs. BC
% The number of IV1 levels are: 2
% 
% The number of IV2 levels are: 2
% 
% The number of subjects are:10
% 
% Repeated Measures Two-Way Analysis of Variance Table.
% ---------------------------------------------------------------------------
% SOV                  SS          df           MS             F        P
% ---------------------------------------------------------------------------
% Subjects         4799.486         9        533.276[        4.051   0.0022]
% 
% IV1              3464.664         1       3464.664        17.838   0.0022
% 
% Error(IV1)       1748.052         9        194.228
% 
% IV2               319.415         1        319.415         3.556   0.0920
% 
% Error(IV2)        808.493         9         89.833
% 
% IV1xIV2           235.965         1        235.965         2.128   0.1786
% 
% Error(IV1xIV2)    997.839         9        110.871
% 
% [Error           3554.385        27        131.644]
% 
% Total           12373.914        39
% 
% ---------------------------------------------------------------------------
% If the P results are smaller than 0.05
% the corresponding Ho's tested result statistically significant. Otherwise, are not significative.
% [Generally speaking, no Mean Square is computed for the variable "subjects" since it is assumed
% that subjects differ from one another thus making a significance test of "subjects" superfluous.
% However, for all the interested people we are given it anyway].
%   
% The percentage of the variability in the DV associated with the IV1 (eta squared) is 66.47
% (After the effects of individual differences have been removed).
%   
% The percentage of the variability in the DV associated with the IV2 (eta squared) is 28.32
% (After the effects of individual differences have been removed).

%  post-hoc ttest 
[h, p, ~, stats]=ttest(tmpAA_h, tmpBC_h)
[nanmean(tmpAA_h), nanmean(tmpBC_h)] % 478.9432  489.4525
% h =
% 
%      0
% 
% 
% p =
% 
%     0.0814
% 
% 
% stats = 
% 
%     tstat: -1.9621
%        df: 9
%        sd: 16.9377

[h, p, ~, stats]=ttest(tmpAA_m, tmpBC_m)
[nanmean(tmpAA_m), nanmean(tmpBC_m)]  % 502.4145  503.2085

% h =
% 
%      0
% 
% 
% p =
% 
%     0.8197
% 
% 
% stats = 
% 
%     tstat: -0.2346
%        df: 9
%        sd: 10.7015

% interaction
[h, p, ~, stats]=ttest(tmpAA_h-tmpBC_h, tmpAA_m-tmpBC_m)
[nanmean(tmpAA_h-tmpBC_h), nanmean(tmpAA_m-tmpBC_m)]  
% h =
% 
%      0
% 
% 
% p =
% 
%     0.1786
% 
% 
% stats = 
% 
%     tstat: -1.4589
%        df: 9
%        sd: 21.0591
% 
% 
% ans =
% 
%   -10.5093   -0.7941

% without 10

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
% Subjects         3608.966         8        451.121[        3.560   0.0074]
% 
% IV1              2540.663         1       2540.663        13.993   0.0057
% 
% Error(IV1)       1452.570         8        181.571
% 
% IV2               464.951         1        464.951         6.239   0.0371
% 
% Error(IV2)        596.187         8         74.523
% 
% IV1xIV2           233.506         1        233.506         1.882   0.2074
% 
% Error(IV1xIV2)    992.826         8        124.103
% 
% [Error           3041.583        24        126.733]
% 
% Total            9889.668        35
% 
% ---------------------------------------------------------------------------
% If the P results are smaller than 0.05
% the corresponding Ho's tested result statistically significant. Otherwise, are not significative.
% [Generally speaking, no Mean Square is computed for the variable "subjects" since it is assumed
% that subjects differ from one another thus making a significance test of "subjects" superfluous.
% However, for all the interested people we are given it anyway].
%   
% The percentage of the variability in the DV associated with the IV1 (eta squared) is 63.62
% (After the effects of individual differences have been removed).
%   
% The percentage of the variability in the DV associated with the IV2 (eta squared) is 43.82
% (After the effects of individual differences have been removed).
%   
% 
% h =
% 
%      0
% 
% 
% p =
% 
%     0.0615
% 
% 
% stats = 
% 
%     tstat: -2.1732
%        df: 8
%        sd: 16.9536
% 
% 
% ans =
% 
%   480.7818  493.0630
% 
% 
% h =
% 
%      0
% 
% 
% p =
% 
%     0.5655
% 
% 
% stats = 
% 
%     tstat: -0.5994
%        df: 8
%        sd: 10.4799
% 
% 
% ans =
% 
%   502.6771  504.7710
% 
% 
% h =
% 
%      0
% 
% 
% p =
% 
%     0.2074
% 
% 
% stats = 
% 
%     tstat: -1.3717
%        df: 8
%        sd: 22.2803
% 
% 
% ans =
% 
%   -12.2812   -2.0939


%% (2) variation across the three ioi positions 
% might be less in the AA compared to BC

%% (3) variation across the three ioi positions 
% might be less in the Max compared to Human 



