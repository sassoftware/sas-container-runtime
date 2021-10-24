#!/bin/sh
# 
# get the latest redis 
# load the image for homeloan - provided as as example
# Make sure you have a homeloan:1.0.0 image in your docker
#
docker pull redis:latest 
# docker load -i ./docker-images/homeloan.jar
scripts/build.sh
