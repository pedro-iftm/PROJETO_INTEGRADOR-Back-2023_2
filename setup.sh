#!/usr/bin/env bash
pip3 install virtualenv
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
docker-compose down
docker-compose up -d postgres
docker-compose down
deactivate
