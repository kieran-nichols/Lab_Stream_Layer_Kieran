# README

## LSL Video Capture v2

### Authors:
- Kieran Nichols (knichols4@wisc.edu)
- Based on code from [Vahid Samadi Bokharaie](https://github.com/vahid-sb/LSL_Video_Acquisition).

### Date: 8/5/24

### Description:
This script captures video from a webcam and streams it via the Lab Streaming Layer (LSL). It also saves the captured video to a file and displays it with an overlay showing elapsed time and frame rate.

## Prerequisites:
- Python 3.x
- OpenCV (`cv2`) library
- pylsl (Python library for LSL)
- numpy library

## Installation:
1. **Python Installation**: Ensure you have Python installed on your system. You can download it from [python.org](https://www.python.org/downloads/).
2. **Library Installation**: Install the required libraries using pip:
    ```bash
    pip install opencv-python pylsl numpy
    ```

## Usage:
1. **Script Configuration**:
   - Set the `dev` variable to the index number of your webcam/camera. Use the `check_available_ports.py` script to find out the index number.
   - Adjust the `new_fps` variable to set the desired frames per second.
   - Modify the `adj_width` and `adj_height` variables to set the desired resolution.

2. **Running the Script**:
   - Execute the script using the following command:
     ```bash
     python LSL_video_capture_v2.py
     ```

3. **Script Functionality**:
   - The script initializes the webcam, sets up the video capture properties, and creates an LSL stream outlet.
   - It captures video frames, resizes them, and displays them with an overlay showing the elapsed time, sampling frequency, and frame number.
   - The captured video is saved to a file, and each frame is streamed via LSL.

## Code Overview:

### createOutlet Function:
- **Parameters**:
  - `stream_name`: Name of the LSL stream.
  - `channel_names`: List of channel names for the stream.
  - `videoFile`: Path to the video file to save.

- **Returns**:
  - `StreamOutlet`: An LSL stream outlet object.

### Main Script:
- **Import Libraries**:
  - `cv2`: For video capture and processing.
  - `datetime`, `os`, `time`, `numpy`: For various utility functions.
  - `pylsl`: For LSL streaming.

- **Setup Video Capture**:
  - Initializes the webcam and sets the capture properties (FPS, resolution, codec).
  - Creates a video writer object to save the captured video.

- **Create LSL Stream Outlet**:
  - Calls `createOutlet` to set up the LSL stream outlet.

- **Capture and Stream Video**:
  - Enters an infinite loop to continuously capture video frames.
  - Resizes and displays the frames with an overlay showing elapsed time and frame rate.
  - Saves the frames to the video file and pushes them to the LSL stream outlet.
  - Adjusts the sleep time to maintain the desired frame rate.
  - Breaks the loop if the 'q' key is pressed.

### Example Output:
- "Cannot open camera" (if the webcam cannot be initialized)
- Display of video frames with overlay showing elapsed time, sampling frequency, and frame number.
- "Saved output video to: <filename>"

## Notes:
- Ensure the `dev` variable is set to the correct index number for your webcam/camera.
- The script uses a `while True` loop to continuously capture and stream video. To stop the script, press the 'q' key.
- The captured video is saved in the same directory as the script, with a filename containing the camera index and timestamp.

## License:
This script is provided as-is without any warranty. Feel free to modify and use it as needed for your applications.
