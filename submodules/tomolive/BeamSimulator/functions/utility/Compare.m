function [summary,raw] = Compare(varargin)
	rec_list={};
    data_list = MetaData.empty;
    rec_filter = false;
    for i = 1:nargin
        if isvector(varargin{i})
            for j = 1:size(varargin{i},2)
                [data_list,rec_list] = CheckType(varargin{i}(j),data_list,rec_list);
            end
        else
            [data_list,rec_list] = CheckType(varargin{i},data_list,rec_list);
        end
    end
    rec_count = size(rec_list,2);
	data_count = size(data_list,2);
    first = true;
    if rec_count ~= 0 
        rec_filter = true;
    end
    
    for i = 1:data_count
        M = height(data_list(i).recs);
        for j = 1:M
            if rec_filter ==true
                for k =1:rec_count
                    if contains(data_list(i).recs.name(j),rec_list{k})
                        if first == true
                            first=false;
                            [summary,raw] = MakeTable(data_list(i),j);
                        else
                            [summary,raw] = MakeTable(data_list(i),j, summary, raw);
                        end
                    end
                end
            else                       
                if first == true
                    first=false;
                    [summary,raw] = MakeTable(data_list(i),j);
                else
                    [summary,raw] = MakeTable(data_list(i),j, summary, raw);
                end
            end
        end
    end
end

function [sum,raw] = MakeTable(met,index,sum,raw)
    name = met.name;
    if met.vol_bool
        name = [met.vol.name,'_',name];
    end
    recdata = met.recs(index,:);
    rec = recdata.rec(1);
    name = strcat(name,'_',recdata.name(1));
	rawtemp = rec.eval.raw;
	time = strcat(name,' time');
	projdif = strcat(name,' projdif');
	voldif = strcat(name,' voldif');
	rawtemp.Properties.VariableNames={ convertStringsToChars(time)  convertStringsToChars(projdif)  convertStringsToChars(voldif)};
                    
    s2 = rec.eval.projdif.init;
	s3 = rec.eval.projdif.avg;
	s4 = rec.eval.voldif.init;
	s5 = rec.eval.voldif.avg;
    summarytemp = table(name,s2,s3,s4,s5,'VariableNames',{'name','proj init','proj ave','vol init','vol ave'});

    if nargin > 2
        a = height(rawtemp);
        b = height(raw);
        if a>b
            NaNtable = array2table(NaN([height(rawtemp(b+1:a,:)) width(raw)]),'VariableNames',raw.Properties.VariableNames);
            raw = [raw; NaNtable];  
        elseif b>a
            NaNtable = array2table(NaN([height(raw(a+1:b,:)) width(rawtemp)]),'VariableNames',rawtemp.Properties.VariableNames);
            rawtemp = [rawtemp; NaNtable];            
        end
        raw = [raw rawtemp];
        sum = [sum;summarytemp];
    else
        sum = summarytemp; 
        raw = rawtemp;        
    end    
end

function [data,rec] = CheckType(in,data,rec)
        if isstring(in) || ischar(in)
                rec{end+1} = convertCharsToStrings(in);
        else
            data(end+1) = in;
        end
end