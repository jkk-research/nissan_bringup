from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    # Low-poly alternative of 3d_nissan.launch.py: the car is drawn from
    # primitive markers (visualization_msgs/MarkerArray) instead of a mesh.
    return LaunchDescription([
        DeclareLaunchArgument('frame_id', default_value='nissan9/base_link'),
        DeclareLaunchArgument('topic', default_value='nissan_marker'),
        DeclareLaunchArgument('publish_rate', default_value='1.0'),

        Node(
            package='nissan_bringup',
            executable='nissan_marker_publisher',
            name='nissan_marker_publisher',
            output='screen',
            parameters=[{
                'frame_id': LaunchConfiguration('frame_id'),
                'topic': LaunchConfiguration('topic'),
                'publish_rate': LaunchConfiguration('publish_rate'),
            }],
        ),
    ])
