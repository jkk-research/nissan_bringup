# `nissan_bringup` ROS2 package

<p align="center">
  <img alt="License: BSD-3-Clause" src="https://img.shields.io/badge/license-BSD--3--Clause-3a3a3a?style=flat-square">
  <img alt="ROS 2: Humble" src="https://img.shields.io/badge/ros2-humble-34aec5?style=flat-square">
  <img alt="ROS 2: Jazzy" src="https://img.shields.io/badge/ros2-jazzy-34aec5?style=flat-square">
</p>

🚗 ROS2 package for basic functions on Nissan Leaf


## Install:
```
cd ~/ros2_ws/src
git clone https://github.com/szenergy/nissan_bringup
cd ~/ros2_ws
colcon build --packages-select nissan_bringup --symlink-install --cmake-args=-DCMAKE_BUILD_TYPE=Release
```

## 3D visualization

Both launch files place the car on the `nissan9/base_link` frame (origin: rear axle center).

**Mesh model** (`robot_state_publisher`, publishes `/robot_description`):
```
ros2 launch nissan_bringup 3d_nissan.launch.py
```
- RViz2: add a `RobotModel` display, set *Description Topic* to `/robot_description`.
- Foxglove: start `foxglove_bridge` from a terminal where `install/setup.bash` is sourced, otherwise the `package://nissan_bringup/meshes/...` mesh cannot be resolved.

**Low-poly marker model** (20 primitive markers, `visualization_msgs/MarkerArray` on `/nissan_marker`):
```
ros2 launch nissan_bringup 3d_nissan_marker.launch.py
```
- RViz2: add a `MarkerArray` display with topic `/nissan_marker`.
- Launch arguments: `frame_id` (default `nissan9/base_link`), `topic` (default `nissan_marker`), `publish_rate` (default `1.0` Hz).

# Other packages

## Links
- [ZED](https://github.com/stereolabs/zed-ros2-wrapper)
- [ouster](https://github.com/ouster-lidar/ouster-ros/tree/ros2)
- [duro gps](https://github.com/szenergy/duro_gps_driver/tree/ros2-humble)
- [novatel gps](https://github.com/jkk-research/novatel_gps_driver.git)
- [SICK lidar](https://github.com/szenergy/sick_scan2)

![](https://raw.githubusercontent.com/szenergy/nissan_leaf_ros/master/nissan_bringup/meshes/Nissan_Leaf_Simulation_02_06.png)
