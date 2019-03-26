#!/usr/bin/env bash

SCRIPT=`basename "$0"`
PSQL_PGHBA=/var/lib/postgresql/data/pgdata/pg_hba.conf

create_db() {

service=$1

echo "Service: $service"

createdb "$service"

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" -d "$service" <<-EOSQL
    CREATE USER test_${service}_service WITH PASSWORD 'myfirst${service}password';
EOSQL

HOST_LOGIN_STRING="host \"${service}\" all 0.0.0.0/0 password"
if ! grep "$HOST_LOGIN_STRING" $PSQL_PGHBA ; then
    echo $HOST_LOGIN_STRING >> $PSQL_PGHBA
fi

}

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
    CREATE EXTENSION adminpack;
EOSQL

LISTEN_STRING="listen_addresses = '*'"
PSQL_CONF=/var/lib/postgresql/data/pgdata/postgresql.conf
if ! grep "$LISTEN_STRING" $PSQL_CONF ; then
    echo $LISTEN_STRING >> $PSQL_CONF
fi

# Add databases
create_db "flows"
create_db "oddjob"
create_db "processing"
