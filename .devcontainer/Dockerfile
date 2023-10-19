FROM python:3.10

ARG ENV_NAME="my_env"
ARG PYTHON_VER="3.10"

RUN mkdir settings
COPY requirements.txt install_dependencies.sh ./settings/

RUN bash ./settings/install_dependencies.sh $ENV_NAME $PYTHON_VER
