import os
from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    
    uav_bringup_dir = get_package_share_directory('uav_bringup')
    sdf_file_path = os.path.join(uav_bringup_dir, 'models', 'iris_depth_camera', 'iris_depth_camera.sdf')

    return LaunchDescription([
        Node(
            package='gazebo_ros',
            executable='spawn_entity.py',
            arguments=['-entity', 'iris_depth_camera', '-file', sdf_file_path, '-x', '0.0', '-y', '0.0', '-z', '0.83', '-R', '0', '-P', '0', '-Y', '0'],
            output='screen',
            parameters=[{'use_sim_time': True}],
            remappings=[('/clock', 'clock')]
        )
    ])
