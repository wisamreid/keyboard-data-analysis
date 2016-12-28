clc
% a = [6 9 11 13 15 17 19 21 23 25]
% a = [6 12 18 21 23 25 27 29 31]

% a = [6 12 18 21 23 25 27 29 31 34 36 38 40 44 46]
% % expecting [21 23 25 27 29 34 36 38 44 46]

a = [6 12 18 21 23 25 27 29 31 34 36 38 40 44 46 50]
% expecting [21 23 25 27 29 34 36 38 44 46]

b = a(find(a(2:end)-a(1:end-1)==2))

% % include final trial?
% if a(end) - a(end - 1) == 2
%     b = [b a(end)]
% end

[~,start] = ismember(b(2),a)

c = a(start:end)
%%
clc

a = [6 12 18 21 23 25 27 29 31 34 36 38 40 44 46 50]

[~,idx] = ismember(21,a)

