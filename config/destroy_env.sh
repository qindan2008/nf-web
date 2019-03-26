#!/usr/bin/env bash

if [ -z `which jq` ]; then
  echo "The tool 'jq' needs to be installed. On Ubuntu 'sudo apt install jq'"
  exit 1
fi

pushd `dirname $0`

source .env

# Find the volume attached to postgres. We know from the project name and the docker-compose
# file that the container name will be ${DEPLOYMENT_NAME}_postgres_1.
# MAGIC STRING
volume_name=`docker inspect ${DEPLOYMENT_NAME}_postgres_1 | jq -r '.. | select(objects.Type == "volume" and objects.Destination == "/var/lib/postgresql/data") | .Name'`
echo $volume_name

docker-compose -p $DEPLOYMENT_NAME down

# Because the postgres container creates a internal volume that docker-compose won't remove,
# we have to remove it manually
docker volume rm $volume_name

popd
