FROM mambaorg/micromamba:latest

USER root
# ENV ENV_NAME resume_gen_env 
COPY env.yml /tmp/env.yml
# COPY env.yml /tmp/requirements.txt

RUN apt-get update && \
    apt-get install git -y

RUN micromamba install -n base -f /tmp/env.yml -y && \
    micromamba clean -a -y

SHELL ["/bin/bash", "--login", "-c"]
