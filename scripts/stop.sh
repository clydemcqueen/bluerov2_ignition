# Sends to cmd_thrust, not cmd_vel
ign topic -t /model/bluerov2/joint/thruster1_joint/cmd_thrust -m ignition.msgs.Double -p 'data: 0'
ign topic -t /model/bluerov2/joint/thruster2_joint/cmd_thrust -m ignition.msgs.Double -p 'data: 0'
ign topic -t /model/bluerov2/joint/thruster3_joint/cmd_thrust -m ignition.msgs.Double -p 'data: 0'
ign topic -t /model/bluerov2/joint/thruster4_joint/cmd_thrust -m ignition.msgs.Double -p 'data: 0'
ign topic -t /model/bluerov2/joint/thruster5_joint/cmd_thrust -m ignition.msgs.Double -p 'data: 0'
ign topic -t /model/bluerov2/joint/thruster6_joint/cmd_thrust -m ignition.msgs.Double -p 'data: 0'
