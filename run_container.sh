#!/bin/bash

xhost +local:docker

sudo docker build -t my_ros_image .

sudo docker run --rm -it -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix --privileged --name my_ros_container my_ros_image