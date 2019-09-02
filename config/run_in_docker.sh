#!/usr/bin/env bash

pushd `dirname $0` > /dev/null

set -a
source .env
set +a

# Service URL's
export PROCESSING_URL=http://${DEPLOYMENT_NAME}_processing_1:8000
export ODDJOB_URL=http://${DEPLOYMENT_NAME}_oddjob_1:8000
export FLOWS_URL=http://${DEPLOYMENT_NAME}_flows_1:8000

# Database connection strings
export ODDJOB_DB_URL=postgresql://test_oddjob_service:myfirstoddjobpassword@${DEPLOYMENT_NAME}_postgres_1:5432/oddjob
export PROCESSING_DB_URL=postgresql://test_processing_service:myfirstprocessingpassword@${DEPLOYMENT_NAME}_postgres_1:5432/processing
export FLOWS_DB_URL=postgresql://test_flows_service:myfirstflowspassword@${DEPLOYMENT_NAME}_postgres_1:5432/flows

# Fetch wr token and certificate
export NF_AUTH_TOKEN=test-authtoken
export NF_SERVER_HOST=http://nextflow:8000
#export NF_SERVER_HOST=http://nf-server.cellgeni.sanger.ac.uk
#export TEST_DIR=tests
#cd $TEST_DIR
#export PYTHONPATH=$PYTHONPATH:$PWD

# Build and run test container
IMAGE_NAME=processing_test_runner
CONTAINER_NAME=processing_test_runner

docker rm $CONTAINER_NAME || echo "Ignore error - no container to remove"
docker build -t $IMAGE_NAME .
docker run \
  --name $CONTAINER_NAME \
  --network ${DEPLOYMENT_NAME}_test_network \
  -e PROCESSING_URL \
  -e ODDJOB_URL \
  -e FLOWS_URL \
  -e FLOWS_DB_URL \
  -e ODDJOB_DB_URL \
  -e PROCESSING_DB_URL \
  -e NF_AUTH_TOKEN \
  -e NF_SERVER_HOST \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -p 0.0.0.0:8888:8888 \
  $IMAGE_NAME ./run.sh $@
rc=$?
mkdir -p test_results/
#docker cp $CONTAINER_NAME:/test_results/junit.xml test_results/

popd > /dev/null

exit $rc
