ARG BASE_IMAGE=ubuntu:20.04
FROM $BASE_IMAGE AS base

MAINTAINER "Giacomo Nodjoumi <giacomo.nodjoumi@hyranet.info>"

ENV DEBIAN_FRONTEND=noninteractive

# Install Python and its tools

RUN apt update && apt install --no-install-recommends -y 	\
apt-transport-https \
    ca-certificates \
    curl \
    gnupg2 \
    locales \
    nano \
    software-properties-common \
    sudo \
    tzdata \
    vim \
    wget \
    git 							\
    build-essential 				\
    curl 							\
    libgl1-mesa-dev 				\
    libglib2.0-0 					\
    python3.9-dev 					\
    python3-tk                \
    python3.9-distutils 			&& \
    rm -rf /var/lib/apt/lists/*	    && \
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && \
	python3.9 get-pip.py 									&& \
	pip3 -q install pip --upgrade

RUN pip3 --no-cache-dir install 	\
	setuptools 						\
    jupyterlab 						\
    git+https://${GITHUB_TOKEN}@github.com/Hyradus/maxrect.git \
    geopandas \
    numpy 							\
  	opencv-python					\
  	opencv-contrib-python			\
  	pandas							\
  	psutil							\
  	rasterio						\
  	scikit-image					\
  	scikit-learn					\
  	scipy 							\
  	tqdm							\
    spectral \
    && rm -rf /var/lib/apt/lists/*

FROM base AS mip-scr

#RUN mkdir /MIP-SCR && \
#    git clone https://github.com/Hyradus/ImageProcessingUtils.git

ARG UID=1000
ARG GID=100
ARG PASSWORD=123456
RUN useradd -m -d /home/user -u $UID -g $GID -s /bin/bash user 		\
    && su - user -c 'ln -s /mnt/data /home/user/data' 				\
    #&& su - user -c 'ln -s /ImageProcessingUtils/MIP-SCR /home/user/MIP-SCR' \
    #&& su - user -c 'ln -s /Tools /home/user/Tools' \
    && echo "user:$PASSWORD" | chpasswd

ADD ../Tools /home/user/Tools
WORKDIR /home/user/
USER user
