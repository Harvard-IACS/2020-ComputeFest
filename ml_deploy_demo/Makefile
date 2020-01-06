# @note: using $$ is not a bug.
DEV_CONTAINER_ID=$$(docker ps | grep ml_deploy_demo_dev | awk '{print $$1}')
NOTEBOOK_CONTAINER_ID=$$(docker ps | grep ml_deploy_demo_jupyter | awk '{print $$1}')
APP_CONTAINER_ID=$$(docker ps | grep ml_deploy_demo_app | awk '{print $$1}')

PROJECT="ml_deploy_demo"

run_docker_dev:
	docker exec -it ${DEV_CONTAINER_ID} /bin/bash

run_docker_notebook:
	docker exec -it ${NOTEBOOK_CONTAINER_ID} /bin/bash

run_docker_app:
	docker exec -it ${APP_CONTAINER_ID} /bin/bash

clean:
	find . -name '*.pyc' -delete
	find . -name '*.pyo' -delete
	find . -regex '^.*\(__pycache__\|\.py[co]\)$$' -delete

flake8:
	flake8 ${PROJECT} --ignore=E203,E501,W503,E722

black:
	black ${PROJECT}

