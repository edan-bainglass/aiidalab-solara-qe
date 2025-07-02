FROM aiidalab/base-with-services:latest

ARG QE_VER=7.4
ARG QE_DIR=/opt/conda/envs/quantum-espresso-${QE_VER}
ARG COMPUTER_LABEL="localhost"

USER ${NB_USER}

# Install QE
RUN set -ex; \
    echo "Installing QE"; \
    mamba create -p ${QE_DIR} qe=${QE_VER}; \
    mamba clean --all -f -y

# Install app
COPY --chown=jovyan:users . /home/jovyan/solara-qe
WORKDIR /home/jovyan/solara-qe
RUN pip install -e .

# Install pseudopotentials
# RUN set -ex; \
#     echo "Installing pseudopotentials"; \
#     /home/jovyan/solara-qe/install-pseudos.sh; \
#     rm -f /home/jovyan/install-pseudos.sh

EXPOSE 3000

WORKDIR /home/jovyan
