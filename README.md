# lang2sql

🚧WIP 🏗️, pre spell checking🛠️

This repo provides a step-by-step guide and a template for setting up a natural language to SQL code generator with the OpneAI API.

## Table of Contents:
- [Motivation](https://github.com/RamiKrispin/lang2sql#motivation)
- [Scope and General Architecture](https://github.com/RamiKrispin/lang2sql#scope-and-general-architecture)
- [Prerequisites](https://github.com/RamiKrispin/lang2sql#prerequisites)
- [Data](https://github.com/RamiKrispin/lang2sql#data)
- [Setting up SQL generator](https://github.com/RamiKrispin/lang2sql#setting-up-sql-generator)
- [Summary](https://github.com/RamiKrispin/lang2sql#summary)
- [Resources](https://github.com/RamiKrispin/lang2sql#resources)
- [License](https://github.com/RamiKrispin/lang2sql#license)


## Motivation

The rapid development of natural language models, especially Large Language Models (LLMs), has presented numerous possibilities for various fields. One of the most common applications is using LLMs for coding. For instance, OpenAI's chatGPT and Meta's Code LLAMA are LLMs that offer state-of-the-art natural language to code generators. One potential use case is a natural language to SQL code generator, which could assist non-technical professionals with simple data requests and hopefully enable the data teams to focus on more data-intensive tasks. This tutorial focuses on setting up a language for SQL code generator using the OpenAI API.

### What can you do with language to SQL code generator application?

One possible application is a chatbot that can respond to user queries with relevant data (Figure 1). The chatbot can be integrated with a Slack channel using a Python application that performs the following steps: 
- Receives the user's question 
- Converts the question into a prompt
- Sends a GET request to the OpenAI API with the prompt 
- Parses the returned JSON into a SQL query 
- Sends the query to the database 
- Returns the user a CSV file containing the relevant data

<figure>
<img src="images/general_arch1.png" width="100%" align="center"/></a>
<figcaption> Figure 1 - Language to SQL code generator use case</figcaption>
</figure>


In this tutorial, we will build a step-by-step Python application that converts user questions into SQL queries.

## Scope and General Architecture

This tutorial provides a step-by-step guide on how to set up a Python application that converts general questions into SQL queries using the OpenAI API. That includes the following functionality:
- Generalized - the application is not limited to a specific table and can be used on any table
- For simplicity, the application is limited to a single table (e.g., no joins)
- Dockerized - develop the application inside a dockerized environment for a simple deployment

Figure 2 below describes the general architecture of a simple language to SQL code generator. 

<figure>
<img src="images/general_arch2.png" width="100%" align="center"/></a>
<figcaption> Figure 2 - Language to SQL code generator general architecture</figcaption>
</figure>


The scope and focus of this tutorial is on the green box - building the following functionality:
- **Question to Prompt** - transform the question into a prompt format:    
    - Pull the table information to create the prompt context
    - Add the question to the prompt

- **API Handler** - a function that works with the OpenAI API:
    - Send a GET request with the prompt
    - Parse the answer into an SQL query
- **DB Handler** - a function that sends the SQL query to the database and returns the required data

## Prerequisites

The main prerequisite for this tutorial is basic knowledge of Python. That includes the following functionality:
- Setting Python functions and objects
- Working with tabular data (i.e., pandas, CSV, etc.) and non-structure data format(i.e., JSON, etc.)
- Working with Python libraries 

In addition, basic knowledge of SQL and access to the OpenAI API are required.

### Nice to Have

While not necessary, having a basic knowledge of Docker is helpful, as the tutorial was created in a Dockerized environment using VScode's Dev Containers extension. If you don't have experience with Docker or the extension, you can still run the tutorial by creating a virtual environment and installing the required packages (as described below). Knowledge of Prompt engineering and the OpenAI API is also beneficial.

I created a detailed tutorial about setting a Python dockerized environment with VScode and the Dev Containers extension:

https://github.com/RamiKrispin/vscode-python

### Python Libraries

To set up a natural language to SQL code generation, we will use the following Python libraries:
- `pandas` - to process data throughout the process
- `duckdb` - to simulate the work with the database
- `openai` - to work with the OpenAI API
- `time` and `os` - to load CSV files and format fields 


If you are not using the tutorial dockerized environment, you can create a local virtual environment from the command line using the script below:

```shell
ENV_NAME=openai_api
PYTHON_VER=3.10
conda create -y --name $ENV_NAME python=$PYTHON_VER 

conda activate $ENV_NAME

pip3 install -r ./.devcontainer/requirements_core.txt
pip3 install -r ./.devcontainer/requirements_openai.txt

```

**Note:** I used `conda` and it should work as well with any other virutal environment method.

We use the `ENV_NAME` and `PYTHON_VER` variables to set the virtual environment and the Python version, respectively.

To confirm that your environment is properly set, use the `conda list` to confirm that the required Python libraries are installed. You should expect the below output:

```shell
(openai_api) root@0ca5b8000cd5:/workspaces/lang2sql# conda list
# packages in environment at /opt/conda/envs/openai_api:
#
# Name                    Version                   Build  Channel
_libgcc_mutex             0.1                        main  
_openmp_mutex             5.1                      51_gnu  
aiohttp                   3.9.0                    pypi_0    pypi
aiosignal                 1.3.1                    pypi_0    pypi
asttokens                 2.4.1                    pypi_0    pypi
async-timeout             4.0.3                    pypi_0    pypi
attrs                     23.1.0                   pypi_0    pypi
bzip2                     1.0.8                hfd63f10_2  
ca-certificates           2023.08.22           hd43f75c_0  
certifi                   2023.11.17               pypi_0    pypi
charset-normalizer        3.3.2                    pypi_0    pypi
comm                      0.2.0                    pypi_0    pypi
contourpy                 1.2.0                    pypi_0    pypi
cycler                    0.12.1                   pypi_0    pypi
debugpy                   1.8.0                    pypi_0    pypi
decorator                 5.1.1                    pypi_0    pypi
duckdb                    0.9.2                    pypi_0    pypi
exceptiongroup            1.2.0                    pypi_0    pypi
executing                 2.0.1                    pypi_0    pypi
fonttools                 4.45.1                   pypi_0    pypi
frozenlist                1.4.0                    pypi_0    pypi
gensim                    4.3.2                    pypi_0    pypi
idna                      3.5                      pypi_0    pypi
ipykernel                 6.26.0                   pypi_0    pypi
ipython                   8.18.0                   pypi_0    pypi
jedi                      0.19.1                   pypi_0    pypi
joblib                    1.3.2                    pypi_0    pypi
jupyter-client            8.6.0                    pypi_0    pypi
jupyter-core              5.5.0                    pypi_0    pypi
kiwisolver                1.4.5                    pypi_0    pypi
ld_impl_linux-aarch64     2.38                 h8131f2d_1  
libffi                    3.4.4                h419075a_0  
libgcc-ng                 11.2.0               h1234567_1  
libgomp                   11.2.0               h1234567_1  
libstdcxx-ng              11.2.0               h1234567_1  
libuuid                   1.41.5               h998d150_0  
matplotlib                3.8.2                    pypi_0    pypi
matplotlib-inline         0.1.6                    pypi_0    pypi
multidict                 6.0.4                    pypi_0    pypi
ncurses                   6.4                  h419075a_0  
nest-asyncio              1.5.8                    pypi_0    pypi
numpy                     1.26.2                   pypi_0    pypi
openai                    0.28.1                   pypi_0    pypi
openssl                   3.0.12               h2f4d8fa_0  
packaging                 23.2                     pypi_0    pypi
pandas                    2.0.0                    pypi_0    pypi
parso                     0.8.3                    pypi_0    pypi
pexpect                   4.8.0                    pypi_0    pypi
pillow                    10.1.0                   pypi_0    pypi
pip                       23.3.1          py310hd43f75c_0  
platformdirs              4.0.0                    pypi_0    pypi
prompt-toolkit            3.0.41                   pypi_0    pypi
psutil                    5.9.6                    pypi_0    pypi
ptyprocess                0.7.0                    pypi_0    pypi
pure-eval                 0.2.2                    pypi_0    pypi
pygments                  2.17.2                   pypi_0    pypi
pyparsing                 3.1.1                    pypi_0    pypi
python                    3.10.13              h4bb2201_0  
python-dateutil           2.8.2                    pypi_0    pypi
pytz                      2023.3.post1             pypi_0    pypi
pyzmq                     25.1.1                   pypi_0    pypi
readline                  8.2                  h998d150_0  
requests                  2.31.0                   pypi_0    pypi
scikit-learn              1.3.2                    pypi_0    pypi
scipy                     1.11.4                   pypi_0    pypi
setuptools                68.0.0          py310hd43f75c_0  
six                       1.16.0                   pypi_0    pypi
smart-open                6.4.0                    pypi_0    pypi
sqlite                    3.41.2               h998d150_0  
stack-data                0.6.3                    pypi_0    pypi
threadpoolctl             3.2.0                    pypi_0    pypi
tk                        8.6.12               h241ca14_0  
tornado                   6.3.3                    pypi_0    pypi
tqdm                      4.66.1                   pypi_0    pypi
traitlets                 5.13.0                   pypi_0    pypi
tzdata                    2023.3                   pypi_0    pypi
urllib3                   2.1.0                    pypi_0    pypi
wcwidth                   0.2.12                   pypi_0    pypi
wheel                     0.41.2          py310hd43f75c_0  
xz                        5.4.2                h998d150_0  
yarl                      1.9.3                    pypi_0    pypi
zlib                      1.2.13               h998d150_0  

```

### Setting Access to the OpenAI API

We will use the OpenAI API to access chatGPT using the text-davinci-003 engine. This required an active OpenAI account and API key. It is straightforward to set an account and API key following the instructions in the below link:

https://openai.com/product

Once you set the access to the API and a key, I recommend adding the key as an environment variable to your `.zshrc` file (or any other format you are using to store environment variables on your shell system). I stored my API key under the `OPENAI_KEY` environment variable.  For convincing reasons, I recommend you use the same naming convention.

To set the variable on the `.zshrc` file (or equivalent), add the below line to the file:

```shell
export OPENAI_KEY="YOUR_API_KEY"
```

If using VScode or running from the terminal, you must restart your session after adding the variable to the `.zshrc` file.


## Data

WIP

## Setting up SQL generator

WIP

## Summary

WIP

## Resources

WIP

## License

This tutorial is licensed under a [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International](https://creativecommons.org/licenses/by-nc-sa/4.0/) License.

