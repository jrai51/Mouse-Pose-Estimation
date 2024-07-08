#!/bin/bash

path_to_video="trial_vids/mouse_trial2.mp4"

path_to_output="predictions/trial2_pose_predictions.slp"

path_to_analysis="predictions/trial2_pose_analysis.csv"

source /home/jrai/mambaforge/bin/activate sleap #should be changed to your path

sleap-track -m "single_instance_n284" -o $path_to_output $path_to_video

sleap-convert $path_to_output --format $path_to_analysis
