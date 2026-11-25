import sys
from os import path

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, LogInfo
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

sys.path.insert(0, path.dirname(path.dirname(path.abspath(__file__))))  # launch/
import nissan_tf_config
"""
orientation_source can be gps / odom  
- gps: orientation provided from the default gps modules 
- odom: orientation counted from previous positions        
z_coord_ref_switch can be zero / exact / zero_based / orig 
- zero: the Z coordinate is always 0
- exact: the Z coorindinate is always z_coord_exact_height param (must be set in this launch)
- zero_based: Z coordinate starts from 0 and relative
- orig: the original Z provided by Duro / Piksi
euler_based_orientation:
- true: euler based, not enabled by default, please enable SPB message SBP_MSG_ORIENT_EULER 0x0221 decimal 545
- false: quaternion based, not enabled by default, please enable SPB message SBP_MSG_ORIENT_QUAT 0x0220 decimal 544
"""
def generate_launch_description():
    # base_link source: config/tf/localization.yaml
    loc = nissan_tf_config.localization()
    return LaunchDescription([
        DeclareLaunchArgument(
            'publish_base_link_tf',
            default_value='true' if loc['base_link_source'] == 'duro' else 'false',
            description='Publish nissan9/gps -> nissan9/base_link (default from config/tf/localization.yaml)'),
        LogInfo(msg=f"[gps_duro] base_link_source: {loc['base_link_source']}, map_origin: {loc['map_origin']}"),
        Node(
            package="duro_gps_driver",
            executable="duro_node",
            namespace="nissan9/gps/duro",
            parameters=[
                {
                    "ip_address": "192.168.11.112",
                    "port": 55555,
                    "gps_receiver_frame_id": "nissan9/duro_gps",
                    "imu_frame_id": "nissan9/duro_gps_imu",
                    "utm_frame_id": "map",
                    "orientation_source": "gps",
                    "z_coord_ref_switch": "orig",
                    "z_coord_exact_height": 1.7,
                    "tf_frame_id": "map",
                    "tf_child_frame_id": "nissan9/gps",
                    "zero_based_pose": False,
                    "euler_based_orientation": True,
                }
            ],
        ),
        # Antenna (nissan9/gps, from the Duro TF) -> rear axle center (nissan9/base_link)
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='base_gps_tf_publisher',
            output='screen',
            condition=IfCondition(LaunchConfiguration('publish_base_link_tf')),
            arguments=[
                '--x',      '0.196',
                '--y',      '0.0',
                '--z',      '-1.1',
                '--yaw',    '0',
                '--pitch',  '0',
                '--roll',   '0',
                '--frame-id',       'nissan9/gps',
                '--child-frame-id', 'nissan9/base_link'],
        ),
    ])
