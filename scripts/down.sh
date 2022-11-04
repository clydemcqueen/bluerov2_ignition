# Sends to cmd_thrust
gz topic -t /model/bluerov2/joint/thruster5_joint/cmd_thrust -m gz.msgs.Double -p 'data: 5'
gz topic -t /model/bluerov2/joint/thruster6_joint/cmd_thrust -m gz.msgs.Double -p 'data: 5'
