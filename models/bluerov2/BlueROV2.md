# BlueROV2

A Gazebo model of the BlueROV2.

![BlueROV2 Gazebo](/images/bluerov2.png)

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
gz sim -v 3 -r bluerov2_underwater.world
~~~

### Run ArduPilot SITL

~~~bash
Tools/autotest/sim_vehicle.py -L RATBeach -v ArduSub --model=JSON --out=udp:0.0.0.0:14550 --console
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

### Notes

The BlueROV2 model has not been tuned.

## Credits

All meshes have been obtained from [Blue Robotics](https://bluerobotics.com/) at the
following sources:

- [BlueROV2 Mesh](https://grabcad.com/library/bluerov2-1)
- [T200 Propeller Mesh](https://grabcad.com/library/bluerobotics-t200-thruster-1)