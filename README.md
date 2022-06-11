# BlueROV2 in Ignition Gazebo

> Status: proof-of-concept

This is a model of the BlueROV2 that runs in Ignition Gazebo.
It uses the BuoyancyPlugin, HydrodynamicsPlugin and ThrusterPlugin.

Requirements:
* Ignition Gazebo, built from source with [this patch](https://github.com/ignitionrobotics/ign-gazebo/pull/1402)
  * See [garden.repos](garden.repos) for commit hashes
  * See [Dockerfile_galactic_garden](Dockerfile_galactic_garden) for build instructions
* ardupilot_gazebo, built from source on [this branch](https://github.com/ArduPilot/ardupilot_gazebo/tree/ignition-garden)
* ArduSub
* MAVProxy

Running Ignition Gazebo:
~~~
$ . ~/ignition_ws/install/setup.bash
$ ign gazebo --version
Ignition Gazebo, version 7.0.0~pre1
$ export IGN_GAZEBO_RESOURCE_PATH=~/colcon_ws/src/bluerov2_ignition/models:~/colcon_ws/src/bluerov2_ignition/worlds
$ export IGN_GAZEBO_SYSTEM_PLUGIN_PATH=~/ardupilot_gazebo/build
$ ign gazebo -v 3 -r underwater.world
~~~

Directly send thrust commands:
~~~
$ . ~/ignition_ws/install/setup.bash
$ cd ~/colcon_ws/src/bluerov2_ignition
$ . scripts/cw.sh
$ . scripts/stop.sh
~~~

Running ArduSub:
~~~
$ cd ~/ardupilot
$ Tools/autotest/sim_vehicle.py -L RATBeach -v ArduSub --model=JSON --out=udp:0.0.0.0:14550 --console
~~~

Sending commands to ArduSub:
~~~
arm throttle
rc 3 1450     
rc 3 1500
mode alt_hold
rc 5 1550
disarm
~~~

Caveats:
* The model needs tuning
* The visuals are quite basic

References:
* https://github.com/ardupilot/ardupilot_gazebo/wiki
* https://ignitionrobotics.org/docs/garden
* https://ardupilot.org/dev/docs/building-setup-linux.html
* https://ardupilot.org/dev/docs/setting-up-sitl-on-linux.html
* https://ardupilot.org/mavproxy/docs/getting_started/download_and_installation.html
* https://www.ardusub.com/developers/rc-input-and-output.html
