# BlueROV2 Heavy

A Gazebo model of the BlueROV2 Heavy configuration.

![BlueROV2 Heavy Gazebo](/images/bluerov2_heavy.png)

## Usage

Gazebo and all other requirements documented in the project [README](/README.md) should
be installed.

Update the `GZ_SIM_RESOURCE_PATH` to include the BlueROV2 models:

~~~bash
export GZ_SIM_RESOURCE_PATH=$GZ_SIM_RESOURCE_PATH:\
~/colcon_ws/src/bluerov2_ignition/models:\
~/colcon_ws/src/bluerov2_ignition/worlds
~~~

### Start Gazebo

~~~bash
gz sim -v 3 -r bluerov2_heavy_underwater.world
~~~

### Run ArduPilot SITL

~~~bash
Tools/autotest/sim_vehicle.py -L RATBeach -v ArduSub -f vectored_6dof --model=JSON --out=udp:0.0.0.0:14550 --console
~~~

### Send commands to the ROV

~~~
arm throttle
rc 3 1450     
rc 3 1500
mode alt_hold
rc 5 1550
disarm
~~~

## Credits

All meshes have been obtained from [Blue Robotics](https://bluerobotics.com/) at the
following sources:

- [BlueROV2 Mesh](https://grabcad.com/library/bluerov2-1)
- [T200 Propeller Mesh](https://grabcad.com/library/bluerobotics-t200-thruster-1)

The hydrodynamic parameters used for the model have been obtained from the following
source:

- [An Open-Source Benchmark Simulator: Control of a BlueROV2 Underwater Robot](https://github.com/ROV-Simulator/ROV-Simulator)