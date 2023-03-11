'''  
=========================================
    * Author: nipun.dhananjaya@gmail.com
    * Created: 04.02.2023
=========================================
'''

import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess, IncludeLaunchDescription
from launch.actions import RegisterEventHandler
from launch.event_handlers import OnProcessExit
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
import xacro



def generate_launch_description():
    pkg_ros_ign_gazebo = get_package_share_directory('ros_ign_gazebo')
    pkg_tracer_ign = get_package_share_directory('tracer_ign_sim')

    # --------- xacro process -------------------------------------------------------------------------
    xacro_file = os.path.join(get_package_share_directory('tracer_ign_sim'), 'urdfs/tracer.urdf.xacro')
    doc = xacro.parse(open(xacro_file))
    xacro.process_doc(doc)
    params = {'robot_description': doc.toxml(), 'use_sim_time':True}
    # -------------------------------------------------------------------------------------------------

    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[params])

    ign_spawn_entity = Node(
        package='ros_ign_gazebo',
        executable='create',
        output='screen',
        arguments=['-string', doc.toxml(), '-name', 'tracer',
                   '-x', '0',
                   '-y', '0',
                   '-z', '0.2'])

    load_joint_state_controller = ExecuteProcess(
        cmd=['ros2', 'control', 'load_controller', '--set-state', 'start', 'joint_state_broadcaster'],
        output='screen'
    )

    load_joint_trajectory_controller = ExecuteProcess(
        cmd=['ros2', 'control', 'load_controller', '--set-state', 'start', 'tracer_controller'],
        output='screen'
    )
    # publish time
    clock_bridge = Node(
        package='ros_ign_bridge',
        executable='parameter_bridge',
        arguments=['/clock@rosgraph_msgs/msg/Clock[ignition.msgs.Clock'],
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

        RegisterEventHandler(
            event_handler=OnProcessExit(
                target_action=ign_spawn_entity,
                on_exit=[load_joint_state_controller],
            )
        ),

        RegisterEventHandler(
            event_handler=OnProcessExit(
                target_action=load_joint_state_controller,
                on_exit=[load_joint_trajectory_controller],
            )
        ),
        clock_bridge,
        node_robot_state_publisher,
        ign_spawn_entity,
        # Launch arguments
        DeclareLaunchArgument(
            'use_sim_time',
            default_value=use_sim_time,
            description='If true, use simulated clock'),

        ])
