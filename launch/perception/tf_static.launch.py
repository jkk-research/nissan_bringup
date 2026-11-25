from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory

import sys
from os import path
sys.path.insert(0, path.dirname(path.dirname(path.abspath(__file__))))  # launch/
import nissan_tf_config

def generate_launch_description():

    # map -> map_gyor_0, map_zala_0, ... from config/tf/map_origins.yaml
    map_origin_tfs = [
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name=f'{name}_tf_publisher',
            output='screen',
            arguments=[
                '--x',  str(float(o['x'])),
                '--y',  str(float(o['y'])),
                '--z',  str(float(o.get('z', 0.0))),
                '--qx', '0',
                '--qy', '0',
                '--qz', '0',
                '--qw', '1',

                '--frame-id',       'map',
                '--child-frame-id', name],
        )
        for name, o in nissan_tf_config.map_origins().items()
    ]

    return LaunchDescription(map_origin_tfs + [
        # nissan9/gps -> nissan9/base_link is published by gps_duro.launch.py,
        # because it is only valid when the Duro provides the vehicle pose
        # (the Novatel publishes map -> nissan9/base_link directly).
        # Duro antenna: same position as nissan9/gps (inverse of gps -> base_link)
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='duro_gps_tf_publisher',
            output='screen',
            arguments=[
                '--x',      '-0.196',
                '--y',      '0.0',
                '--z',      '1.1',
                '--yaw',    '0.0261799',
                '--pitch',  '0.0',
                '--roll',   '0.0',

                '--frame-id',       'nissan9/base_link', 
                '--child-frame-id', 'nissan9/duro_gps'],
        ),
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='duro_gps_imu_tf_publisher',
            output='screen',
            arguments=[
                '--x',      '-0.196',
                '--y',      '0.0',
                '--z',      '1.1',
                '--yaw',    '0.0261799',
                '--pitch',  '0.0',
                '--roll',   '0.0',

                '--frame-id',       'nissan9/base_link', 
                '--child-frame-id', 'nissan9/duro_gps_imu'],
        ),
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='zed2_camera_center_tf_publisher',
            output='screen',
            arguments=[
                '--x',      '1.874',
                '--y',      '0.0',
                '--z',      '1.286',
                '--yaw',    '0.0',
                '--pitch',  '0.0',
                '--roll',   '0.0',

                '--frame-id',       'nissan9/base_link',
                '--child-frame-id', 'nissan9/zed2_camera_link'],
        ),
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='base_link_ground_link_publisher',
            output='screen',
            arguments=[
                '--x',      '0.0',
                '--y',      '0.0',
                '--z',      '-0.316',
                '--yaw',    '0.0',
                '--pitch',  '0.0',
                '--roll',   '0.0',

                '--frame-id',       'nissan9/base_link',
                '--child-frame-id', 'nissan9/ground_link'],
        ),
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='os_left_tf_publisher',
            output='screen',
            arguments=[
                '--x',      '1.769',
                '--y',      '0.58',
                '--z',      '1.278',
                '--yaw',    '0.0',
                '--pitch',  '0.0',
                '--roll',   '0.0',

                '--frame-id',       'nissan9/base_link',
                '--child-frame-id', 'nissan9/os_left'],
        ),
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='os_right_tf_publisher',
            output='screen',
            arguments=[
                '--x',      '1.769',
                '--y',      '-0.58',
                '--z',      '1.278',
                '--yaw',    '0.0',
                '--pitch',  '0.0',
                '--roll',   '0.0',

                '--frame-id',       'nissan9/base_link',
                '--child-frame-id', 'nissan9/os_right'],
        ),
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='os_sensor_lidar_left',
            output='screen',
            arguments=[
                '--x',      '0.0',
                '--y',      '0.0',
                '--z',      '0.0',
                '--yaw',    '0.0',
                '--pitch',  '0.0',
                '--roll',   '0.0',

                '--frame-id',       'nissan9/os_left',
                '--child-frame-id', 'nissan9/os_left_data_frame'],
        ),
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='os_sensor_imu_left',
            output='screen',
            arguments=[
                '--x',      '0.0',
                '--y',      '0.0',
                '--z',      '0.0',
                '--yaw',    '0.0',
                '--pitch',  '0.0',
                '--roll',   '0.0',

                '--frame-id',       'nissan9/os_left',
                '--child-frame-id', 'nissan9/os_left_imu_data_frame'],
        ),
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='os_sensor_lidar_right',
            output='screen',
            arguments=[
                '--x',      '0.0',
                '--y',      '0.0',
                '--z',      '0.0',
                '--yaw',    '0.0',
                '--pitch',  '0.0',
                '--roll',   '0.0',

                '--frame-id',       'nissan9/os_right',
                '--child-frame-id', 'nissan9/os_right_data_frame'],
        ),
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='os_sensor_imu_right',
            output='screen',
            arguments=[ 
                '--x',      '0.0',
                '--y',      '0.0',
                '--z',      '0.0',
                '--yaw',    '0.0',
                '--pitch',  '0.0',
                '--roll',   '0.0',

                '--frame-id',       'nissan9/os_right',
                '--child-frame-id', 'nissan9/os_right_imu_data_frame'],
        ),
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='sick_tf_publisher',
            output='screen',
            arguments=[
                '--x',      '3.707',
                '--y',      '-0.351',
                '--z',      '0.113',
                '--yaw',    '0.0',
                '--pitch',  '0.0',
                '--roll',   '0.0',

                '--frame-id',       'nissan9/base_link',
                '--child-frame-id', 'nissan9/laser'],
        ),
        # IncludeLaunchDescription(
        #     PythonLaunchDescriptionSource(
        #         path.join(
        #             get_package_share_directory('nissan_bringup'),
        #             'launch',
        #             '3d_nissan.launch.py'
        #         )
        #     )
        # ),
        # TODO: launch and executeable file missing
        # IncludeLaunchDescription(
        #     PythonLaunchDescriptionSource(
        #         path.join(
        #             get_package_share_directory('nissan_bringup'),
        #             'launch',
        #             'path_and_steering_marker.launch.py'
        #         )
        #     )
        # ),

    ])