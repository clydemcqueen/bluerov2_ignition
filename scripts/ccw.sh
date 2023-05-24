# Sends to cmd_thrust

if [ $# -eq 0 ]; then
    echo "Usage: $0 <model_name>"
    exit 1
fi

gz topic -t /model/$1/joint/thruster1_joint/cmd_thrust -m gz.msgs.Double -p 'data: -5'
gz topic -t /model/$1/joint/thruster2_joint/cmd_thrust -m gz.msgs.Double -p 'data: 5'
gz topic -t /model/$1/joint/thruster3_joint/cmd_thrust -m gz.msgs.Double -p 'data: 5'
gz topic -t /model/$1/joint/thruster4_joint/cmd_thrust -m gz.msgs.Double -p 'data: -5'
