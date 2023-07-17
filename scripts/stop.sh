# Sends to cmd_thrust, not cmd_vel

if [ $# -eq 0 ]; then
    echo "Usage: $0 <model_name>"
    exit 1
fi

gz topic -t /model/$1/joint/thruster1_joint/cmd_thrust -m gz.msgs.Double -p 'data: 0'
gz topic -t /model/$1/joint/thruster2_joint/cmd_thrust -m gz.msgs.Double -p 'data: 0'
gz topic -t /model/$1/joint/thruster3_joint/cmd_thrust -m gz.msgs.Double -p 'data: 0'
gz topic -t /model/$1/joint/thruster4_joint/cmd_thrust -m gz.msgs.Double -p 'data: 0'
gz topic -t /model/$1/joint/thruster5_joint/cmd_thrust -m gz.msgs.Double -p 'data: 0'
gz topic -t /model/$1/joint/thruster6_joint/cmd_thrust -m gz.msgs.Double -p 'data: 0'

if [ "$1" = "bluerov2_heavy" ]; then
   gz topic -t /model/$1/joint/thruster7_joint/cmd_thrust -m gz.msgs.Double -p 'data: 0'
   gz topic -t /model/$1/joint/thruster8_joint/cmd_thrust -m gz.msgs.Double -p 'data: 0'
fi
