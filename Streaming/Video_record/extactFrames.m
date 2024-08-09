% Define input and output file names
inputFilename = 'Camera0_20240626_1348.avi';
outputFilename = 'output_video.mp4';

% Open the video reader
vid = VideoReader(inputFilename);

% Create video writer for output
outputVid = VideoWriter(outputFilename, 'MPEG-4');
outputVid.FrameRate = vid.FrameRate;
open(outputVid);

% Set frame range to extract
startFrame = 2608;
endFrame = 2847;

% Extract frames and write to output video
for frameIdx = startFrame:endFrame
    frame = read(vid, frameIdx);
    writeVideo(outputVid, frame);
end

% Close the output video file
close(outputVid);

% Optional: Preview the output video
implay(outputFilename);
