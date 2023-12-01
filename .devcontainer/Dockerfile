FROM python:3.10
ARG METHOD="openai"
ARG ENV_NAME="my_env"
ARG PYTHON_VER="3.10"
ARG QUARTO_VER="1.3.450"

RUN mkdir settings
COPY requirements_core.txt install_dependencies_core.sh ./settings/
RUN bash ./settings/install_dependencies_core.sh $ENV_NAME $PYTHON_VER $METHOD

COPY requirements_${METHOD}.txt install_dependencies_other.sh ./settings/
RUN bash ./settings/install_dependencies_other.sh $ENV_NAME $METHOD

COPY install_quarto.sh ./settings/
RUN bash ./settings/install_quarto.sh $QUARTO_VER
