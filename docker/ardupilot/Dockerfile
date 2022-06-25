FROM ubuntu:20.04
WORKDIR /ardupilot

ARG DEBIAN_FRONTEND=noninteractive
RUN useradd -U -m ardupilot && \
    usermod -G users ardupilot

RUN apt-get update && apt-get install --no-install-recommends -y \
    lsb-release \
    sudo \
    bash-completion \
    software-properties-common

# Some handy tools
RUN apt-get update && apt-get install --no-install-recommends -y \
    git \
    glmark2 \
    iputils-ping \
    mlocate \
    vim

# Create non root user for pip
ENV USER=ardupilot

RUN echo "ardupilot ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/ardupilot
RUN chmod 0440 /etc/sudoers.d/ardupilot

RUN chown -R ardupilot:ardupilot /ardupilot

USER ardupilot

# Clone, don't copy
RUN git clone https://github.com/clydemcqueen/ardupilot --recurse-submodules
WORKDIR /ardupilot/ardupilot

ENV SKIP_AP_EXT_ENV=1 SKIP_AP_GRAPHIC_ENV=1 SKIP_AP_COV_ENV=1 SKIP_AP_GIT_CHECK=1
RUN Tools/environment_install/install-prereqs-ubuntu.sh -y

# Set the buildlogs directory into /tmp as other directory aren't accessible
ENV BUILDLOGS=/tmp/buildlogs

# Cleanup
RUN sudo apt-get clean \
    && sudo rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

ENV CCACHE_MAXSIZE=1G

# Compile ArduSub
RUN ./waf configure --board sitl
RUN ./waf sub

# Add .local/bin to the path
ENV HOME=/home/ardupilot
ENV PATH=${HOME}/.local/bin:${PATH}

# MAV interface from GCS -> ArduPilot
# SITL_cmdline.cpp:212
EXPOSE 5760/tcp

# RC interface for RC input from GCS -> ArduPilot
# SITL_cmdline.cpp:213
EXPOSE 5501/udp

# JSON interface for physics from Gazebo -> ArduPilot
# SITL_cmdline.cpp:219
EXPOSE 9003/udp
