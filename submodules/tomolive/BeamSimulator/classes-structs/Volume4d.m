classdef Volume4d
    %VOLUME4D Summary of this class goes here
    %   Detailed explanation goes here
    
    properties
        dir
        name
        vol_table
    end
    
    methods
        function obj = Volume4d(structure,params)
			% Normalize Model
			structure(structure<0) = 0.001;
			minval = min(min(min(structure)));
			maxval = max(max(max(structure)));
			structure = (structure - minval) ./ ( maxval - minval );
			
			% Setups up directories for saving files.
			[obj.dir,obj.name] = fileparts(params.dir);
            if( exist(params.dir, 'dir') )
				rmdir( params.dir, 's' );
            end
			mkdir(params.dir); 
			mkdir(params.dir,'vol');
			
			% Save initial structure as the 0 time structure
			vol = single(structure);
			volname = getname(params);
			write_rec(vol, volname,1,false);
			vol_table = table(0,convertCharsToStrings(volname),'VariableNames',{'time','file'});
			
			%Establish variables before running
			params = params.CalcSteps();
			iter = sum(params.steps);
			
			if params.deform == 0 && params.knock == 0
				N = size(params.times,1);
				for i = 1:N
					vol_temp = table(params.times(i),convertCharsToStrings(volname),'VariableNames',{'time','file'});
					vol_table = [vol_table;vol_temp];
                end
                obj.vol_table = vol_table;
				path = fullfile(obj.dir,obj.name,'vol','data.mat');
				save(path,'obj');
				return;
			end
			
			% run simulation
			a = 1;
			for i = 1:iter 
				mask = makemask(structure);
				structure = deform(structure, params.deform);
				structure = knockon(structure, mask, params.knock);
				if i == params.CalcIter(a)
					vol = single(structure);
					volname = getname(params,a);
					write_rec(vol, volname,1,false);
					vol_temp = table(params.times(a),convertCharsToStrings(volname),'VariableNames',{'time','file'});
					vol_table = [vol_table;vol_temp];
					a = a+1;
				end
				disp(['Completed iteration ',num2str(i+1), ' of ', num2str(iter+1) ]);  
            end
            obj.vol_table = vol_table;
			path = fullfile(obj.dir,obj.name,'vol','data.mat');
			save(path,'obj');
        end
		function series =  MakeSeries(obj,angles,nmean,nstd)
			if nargin <4
				nmean = 0;
				nstd = 0;
			end
			if isrow(angles)
				angles = angles.';
			end
		    N = size(angles,1);
			
			for i = 1:N
				path = fullfile(obj.dir,obj.name,'vol',obj.vol_table.file(i+1));
				volume = double(read_rec(path,false));
				if i ==1
					[x,y,~] = size(volume);
					data = zeros(x,y,N);
					times = zeros([N 1]);
				end
				data(:,:,i) = fp(volume,angles(i,:));
				data(:,:,i) = data(:,:,i) + sqrt(nmean)*randn(size(data(:,:,i))) + nstd;
				times(i,:) = obj.vol_table.time(i+1);
			end
			series = TiltSeries4d(data,angles,times);	
				
		end
    end
end

