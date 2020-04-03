#!/bin/sh

echo "Waiting for postgres ..."
#while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
#  sleep 0.1
#done
sleep 20
echo "$POSTGRES_HOST:$POSTGRES_PORT is up."

exec "$@"