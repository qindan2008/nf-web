#!/usr/bin/env bash

# Set FLOWS_DEPLOYMENT_NAME if you want the docker compose containers
# to be prefixed with a different name to flows_integration_test
if [ -z "$FLOWS_DEPLOYMENT_NAME" ]; then
  FLOWS_DEPLOYMENT_NAME=flows_integration_test
fi
DEPLOYMENT_NAME=$FLOWS_DEPLOYMENT_NAME

if [ -z "$FLOWS_TEST_URL" ]; then
  FLOWS_TEST_URL=127.0.0.1:9997
fi
export FLOWS_TEST_URL=$FLOWS_TEST_URL

if [ -z "$POSTGRES_TEST_URL" ]; then
  POSTGRES_TEST_URL=127.0.0.1:9998
fi
export POSTGRES_TEST_URL=$POSTGRES_TEST_URL

FLOWS_SERVICE_NAME=${DEPLOYMENT_NAME}_flows
export FLOWS_CONTAINER_NAME=${FLOWS_SERVICE_NAME}

pushd `dirname $0`

# Setup tests results directory
RESULTS_DIR=test_results/
mkdir -p $RESULTS_DIR

TEST_DIR=tests
export PYTHONPATH=$PWD
python3 -m tests.prepopulate
#pytest $TEST_DIR/test_processing.py::test_run_pipeline --junitxml=${RESULTS_DIR}junit.xml $@
rc=$?
popd

exit $rc
