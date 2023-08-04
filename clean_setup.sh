#!/usr/bin/env bash
deactivate
rm -rf venv/
docker-compose up -d postgres
docker-compose down -v
docker system prune
docker image prune
docker volume prune
docker container prune
docker image rm $(docker image ls -a -q)
