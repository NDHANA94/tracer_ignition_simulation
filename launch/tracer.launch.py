'''  
=========================================
    * Author: nipun.dhananjaya@gmail.com
    * Created: 04.02.2023
=========================================
'''
"""
Command for testing: 
    keyboard: ros2 run teleop_twist_keyboard teleop_twist_keyboard -_-ros-args -r /cmd_vel:=/model/tracer/cmd_vel
    terminal cmd: ign topic -t "/model/tracer/cmd_vel" -m ignition.msgs.Twist -p "linear: {x: 0.5}, angular: {z: 0.05}
    
 
  * Listen to odometry:
      - ign topic -e -t /model/tracer/odometry
"""
import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess, IncludeLaunchDescription
from launch.actions import RegisterEventHandler
from launch.event_handlers import OnProcessExit
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node




def generate_launch_description():
    pkg_ros_ign_gazebo = get_package_share_directory('ros_ign_gazebo')
    pkg_tracer_ign = get_package_share_directory('tracer_ign_sim')

    # Launch argument
    use_sim_time = LaunchConfiguration('use_sim_time', default=True)

    ign_spawn_entity = Node(
        package='ros_ign_gazebo',
        executable='create',
        output='screen',
        arguments=['-name', 'tracer',
                   '-x', '0',
                   '-y', '0',
                   '-z', '0.2',
                   '-file', os.path.join(pkg_tracer_ign, 'models', 'tracer', 'model.sdf')],
    )

    
    # #  Bridge
    bridge = Node(
        package='ros_ign_bridge',
        executable='parameter_bridge',
        arguments=['/model/tracer/cmd_vel@geometry_msgs/msg/Twist]ignition.msgs.Twist'],
        output='screen'
    )

    # use time
    use_sim_time = LaunchConfiguration('use_sim_time', default=True)

    return LaunchDescription([
        # launch ignition gazebo
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                [os.path.join(pkg_ros_ign_gazebo, 'launch', 'ign_gazebo.launch.py')]),
            launch_arguments=[('ign_args', ' -r -v 4 empty.sdf')]
        ),

        ign_spawn_entity,
        bridge,
        # Launch arguments
        DeclareLaunchArgument(
            'use_sim_time',
            default_value=use_sim_time,
            description='If true, use simulated clock'),

        ])
