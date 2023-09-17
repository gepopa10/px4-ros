import os
from launch import LaunchDescription
from launch.actions import ExecuteProcess
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():  
    uav_bringup_dir = get_package_share_directory('uav_bringup')
    models_dir_path = os.path.join(uav_bringup_dir, 'models')
    px4_dir = os.path.expanduser("~") + '/PX4-Autopilot/'
    px4_build_dir = px4_dir + 'build/px4_sitl_default/'
    plugin_path = px4_build_dir + '/build_gazebo-classic/'
    current_env = os.environ.copy()
    current_env['LD_LIBRARY_PATH'] += ':' + plugin_path

    return LaunchDescription([
        ExecuteProcess(
            cmd=['gazebo', '--verbose', '-s', 'libgazebo_ros_factory.so', '-s', 'libgazebo_ros_init.so', os.path.join(get_package_share_directory('uav_bringup'), 'worlds/cylinder.world')],
            output='screen',
            additional_env={'GAZEBO_MODEL_PATH': models_dir_path, 'GAZEBO_PLUGIN_PATH': plugin_path, 'LD_LIBRARY_PATH': current_env['LD_LIBRARY_PATH']}
        )
    ])