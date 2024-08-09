# README

## noraxon_stream Example

### Authors:
- Kieran Nichols

### Description:
This MATLAB script demonstrates how to stream EMG data from a Noraxon device using the Lab Streaming Layer (LSL). The script initializes a connection to the Noraxon stream, collects data, and streams it via LSL. This example requires MATLAB R2014b or higher.

## Prerequisites:
- MATLAB R2014b or higher
- LSL library for MATLAB
- Noraxon streaming setup

## Setup Instructions for use of liblsl-Matlab/EMG_streaming_LUNA.m:

1. **Enter the folder liblsl-Matlab**

2. **Add LSL Library Paths**:
   Ensure the LSL library paths are correctly added. Update the paths if necessary:
    ```matlab
    addpath 'C:\Users\jayasuriyaar\OneDrive - UW-Madison\Training\LSL\EMG and Other Matlab\liblsl-Matlab';
    addpath 'C:\Users\jayasuriyaar\OneDrive - UW-Madison\Training\LSL\EMG and Other Matlab\liblsl-Matlab\bin';
    addpath 'C:\Users\jayasuriyaar\OneDrive - UW-Madison\Training\LSL\EMG_http';
    ```

3. **Initialize Noraxon Stream**:
   Set the IP address and port for the Noraxon stream:
    ```matlab
    stream_config = noraxon_stream_init('127.0.0.1', 9220);
    ```

4. **Collect Initial Data**:
   Collect an initial set of data to determine the number of channels:
    ```matlab
    data = noraxon_stream_collect(stream_config, 1); 
    ```

## Usage Instructions:

1. **Load LSL Library**:
    ```matlab
    disp('Loading library...');
    lib = lsl_loadlib();
    ```

2. **Create a New Stream Outlet**:
   Define the stream information and create an outlet:
    ```matlab
    len_channels = length(data);
    info = lsl_streaminfo(lib,'EMG','EMG',len_channels,2000,'cf_float32','sdfwerr32432');
    outlet = lsl_outlet(info);
    ```

3. **Stream Data**:
   Continuously collect and stream data:
    ```matlab
    while true
        time = 1;
        data = noraxon_stream_collect(stream_config, time);
        len = length(data(1).samples); 
        tstart = toc;
        num_samples = length(data(1).samples); 
        chunk = zeros(num_samples, len_channels); 
        
        for i = 1:len_channels
            chunk(:, i) = data(i).samples'; 
        end
        
        outlet.push_chunk(chunk');
        tend = toc;
        elapsed_time = tend - tstart;
        pause(time - elapsed_time);
        display(toc - tstart);
    end
    ```

## Notes:

- Ensure that the IP address and port number match the configuration of your Noraxon device.
- Adjust the sampling rate and other parameters as needed for your specific application.
- The script uses a `while true` loop to continuously stream data. To stop the script, you will need to manually interrupt it (e.g., using Ctrl+C in MATLAB).

## Example Output:

- "Loading library..."
- "Creating a new streaminfo..."
- "Opening an outlet..."
- "Now transmitting data..."

## License:
This script is provided as-is by Noraxon USA, Inc. Feel free to modify and use it for your applications.

