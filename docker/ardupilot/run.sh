#!/usr/bin/env bash

# docker network create --driver bridge ardupilot-network

docker run -it \
    --rm \
    --name ardupilot \
    --network ardupilot-network \
    --ip 172.18.0.2 \
    clydemcqueen/ardupilot:latest
