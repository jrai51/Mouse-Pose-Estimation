# Instructions for usage. 

This repository contains a trained SLEAP model for mice pose estimation. The repository includes a Dockerfile to create an image to allow you to easily run inferencing in a container.    

Directory `single_instance_n284` contains the trained model files. `predictions` is the directory containing the .slp SLEAP dataset files, and also converted datasets. The directory `trial_vids` contains the mice videos from behavioural trials.  


## If SLEAP is installed on host computer: 
Commands in order:

1. `mamba activate sleap`

2. `sleap-track -m "single_instance_n284" -o 'predictions/outfile_name.slp' 'trial_vids/infile_name.mp4' `

3. `sleap-convert 'predictions/outfile_name.slp' --format 'h5' -o 'analysis_outfile_name.h5' `

## If Docker is installed:

Build the docker image:
`docker build -t mouse_sleap .`

Run the Docker interactive container: 
`docker run -it --rm --gpus all -e NVIDIA_DRIVER_CAPABILITIES=all mouse_sleap`

1. $ `mamba activate sleap`
2. $ `sleap-track -m "single_instance_n284" -o "predictions/outfile_name.slp" "trial_vids/infile_name.mp4"`
3. $ `sleap-convert "predictions/outfile_name.slp" --format 'h5' -o "predictions/analysis_outfile_name.h5"`

At this point, you should have created an analysis file in the docker container. To copy this analysis file, open a new terminal window, and use the `docker ps` and `docker cp` commands as outline below to copy the analysis file in your container to your host computer files.

First, identify the ID or name of the container you want to save changes from by using the docker ps -a command:

`docker ps -a`

Then use copy the file using: 

`docker cp container_id_or_name:/home/user/predictions/analysis_outfile_name.h5 /path/to/repository/predictions/`

>To render a video showing the pose estimation:
In the docker container, run command:
>
`sleap-render predictions/analysis_outfile_name.h5 --marker_size 2 --crop 100,100`

This will create a video file within the docker container. You can use the `docker cp` command to copy the video to your host computer files.



