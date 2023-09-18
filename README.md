# px4-ros

This repository holds a PX4 simulation demo with gazebo-classic and ROS2 Humble. Manual control and waypoints functionalities are demonstrated.

*Everything is containerized, for quick setup and test*

[Screenshot](./media/demo.png)

## Quickstart

### Prerequisites
- Install docker

### Run
Manual Control Demo:
- Launch the simulation with `run_container.sh` this will build the image and run the container
- Arm the uav with space and the control manual with keyboard
Mission Demo:
1. Enter the running container with `sudo docker exec -it my_ros_container bash`
2. `./launch_mission.sh`

## How it works

### uav_bringup

This package is reponsible of launching gazebo with a world file and spawning the iris quadcopter model with a depth camera.

### uav_teleop

This node publish commands from the keyboard to the topic `/offboard_velocity_cmd`. For example, when you press `UP` a constant twist velocity on the x axis will be published. Also, you can arm the drone with `SPACE`. This sends a bool over the topic `/arm_message`. These messages are processed by another package, the `uav_controller`.

### uav_controller

This package holds the controller node.

It is reponsible for managing the state machine of the px4 by publishing to
- `/fmu/in/offboard_control_mode`

It subscribes to :
- `/fmu/in/offboard_control_mode`
- `/fmu/out/vehicle_odometry` for uav position
- `/fmu/out/vehicle_attitude` for uav attitude
- `/fmu/out/vehicle_status` for uav status
- `/arm_message` to know when to arm from the uav_teleop
- `/offboard_velocity_cmd` to know the commanded velocity from the uav_teleop

It publishes to:
- `/fmu/in/offboard_control_mode` to send to px4 the type of offboard control mode
- `/fmu/in/trajectory_setpoint` to send the velocity commands for manual control but also for position setpoint for a mission
- `/fmu/in/vehicle_command` to send the command type to px4 controller

This has a command loop that runs at 50hz and listens for manual control commands to be sent to px4.

Also, it has a service `launch_mission` that listen if a client want to launch a mission. It is currently hardcoded to stop manual control when a client wants to launch a mission and make the drone follow a 4 waypoints trajectory. When the trajectory is completed (all waypoints reached within a distance threshold) then manual control is available again. The trajectory is simply a offboard command type position and we publish continously to `/fmu/in/trajectory_setpoint` until the position is reached. 

### uav_visualizer

This package holds the visualizer node that is reponsible to publish markers and visualization artifacts to topics rendered by rviz. It also publishes some transform so the depth camera points are well represented in rviz.

It subscribes to :
- `/fmu/in/trajectory_setpoint` to visualize the desired trajectory
- `/fmu/out/vehicle_odometry` for uav position representation
- `/fmu/out/vehicle_attitude` for uav attitude
- `/odom` to compute the transform from world to iris base link. This topic us published by gazebo. It is considered as the ground truth for odometry and more precise that what the px4 controller computes.

It publishes to : 
- `/uav_visualizer/vehicle_pose` a marker for live pose of the uav
- `/uav_visualizer/vehicle_path` a history of the path followed by the uav from the px4 odometry
- `/uav_visualizer/setpoint_path` the desired trajectory given by `/fmu/in/trajectory_setpoint`
