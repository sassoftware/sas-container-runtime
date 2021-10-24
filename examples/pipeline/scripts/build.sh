#!/bin/bash

docker build -t pipeline:1.0.0 .
docker tag pipeline:1.0.0 dbcsv:1.0.0
docker tag pipeline:1.0.0 scrwrapper:1.0.0
docker tag pipeline:1.0.0 dbredis:1.0.0
docker tag pipeline:1.0.0 dbconsole:1.0.0
docker images
