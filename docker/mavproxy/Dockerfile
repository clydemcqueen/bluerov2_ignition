FROM ubuntu:20.04

# Install various things, some of this is to get rid of annoying Gtk warnings
RUN apt-get update && DEBIAN_FRONTEND="noninteractive" apt-get install --no-install-recommends -y \
    bash-completion \
    build-essential \
    git \
    glmark2 \
    iputils-ping \
    libcanberra-gtk-module \
    libcanberra-gtk3-module \
    lsb-release \
    locales \
    mlocate \
    python3-dev \
    python3-lxml \
    python3-matplotlib \
    python3-opencv \
    python3-pip \
    python3-pygame \
    python3-wxgtk4.0 \
    python3-yaml \
    software-properties-common \
    sudo \
    vim \
    yaru-theme-icon

RUN locale-gen en_US en_US.UTF-8

RUN update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8

ENV LANG=en_US.UTF-8

RUN pip3 install mavproxy

# Suppress more Gtk warnings
ENV NO_AT_BRIDGE=1
