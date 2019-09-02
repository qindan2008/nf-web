#!/usr/bin/env bash

pushd `dirname $0` > /dev/null

set -a
source .env
set +a

set -e

if [ `docker-compose -p $DEPLOYMENT_NAME ps -q | wc -l` != "0" ]; then
  # If the deployment is running, destroy it
    $PWD/destroy_env.sh
fi

docker-compose pull processing flows
docker-compose -p $DEPLOYMENT_NAME -f docker-compose.yml up -d
docker ps

./services/flows.sh
./services/oddjob.sh
./services/processing.sh

popd > /dev/null
