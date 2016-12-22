function [  ] = runHere( input_args )
% Author: Wisam Reid
% Sets your working directory and loads all subdirectories of the
% parent folder (of the calling script)
tmp = matlab.desktop.editor.getActive;
file = tmp.Filename;
cd(fileparts(file));
file(find(file=='/',1,'last'):end) = [];
addpath(genpath(file))
end

