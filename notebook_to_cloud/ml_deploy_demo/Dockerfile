# @note: we start with the tensorflow 2.1 docker image with python3 and jupyter
#        docker names usually follow {registry}/{img_name}:{tag} structure.
#        if omit the registry name here, it defaults to the official docker registry.
#        in production env, you would want to host your own docker registry.
ARG BASE_IMG=tensorflow/tensorflow:2.1.0-py3-jupyter
FROM $BASE_IMG

# @note: args don't last past a FROM command. Hence, they must be put after FROM.
#        typically, these are to be filled in by your CI/CD system.
ARG PROJECT_ROOT="."
ARG PROJECT_MOUNT_DIR="/app"

# We avoid running docker as root at construction.
# @note: if you mount your host filesystem on docker
#        changes you make to the filesystem mounted on docker
#        apply to your host filesystem.
#        e.g. if you delete a file X, it will be deleted on your host as well.
#        by creating a separate user and assign a limited permission to it,
#        we avoid the catastrophic situation. by default, docker runs as root!
# https://stackoverflow.com/questions/27701930/add-user-to-docker-container
# https://medium.com/jobteaser-dev-team/docker-user-best-practices-a8d2ca5205f4
# ARG USER_NAME="ml_deploy"
# RUN adduser --disabled-password --gecos '' $USER_NAME

# @note: this will create the path if not existing (=mkdir -p).
ADD $PROJECT_ROOT $PROJECT_MOUNT_DIR

# change the workdir to $PROJECT_MOUNT_DIR
# @note: this will create the path if not existing (=mkdir -p).
WORKDIR $PROJECT_MOUNT_DIR

# pip3 by default as the base image is python 3+
# @note: each docker RUN create a new "layer".
#        to avoid unnecessary networking/computations
#        it's best practice to group commands
#        if they can be meaningfully and functionally grouped.
RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip install .

# set the default user
# USER $USER_NAME
