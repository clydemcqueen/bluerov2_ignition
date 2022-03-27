# Sends to cmd_thrust
ign topic -t /model/bluerov2/joint/thruster5_joint/cmd_thrust -m ignition.msgs.Double -p 'data: 5'
ign topic -t /model/bluerov2/joint/thruster6_joint/cmd_thrust -m ignition.msgs.Double -p 'data: 5'
