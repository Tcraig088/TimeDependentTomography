classdef MetaData
    %METADATA Summary of this class goes here
    %   Detailed explanation goes here
    
    properties
        dir
        name
        series
        vol_bool = false
        vol
        recs
    end
    
    methods
        function obj = MetaData(dir,series,volclass)
            %METADATA Construct an instance of this class
            %   Detailed explanation goes here
            if nargin > 2
                dir = fullfile(volclass.dir,volclass.name,dir);
                obj.vol_bool = true;
                obj.vol = volclass;
            end
            [obj.dir,obj.name] = fileparts(dir);
            path = fullfile(dir,'data.mat');
            if isfile(path)
                CheckDirectory(dir);
            else
                if exist(dir, 'dir')
                    rmdir(dir,'s');
                end
            end
            mkdir(dir);
            
            obj.series = series;
            save(path,'obj');
        end
        
        function obj = NewRec(obj,name,func,params)
            if nargin < 4
                params = [];
            end
            path = fullfile(obj.dir,obj.name,name);
            N = size(obj.recs,1);
            for i = 1:N
                if strcmp(obj.recs(i,:).name,name)
                    CheckDirectory(path);
                    obj.recs(i,:) = [];
                    N = N-1;
                    break;
                end
            end
            var = Reconstruction(name, func,obj,params);
            if N == 0
                obj.recs = table(var,convertCharsToStrings(name),'VariableNames',{'rec','name'});
            else
                var2 = table(var,convertCharsToStrings(name),'VariableNames',{'rec','name'});
                obj.recs = [obj.recs;var2];
            end
            path = fullfile(obj.dir,obj.name,'data.mat');
            save(path,'obj');  
        end 
        
        function met = Filter(obj,name,mask)
            name =  strcat(obj.name,'_',name);
            set = obj.series;
            set.data = obj.series.data(:,:,mask);
            set.angles = obj.series.angles(mask,:);
            set.times = obj.series.times(mask,:);
            volume = obj.vol;
            mask = [true; mask];
            volume.vol_table = obj.vol.vol_table(mask,:);
            
            met = MetaData(name,set,volume);
        end
        
    end
end

