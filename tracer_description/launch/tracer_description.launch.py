'''  
=========================================
    * Author: nipun.dhananjaya@gmail.com
    * Created: 04.2023
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
    this_pkg = get_package_share_directory('tracer_description')
    # ---------  xacro process ------------------------------------------
    xacro_file = os.path.join(this_pkg, 'urdf', 'tracer.urdf.xacro')
    doc = xacro.parse(open(xacro_file))
    xacro.process_doc(doc)
    params = {'robot_description': doc.toxml(), 'use_sim_time':True}
    # -------------------------------------------------------------------

    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[params])
    
    return LaunchDescription([
        robot_state_publisher_node
    ])