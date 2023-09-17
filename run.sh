#!/bin/bash

ROS_SETUP="/opt/ros/humble/setup.bash"
PACKAGE_SETUP="$(dirname "$0")/install/setup.bash"

# Commands to be executed
COMMAND1="MicroXRCEAgent udp4 -p 8888"
COMMAND2="source $ROS_SETUP && source $PACKAGE_SETUP && ros2 launch uav_bringup main_launch.py"
COMMAND3="cd $HOME/PX4-Autopilot && make px4_sitl none_iris"
COMMAND4="source $ROS_SETUP && source $PACKAGE_SETUP && ros2 launch uav_controller uav_controller_launch.py"
COMMAND5="source $ROS_SETUP && source $PACKAGE_SETUP && ros2 launch uav_visualizer uav_visualizer_launch.py"
COMMAND6="source $ROS_SETUP && source $PACKAGE_SETUP && ros2 run uav_teleop uav_teleop_node"

# Start a new tmux session in the background without attaching to it.
tmux new-session -d -s uav_ws 

tmux send-keys -t uav_ws "$COMMAND1" C-m 

tmux split-window -h 

tmux send-keys -t uav_ws.1 "$COMMAND2" C-m 

tmux split-window -v -p 66

tmux send-keys -t uav_ws.2 "$COMMAND3" C-m 

tmux split-window -v 

tmux send-keys -t uav_ws.3 "$COMMAND4" C-m 

tmux select-pane -t 0
tmux split-window -v -p 66

tmux send-keys -t uav_ws.1 "$COMMAND5" C-m 

tmux split-window -v

tmux send-keys -t uav_ws.2 "$COMMAND6" C-m 

# Attach to the session.
tmux attach -t uav_ws
