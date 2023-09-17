
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='uav_controller',
            executable='controller_node',
            name='controller_node'
        ),
    ])
