FROM osrf/ros:galactic-desktop

RUN apt-get update \
 && apt-get dist-upgrade -y \
 && apt-get install -y \
    build-essential \
    lsb-release \
    sudo \
    wget \
    vim \
 && apt-get clean

ENV IGN_WS=/home/ign_ws

# Check out Ignition source
RUN mkdir -p ${IGN_WS}/src \
 && cd ${IGN_WS}/src \
 && wget https://raw.githubusercontent.com/clydemcqueen/bluerov2_ignition/main/garden.repos \
 && vcs import < garden.repos

# Install Ignition dependencies
# This parses Ignition source tree to find package dependencies
RUN /bin/sh -c 'echo "deb http://packages.osrfoundation.org/gazebo/ubuntu-stable `lsb_release -cs` main" > /etc/apt/sources.list.d/gazebo-stable.list' \
 && /bin/sh -c 'echo "deb http://packages.osrfoundation.org/gazebo/ubuntu-nightly `lsb_release -cs` main" > /etc/apt/sources.list.d/gazebo-nightly.list' \
 && /bin/sh -c 'wget http://packages.osrfoundation.org/gazebo.key -O - | apt-key add -' \
 && apt-get update \
 && apt-get install -y \
  $(sort -u $(find . -iname 'packages-'`lsb_release -cs`'.apt' -o -iname 'packages.apt' | grep -v '/\.git/') | sed '/ignition\|sdf/d' | tr '\n' ' ') \
 && apt-get dist-upgrade -y \
 && apt-get clean

# Build Ignition
RUN [ "/bin/bash" , "-c" , \
  "cd ${IGN_WS} \
  && source /opt/ros/galactic/setup.bash \
  && colcon build --merge-install --cmake-args ' -DBUILD_TESTING=OFF' ' -DCMAKE_BUILD_TYPE=Release'" ]
