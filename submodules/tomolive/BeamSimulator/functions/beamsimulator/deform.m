function [obj] = deform(obj, alpha)
%DEFORM Causes elastic deformation in the object
%   Detailed explanation goes here
d_f = -1+2*rand(size(obj,1), size(obj,2), size(obj,3), 3);
sig=10; 

d_f(:,:,:,1) = imgaussfilt3(d_f(:,:,:,1),sig);
d_f(:,:,:,2) = imgaussfilt3(d_f(:,:,:,2),sig);
d_f(:,:,:,3) = imgaussfilt3(d_f(:,:,:,3),sig);
amp = sqrt(d_f(:,:,:,1).^2 + d_f(:,:,:,2).^2 + d_f(:,:,:,3).^2);
d_f=alpha*d_f./amp;
obj = imwarp(obj, d_f);
end

