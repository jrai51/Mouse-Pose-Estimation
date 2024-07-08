FROM condaforge/mambaforge
WORKDIR /usr/src/app
COPY ./ ./
RUN mamba create -y -n sleap -c conda-forge -c nvidia -c sleap -c anaconda sleap=1.3.3

RUN mamba init


RUN git clone https://github.com/talmolab/sleap && cd sleap

RUN mamba env create -f environment.yml -n sleap
RUN mamba create --name sleap pip python=3.7.12 cudatoolkit=11.3 cudnn=8.2

RUN mamba activate sleap
RUN pip install sleap[pypi]==1.3.3

RUN mamba activate sleap