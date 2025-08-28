classdef Params4d
    %PARAMS4D Summary of this class goes here
    %   Detailed explanation goes here
    properties
        times
        dir
        deform = 1;
        knock = 0.9;
        steps;
    end
    
    methods
        function obj = Params4d(dir,times)
            %PARAMS4D Construct an instance of this class
            %   Detailed explanation goes here
            obj.dir = dir;
            obj.times = times;
            if isrow(obj.times)
                obj.times = obj.times.';
            end 
        end
        
        function obj = CalcSteps(obj)
            %METHOD1 Summary of this method goes here
            %   Detailed explanation goes here
            N = size(obj.times,1);
            obj.steps = zeros(N,1);
            obj.steps(1,:) = obj.times(1,:);
            for i = 2:N
                obj.steps(i,:) = obj.times(i,:) - obj.times(i-1,:);
            end
            obj.steps = obj.steps./min(obj.steps);
            obj.steps = round(obj.steps);
            obj.steps = obj.steps.';
        end
        
        function out = CalcIter(obj, iter)
            %METHOD1 Summary of this method goes here
            %   Detailed explanation goes here
            out = 0;
            for i = 1:iter
                out = out + obj.steps(i);
            end
        end
    end
end

