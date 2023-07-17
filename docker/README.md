To build the docker image:
~~~
./build.sh
~~~

To run the BlueROV2 demo, start the container in the 1st terminal, and start ArduSub:
~~~
./run.sh
sim_vehicle.py -L RATBeach -v ArduSub --model=JSON --out=udp:0.0.0.0:14550 --no-rebuild
~~~

In the 2nd terminal start Gazebo:
~~~
docker exec -it bluerov2_ignition /bin/bash
gz sim -v 3 -r bluerov2_underwater.world
~~~
