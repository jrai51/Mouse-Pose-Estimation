import os
import subprocess

# Full path to the model file
model_path = "/path/to/Mouse-Pose-Estimation-main/single_instance_n284"

# Define the directory containing the video files
video_directory = "/path/to/MP4 Files"

# Define output directories
predictions_dir = "/path/to/Mouse-Pose-Estimation-main/predictions"
h5_files_dir = "/path/to/Mouse-Pose-Estimation-main/H5 Files"

# Ensure output directories exist
os.makedirs(predictions_dir, exist_ok=True)
os.makedirs(h5_files_dir, exist_ok=True)

# Get a list of all .mp4 files in the video directory
video_files = [os.path.join(video_directory, f) for f in os.listdir(video_directory) if f.endswith('.mp4')]

# Iterate over each video file
for video_file in video_files:
    # Extract the file name without extension
    file_name = os.path.basename(video_file).split('.')[0]
    
    # Define output file paths
    slp_file = os.path.join(predictions_dir, f"{file_name}.slp")
    h5_file = os.path.join(h5_files_dir, f"{file_name}_analysis.h5")
    
    # Generate the sleap-track command
    sleap_track_cmd = f'sleap-track -m "{model_path}" -o "{slp_file}" "{video_file}"'
    
    # Run the sleap-track command
    subprocess.run(sleap_track_cmd, shell=True)
    
    # Generate the sleap-convert command
    sleap_convert_cmd = f'sleap-convert "{slp_file}" --format "h5" -o "{h5_file}"'
    
    # Run the sleap-convert command
    subprocess.run(sleap_convert_cmd, shell=True)
