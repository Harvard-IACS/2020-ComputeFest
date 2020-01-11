#!/bin/bash

# project-name is used when creating container names
# -d making the containers running in a detached mode (as a background process)
# --build telling docker-compose that we allow re-building images if there are existing ones.
docker-compose -f docker-compose.yaml --project-name ml_deploy_demo up --build -d
