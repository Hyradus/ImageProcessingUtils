#!/bin/bash
DOCKERFILE=IPU.Dockerfile

echo "\n-j Creating IPU:jupyter image"
IPU_IMAGE="ipu:jupyter"
docker build -t "$IPU_IMAGE"               \
        -f $PWD/Dockerfiles/$DOCKERFILE .

[ $? ] && echo "Docker image $IPU_IMAGE built."
