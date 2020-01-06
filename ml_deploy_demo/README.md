# ML From Training to Deployment Demo.
An example repo that shows how to train and deploy a machine learning pipeline in production. Assumes a single package use case. To groom this repo to be a mono-repo that supports multiple packages, a bit of adapation is required.

## Getting Started

### Project Structure

```
ml_deploy_demo
├── LICENSE
├── Makefile: a set of handy commands.
├── README.md
├── VERSION: a semantic version file for the codebase.
├── docker
│   ├── Dockerfile: instruction for docker image construction.
│   ├── docker-compose.yaml: instruction for making and running multiple docker images.
│   └── requirements.txt: dependencies.
├── experiment_configs: a config file that defines an experiment.
│   └── default.yaml: a default exp config file.
├── experiment_output: save all training/experiment logs here.
├── log: save all non-experiment logs here (for production you would use other paths e.g. /var/log).
├── logging.yaml: a config path for logging.
├── ml_deploy_demo
│   ├── api: the Flask app for running an ML API service.
│   │   ├── app.py
│   │   └── ml_app.py
│   ├── models: ML model/algo definitions go here.
│   │   └── neural_networks.py
│   ├── pipelines: training pipelines (for demo purpose).
│   │   └── sklearn.py
│   ├── preprocessing: feature engineering, data augmentation/transformations.
│   │   └── preprocessing.py
│   ├── run.py: an entry module for Flask
│   ├── run.sh: an entry script for Flask
│   ├── train.py: the module for training.
│   ├── predict.py: the module for predicting.
│   └── util: utility functions.
│       └── utils.py
├── models: a local model registry. Models that are acceptably good are promoted to move here.
│   └── iris: a task name.
│       └── v1.joblib: a model with its version.
├── notebooks: notebook files are here.
├── scripts: utility commands go here (also things that could be run by docker runtime).
│   └── start_docker.sh
├── setup.py: an instruction for packaging the codebase as a python package.
└── tests
```

### Prerequisites

Your development and production environments are constructed by Docker. Install Docker for Desktop for your OS.

To verify:
```bash
docker --version
docker-compose --version
```

Regarding docker-compose, refer to this [doc](https://docs.docker.com/compose/install/).


### Development Environments
In `docker/` directiory, we have `Dockerfile`, a blueprint for our development environment, `docker-compose.yaml`, a handy configuration file for controlling multiple docker containers, and `requirements.txt` that lists the python dependencies.

Currently, we support three docker images where each serves a different purpose:
- `ml_deploy_demo_jupyter`: a server for running jupyter notebooks.
- `ml_deploy_demo_app`: a web server for running a flask-based ML API.
- `ml_deploy_demo_dev`: a container for interactive debugging (you get into the interactive shell of the container and run scripts).

To get into a running docker container, you just need to do.
```bash
# container_id can be obtained from docker ps
docker exec -it ${CONTAINER_ID} /bin/bash
# alternative, and more conveniently, you can just
make run_docker_notebook
# or
make run_docker_app
# or
make run_docker_dev
```

#### Running Multiple Dockers At Once
To run docker multiple containers, we use `docker-compose`.

```bash
# the actual command is inside this bash script
chmod +x ./scripts/start_docker.sh
./scripts/start_docker.sh
```

To see docker containers are running,
```bash
docker ps
```
## Training (Experiment Configurations)
All experiments are expected to be configured via files in `experiment_configs/*.yaml`. This declarative approach allows you to run reproducible experiments at scale. It is reproducible because you can have a full control over the setup of an experiment and the setup can be checkpointed via git. You can also discuss the setup with your colleagues using Github UI. It is more scalable because each config file can act as the abstraction as a training job. As such, if you have a distributed training system (e.g. HPC), you can asign config file to a node(s) in parallel. Since all artifcats related to an experiment has its own output directory, one can inspect the results of each experiment in isolation.

@todo: add more advice.
Ideally, you would want to have a more advanced tools for experiment tracking.

## Running API service
The prediction endpoint is exposed, by default, at `http://0.0.0.0:5000/predict` where a sklearn model trained on Iris dataset is serving. You can make a POST request with a json object has the key "data" to receive predictions of the model.

An example can be found in `Makefile`.
```bash
make test_api
```
More advanced API development tools like [POSTMAN](https://www.getpostman.com/) are preferred.


## Deployment

## Running the tests
@todo: general CI/CD description goes here. remove if we're not going to cover it.

### Coding Style
```
make black
make flake8
```

## Deployment
Add additional notes about how to deploy this on a live system


## Contributing
TBD

## Versioning
We use [SemVer](http://semver.org/) for versioning.

## Authors
dhfromkorea@gmail.com (M.E. IACS, Harvard University)

## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

## Docker
Building docker images may take several minute.

