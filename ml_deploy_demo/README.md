An example of a machine learning pipeline from training to deployment. Assumes a single package use case. To groom this repo to be a mono-repo that supports multiple packages, a bit of adapation is required.

## Docker
Building docker images may take several minute.

To build a set of docker containers for development.
```bash
# project-name is used when creating container names
# -d making the containers running in a detached mode (as a background process)
# --build telling docker-compose that we allow re-building images if there are existing ones.
docker-compose -f docker/docker-compose.yaml --project-name ml_deploy_demo up --build -d
```

To get into a running docker container.
```bash
# container_id can be obtained from docker ps
docker exec -it ${CONTAINER_ID} /bin/bash
```


## Applications/Services (Docker containers)

### Jupyter Notebook
```bash
make run_docker_notebook
```

### API
```bash
make run_docker_app
```

### dev
```bash
make run_docker_dev
```
