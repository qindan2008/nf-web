#!/usr/bin/env bash

export PYTHONPATH=$PWD/../nf_web/
export SQLALCHEMY_DATABASE_URI="sqlite:///:memory:"
export SQLALCHEMY_TRACK_MODIFICATIONS=0
export SQLALCHEMY_ECHO=0
export SQLALCHEMY_RECORD_QUERIES=0

TEST_DIR=`dirname $0`

# Setup results directory
RESULTS_DIR=`dirname $0`/test_results/
mkdir -p $RESULTS_DIR

pytest $TEST_DIR --junitxml=${RESULTS_DIR}junit.xml
