function [path] = getname(params,i)
%GETNAME Summary of this function goes here
%   Detailed explanation goes here
    if nargin < 2
        path = fullfile(params.dir,'vol\0_vol_init.rec');
    else
        path = strcat(num2str(i),'_vol_sim.rec');
        path = fullfile(params.dir,'vol',path);
    end
end

