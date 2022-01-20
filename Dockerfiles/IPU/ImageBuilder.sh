#!/bin/bash

GDAL_VERSION='3.4.1'
JUPYTER_ENABLE_LAB='yes'
DOCKERFILE=IPU.dockerfile


BASE_IMAGE="osgeo/gdal:ubuntu-full-$GDAL_VERSION"


echo "\n-j Creating jupyter:gdal image"
JUPYTER_IMAGE="jupyter:gdal"
git clone 'https://github.com/jupyter/docker-stacks.git'
(
cd docker-stacks
docker build -t "$JUPYTER_IMAGE"                 \
        --build-arg ROOT_CONTAINER="$BASE_IMAGE" \
        base-notebook/
)
[ $? ] && rm -rf docker-stacks && echo "Docker image $OUTPUT_IMAGE built."

IPU_IMAGE="ipu:jupyter"

echo "Creating $IPU_IMAGE image"
docker build -t "$IPU_IMAGE"                              \
        --build-arg BASE_IMAGE="$JUPYTER_IMAGE"               \
        --build-arg JUPYTER_ENABLE_LAB=$JUPYTER_ENABLE_LAB \
        -f $PWD/$DOCKERFILE .

[ $? ] && echo "Docker image $IPU_IMAGE built."
