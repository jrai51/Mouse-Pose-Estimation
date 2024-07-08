# Use the official NVIDIA CUDA image as a base
FROM nvidia/cuda:12.2.0-devel-ubuntu22.04

# Set the default shell to bash
SHELL ["/bin/bash", "-c"]

# Update and install necessary packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    wget \
    curl \
    ca-certificates \
    sudo \
    git \
    bzip2 \
    libglib2.0-0 \
    libxext6 \
    libsm6 \
    libxrender1 \
    libgl1-mesa-glx \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Python and other essential tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    python3-venv

# Install Mamba
RUN curl -L https://github.com/conda-forge/miniforge/releases/latest/download/Mambaforge-Linux-x86_64.sh -o Mambaforge.sh \
    && bash Mambaforge.sh -b -p /opt/mambaforge \
    && rm Mambaforge.sh \
    && /opt/mambaforge/bin/mamba init

# Set up environment variables for Mamba
ENV PATH=/opt/mambaforge/bin:$PATH

# Set up a user (optional)
RUN useradd -ms /bin/bash user
RUN echo 'user ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

# Change ownership of the Mamba installation directory to the user
RUN chown -R user:user /opt/mambaforge

USER root
WORKDIR /home/user
COPY . .

# Adjust permissions on required directories or files
# RUN chown -R user:user /home/user/predictions
# RUN chmod -R 755 /home/user/predictions

# RUN chown -R user:user /home/user/trial_vids
# RUN chmod -R 755 /home/user/trial_vids

# Create and activate the 'sleap' environment, then install sleap
RUN /bin/bash -c "source /opt/mambaforge/bin/activate && mamba create -y -n sleap -c conda-forge -c nvidia -c sleap -c anaconda sleap && mamba init"

# Expose Jupyter Notebook port
EXPOSE 8888

# Command to keep the container running
CMD ["/bin/bash"]
