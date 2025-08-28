function CheckDirectory(dir)
%CHECKANDDELETE Summary of this function goes here
%   Detailed explanation goes here
    app = DirectoryUI(dir);  % create the parameter window
    while app.done == false  % polling
        pause(0.05);
    end
    val = app.proceed;  % get the values set in the parameter window
    app.CloseTheWindow; 
    if ~val
        error('User Terminated Program');
    end
end

