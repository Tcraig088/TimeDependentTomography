function [obj] = LoadMetaData(dir)
%LOADMETADATA Summary of this function goes here
%   Detailed explanation goes here
    data = load(dir);
    obj = data.obj;
    [obj.dir,~,~] = fileparts(dir);
    [obj.dir,~] = fileparts(obj.dir);
    save(dir,'obj');
end

