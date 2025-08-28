function [obj_out] = knockon(obj_in, mask, prob)
%KNOCKON Creates a knockon effect in the mask.
%   The outer layer of the mask is knock
    [x,y,z] = size(mask);
    mask = prob.^(mask./3);
    buried = prob^(27/3);
    for i = 1:x
        for j = 1:y
			for k = 1:z
				if mask(i,j,k) ~= buried || 0
                    if rand < mask(i,j,k)
                        mask(i,j,k) = 0;
                    end
                end
            end
        end
    end
    
    mask = mask==0;
    %obj_out = mask;
    obj_out = obj_in;
    obj_out(mask) = 0;

end