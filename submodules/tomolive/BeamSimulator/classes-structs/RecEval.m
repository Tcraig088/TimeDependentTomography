classdef RecEval
    %EVALUATION Summary of this class goes here
    %   Detailed explanation goes here
    
    properties
        projdif 
        voldif
        raw
    end
    
    methods
        function obj = RecEval(met,rec)
            %EVALUATION Construct an instance of this class
            %   Detailed explanation goes here
            x = met.series.times;
            y1 = CalcProjDif(met,rec.rec_table);
            if met.vol_bool
                [y2,y2init] = CalcVolDif(met,rec.rec_table);
            else
                y2 = y1;
                y2init = NaN;
                y2(:) = NaN;
            end
            obj.raw = table(x,y1,y2,'VariableNames',{'time','projdif','voldif'});
            obj.projdif = struct(...
                'init', y1(1),...
                'avg', sum(y1)/size(y1,1));
            obj.voldif = struct(...
                'init', y2init,...
                'avg', sum(y2)/size(y2,1));
        end
        
    end
end

