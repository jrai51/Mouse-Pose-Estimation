# Instructions for usage. 

This repository contains a trained SLEAP model for mice pose estimation. The repository includes a bash script `annotate.sh` for simple usage on linux machines; simply edit variable values to the appropriate file paths and run `bash annotate.sh`.   

Directory `single_instance_n284` contains the trained model files. `predictions` is the directory containing the .slp SLEAP dataset files, and also converted datasets. The directory `trial_vids` contains the mice videos from behavioural trials.      

Commands in order:

1. `mamba activate sleap`

2. `sleap-track -m "single_instance_n284" -o 'predictions/outfile_name.slp' 'trial_vids/infile_name.mp4' `

3. `sleap-convert 'predictions/outfile_name.slp' --format 'outfile_name.csv' `

