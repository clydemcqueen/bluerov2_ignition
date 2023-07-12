# Sends to cmd_thrust

if [ $# -eq 0 ] || [ $# -eq 1 ]; then
    echo "Usage: $0 <model_name> <frame>"
    exit 1
fi

if [ "$2" = "vectored" ]; then
   gz topic -t /model/$1/joint/thruster5_joint/cmd_thrust -m gz.msgs.Double -p 'data: -5'
   gz topic -t /model/$1/joint/thruster6_joint/cmd_thrust -m gz.msgs.Double -p 'data: -5'
   
elif [ "$2" = "vectored_6dof" ]; then
   gz topic -t /model/$1/joint/thruster5_joint/cmd_thrust -m gz.msgs.Double -p 'data: -5'
   gz topic -t /model/$1/joint/thruster6_joint/cmd_thrust -m gz.msgs.Double -p 'data: -5'
   gz topic -t /model/$1/joint/thruster7_joint/cmd_thrust -m gz.msgs.Double -p 'data: -5'
   gz topic -t /model/$1/joint/thruster8_joint/cmd_thrust -m gz.msgs.Double -p 'data: -5'
   
else
   echo "Usage: $0 <model_name> <frame>"
   exit 1
   
fi
