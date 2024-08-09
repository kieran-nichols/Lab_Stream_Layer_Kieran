# Lab Streaming Layer Repository

This repository contains scripts and tools for streaming and post-processing data using the Lab Streaming Layer (LSL). The repository is divided into two main folders: `Streaming` and `Post-processing`.

### Authors:
- Kieran Nichols (knichols4@wisc.edu)

## Repository Structure

- `Streaming`: Contains scripts for capturing and streaming various types of data (e.g., video, physiological signals) via LSL.
- `Post-processing`: Contains scripts and tools for processing the streamed data after collection.

## Folder Summaries

### [Streaming](https://github.com/neuroergolab/Lab_Streaming_Layer/tree/main/Streaming)

The `Streaming` folder includes scripts for setting up data streams using LSL. These scripts capture data from different sources such as webcams, physiological sensors, and other devices, and stream this data in real-time via LSL.

#### Key Scripts:

- **LSL_video_capture_v2.py**: Captures video from a webcam and streams it via LSL. This script sets up the video capture properties, initializes an LSL stream outlet, and streams video frames in real-time.
- **other_stream_scripts**: Add the other scripts for streaming other types of data or from other devices.

### [Post-processing](https://github.com/neuroergolab/Lab_Streaming_Layer/tree/main/Post-processing)

The `Post-processing` folder includes scripts for processing the data that has been streamed and recorded. These scripts handle data cleaning, analysis, and visualization to help interpret the streamed data.

#### Key Scripts:

- - **other_stream_scripts**: Add the other scripts for the post-processing.

## Usage

1. **Streaming Data**:
   - Navigate to the `Streaming` folder.
   - Select and configure the appropriate streaming script for your data source.
   - Run the script to start streaming data via LSL.

2. **Post-processing Data**:
   - Navigate to the `Post-processing` folder.
   - Select the appropriate script for your data processing needs.
   - Run the script to process, analyze, and visualize the streamed data.

## Contributing

Contributions to this repository are welcome. If you have scripts or tools that enhance the streaming or post-processing capabilities, please consider contributing by creating a pull request.

## License

This repository is provided under the MIT License. Feel free to use, modify, and distribute the scripts and tools as needed.

## Contact

For questions or support, please contact the repository maintainers or create an issue in the repository.

