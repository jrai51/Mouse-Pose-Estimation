#!/bin/bash

path_to_video="trial_vids/mouse_trial3.mp4"

path_to_output="pose_predictions.slp"

source /home/jrai/mambaforge/bin/activate sleap

sleap-track -m "single_instance_n284" -o $path_to_output $path_to_video

sleap-convert $path_to_output --format 'analysis.csv'
