# @note: we start with a smal docker image that contains a python3.7.0 runtime.
#        docker names usually follow {registry}/{img_name}:{tag} structure.
#        if omit the registry name here, it defaults to the official docker registry.
#        in production env, you would want to host your own docker registry.
FROM python:3.7.0

# assuming dockerfile is run within docker/ folder.
# @note: args don't last past a FROM command. Hence, they must be put after FROM.
#        typically, these are to be filled in by your CI/CD system.
ARG PROJECT_ROOT="../"
ARG PROJECT_NAME="ml_deploy_demo"
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
ARG USER_NAME="ml_deploy"
RUN adduser --disabled-password --gecos '' $USER_NAME

# @note: this will create the path if not existing (=mkdir -p).
ADD $PROJECT_ROOT/requirements.txt $PROJECT_MOUNT_DIR/$PROJECT_NAME/requirements.txt

# change the workdir to $PROJECT_MOUNT_DIR/ml_deploy_demo
# @note: this will create the path if not existing (=mkdir -p).
WORKDIR $PROJECT_MOUNT_DIR/$PROJECT_NAME

# pip3 by default as the base image is python 3+
# @note: each docker RUN create a new "layer".
#        to avoid unnecessary networking/computations
#        it's best practice to group commands
#        if they can be meaningfully and functionally grouped.
RUN pip install --upgrade pip && \
    pip install -r requirements.txt
   
# copy project source code (in a host) to docker.
ADD $PROJECT_ROOT/$PROJECT_NAME $PROJECT_MOUNT_DIR/$PROJECT_NAME

WORKDIR $PROJECT_MOUNT_DIR

# set the default user
USER $USER_NAME

# expose a specific port for communicating w/ the world outside docker.
EXPOSE 5000
