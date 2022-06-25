FROM clydemcqueen/galactic_garden:latest
WORKDIR /home

ARG IGN_WS=/home/ign_ws
ENV APG_WS=/home/ardupilot_gazebo
ENV COLCON_WS=/home/colcon_ws

RUN apt-get update \
 && apt-get dist-upgrade -y \
 && DEBIAN_FRONTEND="noninteractive" apt-get install -y \
    bash-completion \
    keyboard-configuration \
    python3-dev \
    python3-opencv \
    python3-wxgtk4.0 \
    python3-pip \
    python3-matplotlib \
    python3-lxml \
    python3-pygame \
    rapidjson-dev \
    software-properties-common \
 && apt-get clean

# Some handy tools
RUN apt-get update \
 && apt-get dist-upgrade -y \
 && DEBIAN_FRONTEND="noninteractive" apt-get install -y \
    git \
    glmark2 \
    iputils-ping \
    mlocate \
    vim

# Build ardupilot_gazebo
RUN git clone https://github.com/ArduPilot/ardupilot_gazebo.git -b ignition-garden

RUN [ "/bin/bash" , "-c" , " \
  cd ${APG_WS} \
  && mkdir build \
  && cd build \
  && source ${IGN_WS}/install/setup.bash \
  && cmake .. -DCMAKE_BUILD_TYPE=RelWithDebInfo \
  && make -j4" ]

# Add ardupilot_gazebo to the Gazebo plugin path
ENV IGN_GAZEBO_SYSTEM_PLUGIN_PATH="/home/ardupilot_gazebo/build:${IGN_GAZEBO_SYSTEM_PLUGIN_PATH}"

RUN mkdir -p ${COLCON_WS}/src
COPY . ${COLCON_WS}/src/bluerov2_ignition

RUN [ "/bin/bash" , "-c" , " \
  cd ${COLCON_WS} \
  && source ${IGN_WS}/install/setup.bash \
  && source /opt/ros/galactic/setup.bash \
  && colcon build" ]

# ArduPilotPlugin fdm_port_in
EXPOSE 9002/udp
