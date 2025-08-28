% This script is a full tutorial on how to use the beam simulator and data
% manager tool kits
%% Load in the dependencies
% The Data Manager is dependent on tomohawk and Astra
% The Beam Simulator is additionally dependent on the Data Manager
addpath(genpath('tomohawk_2020'))
addpath(genpath('astra-1.9.0.dev11'))
addpath(genpath('BeamSimulator-1.0.1'))
addpath(genpath('DataManager-1.0.3'))
addpath(genpath('VolViewer4D'))

%% Using The Beam Simulator - Loading the Structure
%  Load in a preset structure e.g. NanoCage or Phantom Shepp-Logan
%data = load('nanocage_phantom.mat');
%obj = data.mask;
obj = phantom3d(512);
% or it can be a custom structure of your choosing

%% Define the Simulation Parameters
% mandatory parameters
dir = 'path_to_data';
times = (1:3).';
params = Params4d(dir,times);

% additional parameters can be adjusted these default to 1& 0.9
params.deform = 0;  % elastic deformation
params.knock = 0; % knock on damage

%% Run the Simulation
vol = Volume4d(obj,params);
angles = mod((1:71)*deg2rad(140)*((1+sqrt(5))/2),deg2rad(140));
angles = (rad2deg(angles)-70).';

angles = ((times-1)*70)-70;
%set noise and make tilt series 
%nmean =6;
%ndev =1;
%series = vol.MakeSeries(angles,nmean,ndev);
% noise mean and deviation default to zero

%%
series = vol.MakeSeries(angles);
met = MetaData('inc',series,obj);

%% Setting Up a MetaDat  a Class - Simulated or Real Data
% Simulated
met = MetaData('GRS',series,vol);
% Real
%met = MetaData('D:\Data\SampleName',series);
% Run reconstruction with or without additional params
%met = met.NewRec('RecName', @rec_sirt);

%% Evaluate data using the compare tool
[summary,raw] = Compare(met1,met2,met3,"SIRT","EM");
% Creates tables comparing all the data in met 1-3
% filters searching for the EM & SIRT reconstructions 
% by default it compares all available reconstructions
% data can be individually inputted or as an array
[summary,raw] = Compare([met1,met2,met3],"SIRT","EM");
% must be string "SIRT" is valid 'SIRT' is not
%% Make New MetaData classes from an existing data

mask = abs(rem(met.series.angles,4)) == 3;
met2 = met.Filter('inc4',mask);

%% To Load in an existing script

% Dont use the standard matlab load function because if you move the directory it will get confused
% There will be a file called data.mat in your directory which you can load all the metadata from.
met = LoadMetaData('path_to_data.mat_file');