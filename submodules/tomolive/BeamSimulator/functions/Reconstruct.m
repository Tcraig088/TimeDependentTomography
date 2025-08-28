function [out] = Reconstruct(dir,sub_dir, func,data, params)
%RECONSTRUCT Summary of this function goes here
%   Detailed explanation goes here
	N = size(params,2);
	switch N
        case 0
            rec = func(data);
        case 1
            rec = func(data,params(1));
        case 2
        	rec = func(data,params(1),params(2));
        case 3
        	rec = func(data,params(1),params(2),params(3));
        case 4
        	rec = func(data,params(1),params(2),params(3),params(4));
        case 5
        	rec = func(data,params(1),params(2),params(3),params(4),params(5));
        case 6
        	rec = func(data,params(1),params(2),params(3),params(4),params(5),params(6));
        case 7
        	rec = func(data,params(1),params(2),params(3),params(4),params(5),params(6),params(7));
        case 8
        	rec = func(data,params(1),params(2),params(3),params(4),params(5),params(6),params(7),params(8));
        otherwise
        	error('The reconstruction utility cannot support more than 8 parameters or an empty parmater set')
    end
    if istable(rec)
        N = height(rec);
        out = rec;
        for i = 1:N
            [in_dir,name,ext] = fileparts(rec.file(i));
            if in_dir ~= fullfile(dir,sub_dir)
                out.file(i) = fullfile(sub_dir,strcat(name,ext));
                copyfile(in.file(i),fullfile(dir,sub_dir));
            else
            	out.file(i) = fullfile(sub_dir,strcat(name,ext));
            end
        end
    else
        path = fullfile(sub_dir,'record.rec');
        fullpath = fullfile(dir, path);
        write_rec(rec,fullpath,data.pixelsize,false);
        out = table(data.times(1),data.times(end),convertCharsToStrings(path),'VariableNames',{'start','end','file'});
    end
end

