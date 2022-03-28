#!/usr/bin/env python3

"""
Generate the model.sdf file by substituting strings of the form "@foo" with calculated values

There are 2 control methods: /cmd_thrust and /cmd_vel. See the comments in ArduPilotPlugin.cc for details.
"""

import re
import sys

mass = 10
visual_x = 0.457
visual_y = 0.338
visual_z = 0.25
fluid_density = 1000
dome_x = visual_x / 2

# The ROV should be positively buoyant
buoyancy_adjustment = 0.05
displaced_mass = mass + buoyancy_adjustment

# The collision box is used by the BuoyancyPlugin
# collision_x * collision_y * collision_z * density == displaced_mass
collision_x = visual_x
collision_y = visual_y
collision_z = displaced_mass / (visual_x * visual_y * fluid_density)

# The center of mass is just above the origin
mass_z = 0.011

# The center of volume is directly above the center of mass, resulting in a restoring force
volume_z = 0.06

ixx = mass / 12 * (collision_y * collision_y + collision_z * collision_z)
iyy = mass / 12 * (collision_x * collision_x + collision_z * collision_z)
izz = mass / 12 * (collision_x * collision_x + collision_y * collision_y)

# 2nd order stability for the HydrodynamicsPlugin
xUU = -0.5 * visual_y * visual_z * 0.8 * fluid_density
yVV = -0.5 * visual_x * visual_z * 0.95 * fluid_density
zWW = -0.5 * visual_x * visual_y * 0.95 * fluid_density
kPP = -0.5 * 0.004 * fluid_density
mQQ = -0.5 * 0.004 * fluid_density
nRR = -0.5 * 0.004 * fluid_density

# Thruster placement
thruster_x = 0.15
thruster_y = 0.09
thruster_z = -0.009
vert_thruster_y = 0.105
vert_thruster_z = 0.09

# Propeller link parameters
propeller_size = "0.1 0.02 0.01"
propeller_mass = 0.002
propeller_ixx = 0.001
propeller_iyy = 0.001
propeller_izz = 0.001

# ThrusterPlugin parameters
propeller_diameter = 0.1
thrust_coefficient = 0.02
use_angvel_cmd = True

# ArduPilotPlugin control parameters
servo_min = 1100
servo_max = 1900
control_offset = -0.5
control_multiplier = 0

# Thruster topics, the final bit will be added by update_globals()
thruster1_topic = "/model/bluerov2/joint/thruster1_joint/cmd_"
thruster2_topic = "/model/bluerov2/joint/thruster2_joint/cmd_"
thruster3_topic = "/model/bluerov2/joint/thruster3_joint/cmd_"
thruster4_topic = "/model/bluerov2/joint/thruster4_joint/cmd_"
thruster5_topic = "/model/bluerov2/joint/thruster5_joint/cmd_"
thruster6_topic = "/model/bluerov2/joint/thruster6_joint/cmd_"


# Use one of the 2 control methods: thrust (force = true) or velocity (force = false)
# TODO(clyde) thrusters 3, 4 and 6 are spinning the wrong way when force == false
def update_globals(force):
    global use_angvel_cmd
    global control_multiplier
    global thruster1_topic
    global thruster2_topic
    global thruster3_topic
    global thruster4_topic
    global thruster5_topic
    global thruster6_topic

    if force:
        print("control method = thrust force")
        use_angvel_cmd = False
        thruster1_topic += "thrust"
        thruster2_topic += "thrust"
        thruster3_topic += "thrust"
        thruster4_topic += "thrust"
        thruster5_topic += "thrust"
        thruster6_topic += "thrust"

        # Force range [-50, 50]
        control_multiplier = 100
    else:
        print("control method = angular velocity")
        use_angvel_cmd = True
        thruster1_topic += "vel"
        thruster2_topic += "vel"
        thruster3_topic += "vel"
        thruster4_topic += "vel"
        thruster5_topic += "vel"
        thruster6_topic += "vel"

        # Velocity range TODO
        control_multiplier = 100  # TODO


def generate_model(input_path, output_path):
    s = open(input_path, "r").read()
    pattern = re.compile(r"@(\w+)")
    # globals()['foo'] will return the value of foo
    # TODO(clyde) trim floats
    s = re.sub(pattern, lambda m: str(globals()[m.group(1)]), s)
    open(output_path, "w").write(s)


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage:")
        print("generate_model.py infile outfile 0|1")
        print("0: use angular velocity")
        print("1: use thrust force")
        exit(-100)

    # A bit picky, but works
    update_globals(bool(int(sys.argv[3])))

    generate_model(sys.argv[1], sys.argv[2])
