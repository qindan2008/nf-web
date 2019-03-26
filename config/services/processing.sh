#!/usr/bin/env bash

set -e

SERVICE=processing

pushd `dirname $0`

# Generate the DDL
docker exec ${DEPLOYMENT_NAME}_${SERVICE}_1 /opt/cgpaas/scripts/create_ddl.sh > ddl.sql
sed -i -e "s/%cgpaaspgdbuser/test_${SERVICE}_service/g" ddl.sql
docker cp ./ddl.sql ${DEPLOYMENT_NAME}_postgres_1:/tmp/ddl.sql

sleep 0.5

# Create database
docker exec -u postgres ${DEPLOYMENT_NAME}_postgres_1 psql ${SERVICE} -f /tmp/ddl.sql

popd
