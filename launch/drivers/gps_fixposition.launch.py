from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch.substitutions import PathJoinSubstitution


def generate_launch_description():
    node_name = LaunchConfiguration('node_name')
    config = LaunchConfiguration('config')
    launcher = LaunchConfiguration('launcher')

    node_name_arg = DeclareLaunchArgument(
        'node_name',
        default_value='fixposition_driver_ros2',
        description='Node name')
    config_arg = DeclareLaunchArgument(
        'config',
        default_value='config/gps/fixposition_config.yaml',
        description='Configuration file to use')
    launcher_arg = DeclareLaunchArgument(
        'launcher',
        default_value='',
        description='Launch node via this (node launch-prefix)')

    config_file = PathJoinSubstitution([
        FindPackageShare('nissan_bringup'),
        config,
    ])

    fixposition_node = Node(
        package='fixposition_driver_ros2',
        executable='fixposition_driver_ros2_exec',
        name=node_name,
        output='screen',
        respawn=True,
        respawn_delay=5.0,
        prefix=launcher,
        arguments=['--ros-args', '--log-level', [node_name, ':=info']],
        parameters=[config_file],
    )

    return LaunchDescription([
        node_name_arg,
        config_arg,
        launcher_arg,
        fixposition_node,
    ])