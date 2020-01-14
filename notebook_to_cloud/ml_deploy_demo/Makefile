# @note: using $$ is not a bug.
DEV_CONTAINER_ID=$$(docker ps | grep ml_deploy_demo_dev | awk '{print $$1}')
NOTEBOOK_CONTAINER_ID=$$(docker ps | grep ml_deploy_demo_jupyter | awk '{print $$1}')
APP_CONTAINER_ID=$$(docker ps | grep ml_deploy_demo_app | awk '{print $$1}')

PROJECT="ml_deploy_demo"

# superset of python setup.py install
package_prod:
	pip install .

# superset of python setup.py develop
package_dev:
	pip install --editable .

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

# a hacky way to test api.
test_api:
	curl -i -H "Content-Type: application/json" \
		-X POST -d '{"data": ["this is the best!", "this is the worst!"]}' http://0.0.0.0:5000/predict
