from os import path

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    pkg_share = get_package_share_directory('nissan_bringup')
    urdf_file = path.join(pkg_share, 'param', 'nissan_leaf_robotdescription.ref.xml')
    rviz_file = path.join(pkg_share, 'config', 'rviz', 'nissan_3d.rviz')

    with open(urdf_file, 'r') as f:
        robot_description = f.read()

    return LaunchDescription([
        DeclareLaunchArgument('rviz', default_value='true',
                              description='Start RViz with the Nissan model'),

        # Publishes /robot_description (transient local) for the RViz RobotModel display.
        # The model is attached to the nissan9/base_link frame.
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='nissan_state_publisher',
            output='screen',
            parameters=[{'robot_description': robot_description}],
        ),
        # Node(
        #     package='rviz2',
        #     executable='rviz2',
        #     name='rviz2',
        #     arguments=['-d', rviz_file],
        #     condition=IfCondition(LaunchConfiguration('rviz')),
        # ),
    ])
