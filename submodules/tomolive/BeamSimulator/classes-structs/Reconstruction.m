classdef Reconstruction
    %RECONSTRUCTION Summary of this class goes here
    %   Detailed explanation goes here
    
    properties
        rec_table
        eval
    end
    
    methods
        function obj = Reconstruction(name,func,met,params)
            %RECONSTRUCTION Construct an instance of this class
            %   Detailed explanation goes here
            
            dir = fullfile(met.name,name);
            if exist(fullfile(met.dir,dir), 'dir')
                rmdir(fullfile(met.dir,dir), 's' );
            end
            mkdir(met.dir,dir);
            
            obj.rec_table = Reconstruct(met.dir,dir, func,met.series,params);           
            obj.eval = RecEval(met, obj);
        end
    end
end

