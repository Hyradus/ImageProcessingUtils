#!/bin/bash
DOCKERFILE=IPU.Dockerfile

echo "\n-j Creating IPU:lab image"
IPU_IMAGE="ipu:lab"
docker build -t "$IPU_IMAGE"               \
        -f $PWD/Dockerfiles/$DOCKERFILE .

[ $? ] && echo "Docker image $IPU_IMAGE built."
