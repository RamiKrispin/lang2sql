FROM python:3.10
ARG METHOD="openai"
ARG ENV_NAME="my_env"
ARG PYTHON_VER="3.10"

RUN mkdir settings
COPY requirements_${METHOD}.txt install_dependencies.sh ./settings/

RUN bash ./settings/install_dependencies.sh $ENV_NAME $PYTHON_VER $METHOD
