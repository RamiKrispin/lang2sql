#!/bin/bash

ENV_NAME=$1
REQUIREMENTS=$2

source ./root/.bashrc
conda activate $ENV_NAME

# # Install the Python packages
if [[ $REQUIREMENTS == "openai" ]] ; then
pip3 install -r /settings/requirements_openai.txt
elif [[ $REQUIREMENTS == "transformers" ]] ; then
pip3 install -r /settings/requirements_transformers.txt
fi