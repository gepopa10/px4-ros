#!/bin/bash

ROS_SETUP="/opt/ros/humble/setup.bash"

source $ROS_SETUP

ros2 service call /launch_mission std_srvs/srv/Trigger "{}"