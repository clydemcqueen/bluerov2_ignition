# BlueROV2 in Ignition Gazebo

> Proof-of-concept, YMMV

This is a model of the BlueROV2 that runs in Ignition Gazebo.
It uses the BuoyancyPlugin, HydrodynamicsPlugin and ThrusterPlugin.

Requirements:
* Gazebo Ignition, built from source with [this patch](https://github.com/ignitionrobotics/ign-gazebo/pull/1402)
* [This fork of ardupilot_gazebo](https://github.com/clydemcqueen/ardupilot_gazebo/tree/ignition-garden)
* ArduSub
* MAVProxy

Running Ignition Gazebo:
~~~
$ . ~/projects/ignition_ws/install/setup.bash
$ ign gazebo --version
Ignition Gazebo, version 7.0.0~pre1
$ export IGN_GAZEBO_RESOURCE_PATH=~/projects/bluerov2_ignition/models:~/projects/bluerov2_ignition/worlds
$ export IGN_GAZEBO_SYSTEM_PLUGIN_PATH=~/projects/ardupilot_gazebo/build
$ ign gazebo -v 3 -r underwater.world
~~~

Directly send thrust commands:
~~~
$ . ~/projects/ignition_ws/install/setup.bash
$ cd ~/projects/bluerov2_ignition
$ . scripts/cw.bash
$ . scripts/stop.bash
~~~

Running ArduSub:
~~~
$ cd ~/projects/ardupilot
$ Tools/autotest/sim_vehicle.py -L RATBeach -v ArduSub --model=JSON --out=udp:0.0.0.0:14550 --console
~~~

Sending commands to ArduSub:
~~~
arm throttle
rc 5 1450
mode 2
disarm
~~~

Caveats:
* The model needs a lot of tuning
* The visuals are quite basic
* There are probably bugs

References:
* https://github.com/ardupilot/ardupilot_gazebo/wiki
* https://ignitionrobotics.org/docs/garden
* https://ardupilot.org/dev/docs/building-setup-linux.html
* https://ardupilot.org/dev/docs/setting-up-sitl-on-linux.html
* https://ardupilot.org/mavproxy/docs/getting_started/download_and_installation.html
* https://www.ardusub.com/developers/rc-input-and-output.html
