function extractAllAndGetDataQuality(settings)
% This file will run the Tobii Glasses 2 data extractor and data quality
% computations on all recordings in all projects in a projects folders, all
% recordings in a selected project, or a given selected recording. This so
% that this does not have to be done manually for each recording when
% aggregating, e.g., data quality information for a whole project.
%
% Part of GlassesViewer.
% Cite as: Niehorster, D.C., Hessels, R.S., and Benjamins, J.S. (2020).
% GlassesViewer: Open-source software for viewing and analyzing data from
% the Tobii Pro Glasses 2 eye tracker. Behavior Research Methods. doi:
% 10.3758/s13428-019-01314-1

qDEBUG = false;
if qDEBUG
    dbstop if error
end

myDir     = fileparts(mfilename('fullpath'));
if nargin<1 || isempty(settings)
    if ~isempty(which('matlab.internal.webservices.fromJSON'))
        jsondecoder = @matlab.internal.webservices.fromJSON;
    elseif ~isempty(which('jsondecode'))
        jsondecoder = @jsondecode;
    else
        error('Your MATLAB version does not provide a way to decode json (which means its really old), upgrade to something newer');
    end
    settings  = jsondecoder(fileread(fullfile(myDir,'defaults.json')));
end

addpath(genpath('function_library'),genpath('user_functions'),genpath('SDparser'))

% For the Glasses 2, select either the folder of a specific recording
% to open, or the projects directory copied from the SD card itself.
% So, if "projects" is the project folder on the SD card, there are
% three places that you can point the software to:
% 1. the projects folder itself
% 2. the folder of a specific project. An example of a specific project
%    is: projects\raoscyb.
% 3. the folder of a specific recording. An example of a specific
%    recording is: projects\raoscyb\recordings\gzz7stc. Note that the
%    higher level folders are not needed when opening a recording, so
%    you can just copy the "gzz7stc" folder of this example somewhere
%    and open it in isolation.
%
% For the Glasses 3, select either a folder containing Glasses 3
% recording folders, or the folder of a specific recording. So if "xxx"
% is the folder on the SD card, there are two places that you can point
% the software to:
% 1. the xxx folder itself
% 2. the folder of a specific recording. An example of a specific
%    recording is: xxx\20220310T130724Z. Note that only this folder in
%    isolation is needed when opening a recording, so you can just copy
%    the "20220310T130724Z" folder of this example somewhere and open
%    it in isolation.
if 1
    selectedDir = uigetdir('','Select projects, project or recording folder');
else
    % for easy use, hardcode a folder.
    if 1
        % example of where projects directory is selected, shows recording
        % selector
        selectedDir = fullfile(myDir,'demo_data','projects');
    elseif 0
        % example of where directory of a specific project is selected,
        % shows recording selector
        selectedDir = fullfile(myDir,'demo_data','projects','raoscyb');
    else
        % example of where a recording is directly selected
        selectedDir = fullfile(myDir,'demo_data','projects','raoscyb','recordings','gzz7stc');
    end
end
if ~selectedDir
    return
end

% find out if this is a projects folder or the folder of an individual
% recording, take appropriate action
qIsSingleRecording = ...
    exist(fullfile(selectedDir,'segments'),'dir') && exist(fullfile(selectedDir,'recording.json'),'file') || ... % G2
    exist(fullfile(selectedDir,'recording.g3'),'file');
qIsSpecificProject = false;
if ~qIsSingleRecording
    % assume this is a project dir. G2ProjectParser will fail if it is not
    [isG2,qIsSpecificProject] = G2ProjectParser(selectedDir,true);
    if ~isG2
        isG3 = G3ProjectParser(selectedDir,true);
        if ~isG3
            error('Could not find Glasses 2 or Glasses 3 recordings or projects in the folder: %s',selectedDir);
        end
    end
end

% check what to process
if qIsSingleRecording
    folders = {''};
    % get some info about recording
    project = {''};
    recjson = jsondecoder(fileread(fullfile(selectedDir, 'recording.json')));
    if isfield(recjson.rec_info,'Name')
        recording = {recjson.rec_info.Name};
    else
        recording = {recjson.rec_info.name};
    end
    participant = {''};
    if isfield(recjson,'rec_participant')
        partjsonfile = fullfile(selectedDir, 'participant.json');
        if exist(partjsonfile,'file')==2
            partjson = jsondecoder(fileread(partjsonfile));
            if isfield(partjson.pa_info,'Name')
                participant = {partjson.pa_info.Name};
            else
                participant = {partjson.pa_info.name};
            end
        end
    end
else
    if isG2
        fid = fopen(fullfile(selectedDir,'lookup_G2.tsv'),'rt');
        fgetl(fid);
        C = textscan(fid,repmat('%s',1,18),'delimiter','\t');
        fclose(fid);
        
        project     = C{5};
        participant = C{7};
        recording   = C{9};
        
        if qIsSpecificProject
            folders = cellfun(@(x)  fullfile(  'recordings',x),     C{3},'uni',false);
        else
            folders = cellfun(@(x,y)fullfile(x,'recordings',y),C{1},C{3},'uni',false);
        end
    else
        fid = fopen(fullfile(selectedDir,'lookup_G3.tsv'));
        fgetl(fid);
        C = textscan(fid,repmat('%s',1,8),'delimiter','\t');
        fclose(fid);
        
        recording   = C{3};
        participant = C{2};
        project     = repmat({''},length(recording),1);
        
        folders     = C{1};
    end
end

% load glasses data, get data quality
codeStream      = 'analysis interval';
codeCat         = 'included';
for p=length(folders):-1:1
    myDir           = fullfile(selectedDir,folders{p});
    
    % load data
    if isG2
        data            = readG2DataFiles(myDir,settings.userStreams,qDEBUG);
    else
        data            = readG3DataFiles(myDir,settings.userStreams,qDEBUG);
    end
    
    % get data quality, use coding if available
    qHaveAnalysisInterval = false;
    codingFile            = fullfile(myDir,'coding.mat');
    if exist(codingFile,'file')==2
        coding                  = load(codingFile);
        qWhichStream            = strcmp(coding.stream.lbls,codeStream);
        nStreams                = sum(qWhichStream)==1;
        assert(nStreams<2,'More than one analysis interval coding stream found, impossible');
        if nStreams==1
            qWhichCodeCat           = strcmp(coding.codeCats{qWhichStream}(:,1),codeCat);
            nCodeCats               = sum(qWhichCodeCat);
            assert(nCodeCats<2,'More than one coding category with the same name found in coding stream, impossible');
            qHaveAnalysisInterval   = nCodeCats==1;
        end
    end
    
    if qHaveAnalysisInterval
        code                = coding.codeCats{qWhichStream}{qWhichCodeCat,2};
        iCode               = find(~~bitand(coding.type{qWhichStream},code));
        analysisIntervals   = [coding.mark{qWhichStream}(iCode); coding.mark{qWhichStream}(iCode+1)].';
        data.quality        = computeDataQuality(myDir, data, settings.dataQuality.windowLength, analysisIntervals);
    else
        warning('analysis interval unknown');
        data.quality        = computeDataQuality(myDir, data, settings.dataQuality.windowLength);
    end
    
    % store for output (NB! this just outputs data quality for the first
    % analysis interval!)
    output(p).dq        = data.quality.interval(1);
    output(p).vq.scene  = data.video.scene.missProp;
    if isfield(data.video,'eye')
        output(p).vq.eye    = data.video.eye.missProp;
    else
        output(p).vq.eye    = nan;
    end
end

fid = fopen(fullfile(selectedDir,'dataQuality.xls'),'wt');
fprintf(fid,'project\tparticipant\trecording\tRMS left azi\tRMS left ele\tRMS right azi\tRMS right ele\tRMS binocular gaze point video X\tRMS binocular gaze point video X\tdata loss left\tdata loss right\tdata loss binocular gaze point video\tprop missing scene video\tprop missing eye video\n');
for p=1:length(output)
    fprintf(fid,'%s\t%s\t%s\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.3f\t%.3f\n',...
        project{p},participant{p},recording{p},...
        output(p).dq.RMSS2S.azi(1),output(p).dq.RMSS2S.ele(1),output(p).dq.RMSS2S.azi(2),output(p).dq.RMSS2S.ele(2),output(p).dq.RMSS2S.bgp,...
        output(p).dq.dataLoss.azi,output(p).dq.dataLoss.bgp(1),...
        output(p).vq.scene,output(p).vq.eye);
end
fclose(fid);
