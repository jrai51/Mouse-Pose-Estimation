FROM continuumio/miniconda
WORKDIR /usr/src/app
COPY ./ ./

RUN mamba create -y -n sleap -c conda-forge -c nvidia -c sleap -c anaconda sleap=1.3.3
#RUN ["mamba", "create", "-y", "-n", "sleap", "-c", "conda-forge", "-c", "nvidia", "-c", "sleap", "-c", "anaconda", "sleap=1.3.3"]