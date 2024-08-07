# Instructions for usage. 

This repository contains a trained SLEAP model for mice pose estimation. The repository includes a Dockerfile to create an image to allow you to easily run inferencing in a container.    

Directory `single_instance_n284` contains the trained model files. `predictions` is the directory containing the .slp SLEAP dataset files, and also converted datasets. The directory `trial_vids` contains the mice videos from behavioural trials.  

## Test Setup
### If SLEAP is installed on host computer: 
Commands in order:

1. `mamba activate sleap`

2. `cd file pathname`

3. `sleap-track -m "single_instance_n284" -o 'predictions/outfile_name.slp' 'trial_vids/mouse_trial2.mp4' `

4. `sleap-convert 'predictions/outfile_name.slp' --format 'h5' -o 'analysis_outfile_name.h5' `

### If Docker is installed:

Build the docker image:
`docker build -t mouse_sleap .`

Run the Docker interactive container: 
`docker run -it --rm --gpus all -e NVIDIA_DRIVER_CAPABILITIES=all mouse_sleap`

1. $ `mamba activate sleap`
2. $ `sleap-track -m "single_instance_n284" -o "predictions/outfile_name.slp" "trial_vids/infile_name.mp4"`
3. $ `sleap-convert "predictions/outfile_name.slp" --format 'h5' -o "predictions/analysis_outfile_name.h5"`

At this point, you should have created an analysis file in the docker container. To copy this analysis file, open a new terminal window, and use the `docker ps` and `docker cp` commands as outline below to copy the analysis file in your container to your host computer files.

First, identify the ID or name of the container you want to save changes from by using the docker ps -a command: `docker ps -a`

Then use copy the file using: 
`docker cp container_id_or_name:/home/user/predictions/analysis_outfile_name.h5 /path/to/repository/predictions/`

>To render a video showing the pose estimation:
In the docker container, run command:
`sleap-render predictions/analysis_outfile_name.h5 --marker_size 2 --crop 100,100`

This will create a video file within the docker container. You can use the `docker cp` command to copy the video to your host computer files.
## How to Use

### 1. Video to H5 File (`Convert_MP4_to_H5.py`)

> [!WARNING]
> **1. Make sure to adjust the paths in the script according to your directory structure and file locations.**
> 
> **2. Before running you must type this into your terminal to ensure it works `mamba activate sleap`, then run the code**

To convert a video to an H5 file using the provided script, follow these steps:

1. Ensure you have the video files placed in a directory e.g. `/Volumes/okamoto_lab/shared/4 Jay/behaviour/in vivo imaging`
2. Update the script `Convert_MP4_to_H5.py` with your desired file paths for the model, video files, and output directories.
3. Run the script using Python.

> [!IMPORTANT]
> This script will automatically process all `.mp4` files in the specified directory, generating SLEAP dataset files and converting them to H5 format.

### 2. H5 Files to CSV (`Convert_H5_to_CSV.py`)

This section explains how to convert H5 files generated from SLEAP pose estimation into CSV format for further analysis or visualization.

#### Prerequisites

Ensure you have the following Python packages installed:

- `h5py`
- `pandas`
- `numpy`

You can install these packages using pip:
`pip install h5py pandas numpy`

#### Prepare the Directories:
- Place your H5 files in the specified input directory (e.g. /path/to/H5 Files).
- Ensure the output directory for CSV files exists or will be created by the script (e.g. /path/to/CSV Files).

(Modify the input_dir and output_dir variables in the script to match the paths where your H5 files are located and where you want to save the CSV files.)

> [!IMPORTANT]
> The provided script `Convert_H5_to_CSV.py` will convert all H5 files in the specified input directory to `.CSV` format and save them in the specified output directory.
> Additionally, it preprocesses the data by filling missing values and interpolating to ensure smooth data.

### 3. CSV to MP4 with Dots (`Convert_CSV_to_MP4.py`)

This section explains how to overlay points from CSV files onto the corresponding video files and save the results as MP4 videos.

#### Prerequisites

Ensure you have the following Python packages installed:

- `opencv-python`
- `pandas`
- `numpy`
- `pync` (for macOS notifications, this optional you can get rid of it if you don't require it) 

You can install these packages using pip:

`pip install opencv-python pandas numpy pync`

> [!TIP]
> This code will open a GUI called `Point Viewer` that will help you ensure that the Green Points (PoGS) match the video frames. 

#### How to Use Point Viewer

1. Place your CSV files containing the points data in the csv_folder.

2. Ensure the corresponding video files are in the video_folder.

3. Run the script. It will display a window where you can use trackbars to navigate through the video and point data. Use the keys as described below to control playback and saving:

##### Controls
- 'ESC': Exit the current mode & go to next video
- 'l': Increase the current frame index by 10.
- 'j': Decrease the current frame index by 10.
- 'i': Increase the current frame index by 1.
- 'k': Decrease the current frame index by 1.
- 'a': Decrease the start frame by 10.
- 'd': Increase the start frame by 10.
- 's': Decrease the start frame by 1.
- 'w': Increase the start frame by 1.
- 'n': Start video playback with points overlay.
- 'b': Go back to trackbars mode from playback mode.
- 'u': Save the video with points overlay (this can be done in trackbar mode so note down what `frame` and `PoGS` you were at)

**The output videos with points overlay will be saved in the output_folder.**

> [!IMPORTANT]
> The provided script Convert_CSV_to_MP4.py overlays points from the CSV files onto the corresponding video frames and saves the annotated videos.

> [!WARNING]
> Ensure your paths are correctly set to avoid any file not found errors.

> [!CAUTION]
> Always back up your original files before running scripts that modify them.



