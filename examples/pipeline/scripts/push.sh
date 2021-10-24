#!/bin/bash
crname=$1
cr=$1.azurecr.io
az acr login -n $1
echo $cr

docker tag pipeline:1.0.0 $cr/pipeline:1.0.0
docker tag dbcsv:1.0.0 $cr/dbcsv:1.0.0
docker tag scrwrapper:1.0.0 $cr/scrwrapper:1.0.0
docker tag dbredis:1.0.0 $cr/dbredis:1.0.0
docker tag redis:latest $cr/redis:latest
docker tag homeloan:1.0.0 $cr/homeloan:1.0.0
docker tag dbconsole:1.0.0 $cr/dbconsole:1.0.0

docker images | grep $cr

docker push $cr/pipeline:1.0.0
docker push $cr/dbcsv:1.0.0
docker push $cr/scrwrapper:1.0.0
docker push $cr/dbredis:1.0.0
docker push $cr/redis:latest
docker push $cr/homeloan:1.0.0
docker push $cr/dbconsole:1.0.0


