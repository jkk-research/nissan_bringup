from launch import LaunchDescription
from launch_ros.actions import Node
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
    return LaunchDescription([
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
                    "z_coord_ref_switch": "exact",
                    "z_coord_exact_height": 1.7,
                    "tf_frame_id": "map",
                    "tf_child_frame_id": "nissan9/gps",
                    "zero_based_pose": False,
                    "euler_based_orientation": True,
                }
            ],
        ),
    ])