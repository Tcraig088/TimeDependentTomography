function [out,init] = CalcVolDif(met,rec_table)
%CALCPROJDIF Summary of this function goes here
%   Detailed explanation goes here
    N = height(met.vol.vol_table);
    out = zeros([N-1 1]);
    for i = 1:N
        count = 0;
        path = fullfile(met.vol.dir,met.vol.vol_table.file(i));
        vol = read_rec(path,false);
        
        if i == 1
            path = fullfile(met.dir,rec_table.file(1));
            srec = read_rec(path,false);
            count = 1;
        else
            subset = rec_table(rec_table.start <= met.vol.vol_table.time(i),:);
            subset = subset(subset.end >= met.vol.vol_table.time(i),:);
            M = height(subset);
            
            for j = 1:M
                count = count+1;
                path = fullfile(met.dir,subset.file(j));
                rec = read_rec(path,false);
                if j == 1
                    srec = rec.*0;
                end
                srec = srec + rec;
            end
        end
        rec = srec./count;
        dmap = abs(vol - rec);
        val = sum(sum(sum(dmap)));
        norm = vol;
        if i == 1
            init = val/sum(sum(sum(norm)));
        else
            out(i-1,:) = val/sum(sum(sum(norm)));
        end
    end
end



