#!/bin/sh
docker rmi pipeline:1.0.0
docker rmi dbcsv:1.0.0
docker rmi scrwrapper:1.0.0
docker rmi dbredis:1.0.0
docker images
