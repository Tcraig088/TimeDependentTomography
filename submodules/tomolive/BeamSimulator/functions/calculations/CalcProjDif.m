function [out] = CalcProjDif(met,rec_table)
%CALCPROJDIF Summary of this function goes here
%   Detailed explanation goes here
    
    N = size(met.series.angles,1);
    out = zeros([N 1]);
    for i = 1:N
        count = 0;
        subset = rec_table(rec_table.start <= met.series.times(i),:);
        subset = subset(subset.end >= met.series.times(i),:);
        M = height(subset);
        srec = 0;
        for j = 1:M
            count = count+1;
            path = fullfile(met.dir,subset.file(j));
            rec = read_rec(path,false);
            srec = srec + rec;
        end
        rec = srec./count;
        fordproj = fp(rec,met.series.angles(i));
        dmap = abs(met.series.data(:,:,i) - fordproj);
        out(i) = sum(sum(dmap));
        norm = (met.series.data(:,:,i))./2;
        out(i) = out(i)/sum(sum(norm));
    end
end

