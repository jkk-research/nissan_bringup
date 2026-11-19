## runs left and right c2 cameras
# /nissan9/camera/camera0/camera_info
# /nissan9/camera/camera0/image_compressed
# /nissan9/camera/camera1/camera_info
# /nissan9/camera/camera1/image_compressed

import argparse
import os
import sys
from pathlib import Path  
from typing import List, Optional
from ament_index_python.packages import get_package_share_directory
from pydantic import BaseModel, root_validator, validator
from launch import LaunchDescription  
from launch.actions import DeclareLaunchArgument, TimerAction
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node  
from launch_ros.parameter_descriptions import ParameterValue

nissan_bringup_pkg_dir = get_package_share_directory('nissan_bringup')


class CameraConfig(BaseModel):
    name: str = 'camera0'
    param_path: Path = Path(nissan_bringup_pkg_dir, 'config', 'camera', 'tieriv_c2_camera_params.yaml')
    remappings: Optional[List]
    namespace: Optional[str]

    @validator('param_path')
    def validate_param_path(cls, value):
        if value and not value.exists():
            raise FileNotFoundError(f'Could not find parameter file: {value}')
        return value

    @root_validator(allow_reuse=True)
    def validate_root(cls, values):
        name = values.get('name')
        remappings = values.get('remappings')
        if name and not remappings:
            # Automatically set remappings if name is set
            remappings = [
                ('image_raw/compressed', f'/nissan9/camera/{name}/image_compressed'),
                ('camera_info', f'/nissan9/camera/{name}/camera_info'),
            ]
        values['remappings'] = remappings
        return values

# # Hack to get relative import of .camera_config file working
# dir_path = os.path.dirname(os.path.realpath(__file__))
# sys.path.append(dir_path)


CAMERAS = []
CAMERAS.append(
    CameraConfig(
        name='camera0',
        param_path=Path(nissan_bringup_pkg_dir, 'config', 'camera', 'tieriv_c2_camera_params.yaml')
    )
)    
## sleep to allow multiple cameras to be recognized

# CAMERAS.append(
#     CameraConfig(
#         name='camera1',
#         param_path=Path(nissan_bringup_pkg_dir, 'config', 'camera', 'tieriv_c2_camera_params_1.yaml')
    # )
    # Add more Camera's here and they will automatically be launched below
# )


def generate_launch_description():
    ld = LaunchDescription()

    parser = argparse.ArgumentParser(description='usb_cam demo')
    parser.add_argument('-n', '--node-name', dest='node_name', type=str, help='name for device', default='usb_cam')

    camera_node = Node(
            package='usb_cam', executable='usb_cam_node_exe', output='screen',
            name=CAMERAS[0].name,
            namespace=CAMERAS[0].namespace,
            parameters=[
                CAMERAS[0].param_path,
                {
                    'image_raw.enable_pub_plugins': ['image_transport/compressed'],
                    'output_width': ParameterValue(LaunchConfiguration('image_width'), value_type=int),
                    'output_height': ParameterValue(LaunchConfiguration('image_height'), value_type=int),
                },
            ],
            remappings=CAMERAS[0].remappings
        )

    # camera_node1 = Node(    
    #         package='usb_cam', executable='usb_cam_node_exe', output='screen',
    #         name=CAMERAS[1].name,
    #         namespace=CAMERAS[1].namespace,
    #         parameters=[CAMERAS[1].param_path],
    #         remappings=CAMERAS[1].remappings
    #     )


    return LaunchDescription([
        DeclareLaunchArgument(
            'image_width', default_value='1296',
            description='Published image width in pixels. Use 0 for the capture width.',
        ),
        DeclareLaunchArgument(
            'image_height', default_value='720',
            description='Published image height in pixels. Use 0 for the capture height.',
        ),
        TimerAction(period=0.0, actions=[camera_node]),
        # TimerAction(period=5.0, actions=[camera_node1]),
    ])
