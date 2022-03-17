# Sends to cmd_thrust
ign topic -t /model/bluerov2/joint/thruster1_joint/cmd_thrust -m ignition.msgs.Double -p 'data: 5'
ign topic -t /model/bluerov2/joint/thruster2_joint/cmd_thrust -m ignition.msgs.Double -p 'data: 5'
ign topic -t /model/bluerov2/joint/thruster3_joint/cmd_thrust -m ignition.msgs.Double -p 'data: -5'
ign topic -t /model/bluerov2/joint/thruster4_joint/cmd_thrust -m ignition.msgs.Double -p 'data: -5'
