#!/usr/bin/env sh

docker-compose pull
docker-compose up -d
docker-compose exec creditoro_api flask db upgrade