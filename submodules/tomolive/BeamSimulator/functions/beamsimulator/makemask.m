function [mask] = makemask(obj)
%MAKEMASK masks a 3D object with the number of connections to each voxel
	[x,y,z] = size(obj);
	mask = double(obj~=0);
	for i = 1:x
		for j = 1:y
			for k = 1:z
				if mask(i,j,k) ~= 0
                    mask(i,j,k) = 1;
                    [ii,ie,ji,je,ki,ke] = getindex(x,i,j,k);
					for a = ii:ie
						for b = ji:je
							for c = ki:ke
								mask(i,j,k) = mask(i,j,k) + double(mask(a,b,c)~=0);
							end
						end
                    end
                    mask(i,j,k) = mask(i,j,k) - 1;
                end
			end
		end
    end
end

function [ii,ie,ji,je,ki,ke] = getindex(dim, i,j,k)
    ii = i-1;
    ie = i+1;
    if (i - 1)<= 0
        ii = i;
    elseif i + 1 > dim
        ie = i;
    end
    ji = j-1;
    je = j+1;
    if (j - 1)<= 0
        ji = j;
    elseif j + 1 > dim
        je = j;
    end
    ki = k-1;
    ke = k+1;
    if (k - 1)<= 0
        ki = k;
    elseif k + 1 > dim
        ke = i;
    end
end







