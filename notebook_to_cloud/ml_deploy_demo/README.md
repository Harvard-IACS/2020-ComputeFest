# ML From Training to Deployment Demo.
An example repo that shows how to train and deploy a machine learning pipeline in production. Assumes a single package use case. To groom this repo to be a mono-repo that supports multiple packages, a bit of adaptation is required.

## Getting Started
The example we use is a simple text sentiment classifier, trained with `tf.keras` (see [here](https://www.tensorflow.org/api_docs/python/tf/keras)) on the IMDB movie review dataset. We will not focus much on this training, but it is provided in `ml_deploy_demo/pipelines/keras.py`. Our main concern will be to serve up the trained model so that users can send text to it and get a sentiment prediction back.

## Prerequisites
Your development and production environments are constructed by [Docker](docker.com). Install Docker for Desktop for your OS.

To verify that Docker is installed, run `docker --version`.

## Simple Case: One Container
In this directory, we have `Dockerfile`, a blueprint for our development environment, and `requirements.txt` that lists the python dependencies.

To serve the provided pre-trained model, follow these steps:
1. `git clone` this repo
2. `cd notebook_to_cloud/ml_deploy_demo`
3. `docker build -t ml_deploy_demo:latest .` -- this references the `Dockerfile` at `.` (current directory) to build our **Docker image** & tags the docker image with `ml_deploy_demo:latest`
4. Run `docker images` & find the image id of the newly built Docker image, OR run `docker images | grep ml_deploy_demo | awk '{print $3}'`
5. `docker run -it --rm -p 5000:5000 {image_id} /bin/bash ml_deploy_demo/run.sh` -- this refers to the image we built to run a **Docker container**

If everything worked properly, you should now have a container running, which:
1. Spins up a Flask server that accepts POST requests at http://0.0.0.0:5000/predict
2. Runs a Keras sentiment classifier on the `"data"` field of the request (which should be a **list of text strings**: e.g. `'{"data": ["this is the best!", "this is the worst!"]}'`)
3. Returns a response with the model's prediction (1 = positive sentiment, 0 = negative sentiment)

To test this, you can either:
1. Run `make test_api`
2. Write your own POST request (e.g. using [Postman](https://www.getpostman.com/) or `curl`), here is an example response:
```
{
    "input": {
        "data": [
            "this workshop is fun",
            "this workshop is boring"
        ]
    },
    "pred": [
        [
            0.9856576323509216      # closer to 1 => positive
        ],
        [
            0.19903425872325897     # closer to 0 => negative
        ]
    ]
}
```

## Multiple Containers
*Make sure you successfully completed the above example before proceeding.*

To run docker multiple containers, we use `docker-compose`. To verify it is installed, run `docker-compose --version`. Refer to this [documentation](https://docs.docker.com/compose/install/) for more about `docker-compose`.

 The playbook for `docker-compose` is in `docker-compose.yaml`, a handy configuration file for controlling multiple docker containers.

 We also provide a script to launch `docker-compose` in `scripts/`.

```bash
# the actual command is inside this bash script
chmod +x ./scripts/start_docker.sh
./scripts/start_docker.sh
```

To see which docker containers are running,
```bash
docker ps
```

Currently, we support three docker images where each serves a different purpose:
- `ml_deploy_demo_jupyter`: a server for running jupyter notebooks.
- `ml_deploy_demo_app`: a web server for running a flask-based ML API.
- `ml_deploy_demo_dev`: a container for interactive debugging (you get into the interactive shell of the container and run scripts).

To get into a running docker container, we provide helpful commands in the `Makefile` which allows you to do:
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

## Project Structure
```
ml_deploy_demo
├── LICENSE
├── Makefile: a set of handy commands.
├── README.md
├── VERSION: a semantic version file for the codebase.
├── Dockerfile: instruction for docker image construction.
├── docker-compose.yaml: instruction for making and running multiple docker images.
├── requirements.txt: dependencies.
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
│   │   └── keras.py
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
│   └── stop_docker.sh
├── setup.py: an instruction for packaging the codebase as a python package.
└── tests
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
- dhfromkorea@gmail.com (M.E. IACS, Harvard University)
- dylanrandle@gmail.com (M.S. Data Science, Harvard University)
- bpatel@g.harvard.edu (M.E. IACS, Harvard University)

## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

## Docker
Building docker images may take several minute.
