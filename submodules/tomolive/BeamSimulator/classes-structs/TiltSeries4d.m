classdef TiltSeries4d
    % Holds a tilt series with optional metadata.
    %
    % Attributes
    % ----------
    % data : 3D array
    %     Image data.
    % angles : 1D array
    %     Specimen holder tilt angles corresponding to the images.
    % pixelsize : double
    %     Pixelsize in nanometers.
    % times: 1D array
    %     Times in seconds.
    
    properties
        data
        angles
        times
        %if true times are real values if false they are arbitrary
        %not particularly seful in code but is usefule as a reference
        times_bool = false;
        pixelsize = 1;
    end

    methods
        function obj = TiltSeries4d(data, angles, times, pixelsize)
            % If there is only one input it is assumed that the input is a
            % standard 3D tilt series
            if nargin == 1
                obj.data = data.data; 
                obj.angles = data.angles; 
                obj.times = (1:size(obj.angles)).';
                obj.pixelsize = data.pixelsize;
            end
            if nargin > 1
                obj.data = data; 
                obj.angles = angles;
                obj.times = (1:size(angles)).'; 
                obj.times_bool = false;
            end
            if nargin > 2
                obj.times = times; 
                obj.times_bool = true;
            end
            if nargin > 3
                obj.pixelsize = pixelsize;
            end
        end
    end
end
