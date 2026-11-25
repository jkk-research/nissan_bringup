# `nissan_bringup` ROS2 package

<p align="center">
  <a href="LICENSE"><img alt="License: BSD-3-Clause" src="https://img.shields.io/badge/license-BSD--3--Clause-c94c32?style=flat-square"></a>
  <a href="https://docs.ros.org/en/humble/"><img alt="ROS 2: Humble" src="https://img.shields.io/badge/ros2-humble-34aec5?style=flat-square"></a>
  <a href="https://docs.ros.org/en/jazzy/"><img alt="ROS 2: Jazzy" src="https://img.shields.io/badge/ros2-jazzy-34aec5?style=flat-square"></a>
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

## TF configuration

Two central files in `config/tf/` are read by `tf_static.launch.py`, `gps_nova.launch.py` and `gps_duro.launch.py`:

- `map_origins.yaml`: local map origins (`map_gyor_0`, `map_zala_0`, ...) in the `map` frame. `tf_static.launch.py` publishes `map -> <origin>` for each entry.
- `localization.yaml`:
  - `base_link_source`: `nova` or `duro`, the only source that publishes the `nissan9/base_link` TF.
    - `nova`: `map -> nissan9/base_link` (rear axle center).
    - `duro`: `map -> nissan9/gps -> nissan9/base_link`.
  - `map_origin`: the current site. The Novatel position is shifted by this origin.

The `publish_tf` (nova) and `publish_base_link_tf` (duro) launch arguments override the file for a single run. After editing the YAML files, rebuild the package (or use `--symlink-install`).

# Other packages

## Links
- [ZED](https://github.com/stereolabs/zed-ros2-wrapper)
- [ouster](https://github.com/ouster-lidar/ouster-ros/tree/ros2)
- [duro gps](https://github.com/szenergy/duro_gps_driver/tree/ros2-humble)
- [SICK lidar](https://github.com/szenergy/sick_scan2)
- [novatel gps](https://github.com/jkk-research/novatel_gps_driver.git)

```bash
sudo apt install ros-$ROS_DISTRO-novatel-oem7-msgs
```

![](https://raw.githubusercontent.com/szenergy/nissan_leaf_ros/master/nissan_bringup/meshes/Nissan_Leaf_Simulation_02_06.png)
