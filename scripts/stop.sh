# Sends to cmd_thrust, not cmd_vel
gz topic -t /model/bluerov2/joint/thruster1_joint/cmd_thrust -m gz.msgs.Double -p 'data: 0'
gz topic -t /model/bluerov2/joint/thruster2_joint/cmd_thrust -m gz.msgs.Double -p 'data: 0'
gz topic -t /model/bluerov2/joint/thruster3_joint/cmd_thrust -m gz.msgs.Double -p 'data: 0'
gz topic -t /model/bluerov2/joint/thruster4_joint/cmd_thrust -m gz.msgs.Double -p 'data: 0'
gz topic -t /model/bluerov2/joint/thruster5_joint/cmd_thrust -m gz.msgs.Double -p 'data: 0'
gz topic -t /model/bluerov2/joint/thruster6_joint/cmd_thrust -m gz.msgs.Double -p 'data: 0'
