# Sends to cmd_thrust
gz topic -t /model/bluerov2/joint/thruster1_joint/cmd_thrust -m gz.msgs.Double -p 'data: -5'
gz topic -t /model/bluerov2/joint/thruster2_joint/cmd_thrust -m gz.msgs.Double -p 'data: -5'
gz topic -t /model/bluerov2/joint/thruster3_joint/cmd_thrust -m gz.msgs.Double -p 'data: 5'
gz topic -t /model/bluerov2/joint/thruster4_joint/cmd_thrust -m gz.msgs.Double -p 'data: 5'
