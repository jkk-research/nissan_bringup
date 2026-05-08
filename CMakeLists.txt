cmake_minimum_required(VERSION 3.8)
project(nissan_bringup)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
# uncomment the following section in order to fill in
# further dependencies manually.
# find_package(<dependency> REQUIRED)
find_package(rclcpp REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(tf2 REQUIRED)
find_package(tf2_msgs REQUIRED)
find_package(tf2_ros REQUIRED)
find_package(tf2_geometry_msgs REQUIRED)
find_package(novatel_oem7_msgs REQUIRED)
find_package(nav_msgs REQUIRED)


set(ament_dependencies
  rclcpp
  geometry_msgs
  tf2
  tf2_msgs
  tf2_ros
  tf2_geometry_msgs
  novatel_oem7_msgs
  nav_msgs
)




add_executable(global_parameter src/global_parameter_node.cpp)
ament_target_dependencies(global_parameter ${ament_dependencies})

add_executable(nova_oem7_to_tf src/nova_oem7_to_tf.cpp)
ament_target_dependencies(nova_oem7_to_tf ${ament_dependencies})

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # the following line skips the linter which checks for copyrights
  # comment the line when a copyright and license is added to all source files
  set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo)
  # comment the line when this package is in a git repo and when
  # a copyright and license is added to all source files
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

install(TARGETS
  global_parameter
  nova_oem7_to_tf
  DESTINATION lib/${PROJECT_NAME}
)

install(DIRECTORY launch
  DESTINATION share/${PROJECT_NAME})

install(DIRECTORY config
  DESTINATION share/${PROJECT_NAME})

ament_package()
