from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch.substitutions import PathJoinSubstitution

def generate_launch_description():

    return LaunchDescription([
        DeclareLaunchArgument('namespace', default_value='nissan9'),
        
        # params
        Node(
            package='nissan_bringup',
            executable='global_parameter',
            name='car_parameters',
            parameters=[
                {
                    'car_name': 'leaf',

                    PathJoinSubstitution([LaunchConfiguration('namespace'), 'car_width']): '1.77',                       # A jármű teljes szélessége [m]
                    PathJoinSubstitution([LaunchConfiguration('namespace'), 'car_length']): '4.535',                     # A jármű teljes hosszúsága [m]
                    PathJoinSubstitution([LaunchConfiguration('namespace'), 'wheelbase']): '2.7',                        # A jármű tengelytávja [m]
                    PathJoinSubstitution([LaunchConfiguration('namespace'), 'rear_axle_car_front_distance']): '3.707',   # A jármű hátsó tengelye és a kocsi eleje közötti távolság [m]
                    PathJoinSubstitution([LaunchConfiguration('namespace'), 'max_wheel_angle']): '31.0',                 # Maximális kormányszög [deg]
                    PathJoinSubstitution([LaunchConfiguration('namespace'), 'min_wheel_angle']): '-31.0',                # Minimális kormányszög [deg]
                    PathJoinSubstitution([LaunchConfiguration('namespace'), 'max_acceleration']): '3.0',                # Maximális gyorsulás [m/s^2]
                    PathJoinSubstitution([LaunchConfiguration('namespace'), 'max_deceleration']): '6.0',                # Maximális lassulás [m/s^2]

                    # A base_link és a laser frame paraméterei, az irányok a base_link-ről mutatnak a laser frame-re
                    PathJoinSubstitution([LaunchConfiguration('namespace'), 'base_link_laser_trans_x']): '3.707',
                    PathJoinSubstitution([LaunchConfiguration('namespace'), 'base_link_laser_trans_y']): '-0.351',
                    PathJoinSubstitution([LaunchConfiguration('namespace'), 'base_link_laser_trans_z']): '0.113',
                    PathJoinSubstitution([LaunchConfiguration('namespace'), 'base_link_laser_rot_x']): '0.0',
                    PathJoinSubstitution([LaunchConfiguration('namespace'), 'base_link_laser_rot_y']): '0.0',
                    PathJoinSubstitution([LaunchConfiguration('namespace'), 'base_link_laser_rot_z']): '0.0',
                }
            ],
        ),
    ])
