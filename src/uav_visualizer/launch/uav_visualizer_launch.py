import os
from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    package_dir = get_package_share_directory('uav_visualizer')
    return LaunchDescription([
        Node(
            package='uav_visualizer',
            executable='visualizer_node',
            name='visualizer_node'
        ),
        Node(
            package='rviz2',
            namespace='',
            executable='rviz2',
            name='rviz2',
            arguments=['-d', [os.path.join(package_dir, 'resource/uav_visualizer.rviz')]]
        )
    ])
