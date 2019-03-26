#!/usr/bin/env bash

set -e

ODDJOB_CONTAINER_NAME=${DEPLOYMENT_NAME}_oddjob_1
DB_TOOL_CONFIG=db_tool_config.ini

# Create database
docker exec \
    -u root \
    $ODDJOB_CONTAINER_NAME \
    bash -c "cgpaasOddjob database build -c $DB_TOOL_CONFIG \
          && cgpaasOddjob database dicts -c $DB_TOOL_CONFIG"
