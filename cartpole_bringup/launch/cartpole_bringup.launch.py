from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration, Command
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os
import xacro

def generate_launch_description():

    description_pkg_path = get_package_share_directory("cartpole_description")
    gz_pkg_path = get_package_share_directory("gazebo_ros")
    xacro_file = os.path.join(description_pkg_path, "xacro", "robot.xacro")
    rviz_config = os.path.join(description_pkg_path, "config", "default.cartpole.rviz")
    doc = xacro.parse(open(xacro_file))
    xacro.process_doc(doc)

    cartpole_description = doc.toxml()

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [
                os.path.join(gz_pkg_path, "launch", "gazebo.launch.py")
            ]
        )
    )


    rsp_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        output="screen",
        parameters=[{"robot_description" : cartpole_description, "use_sim_time" : True},],
    )

    jsp_node = Node(
        name="joint_state_publisher",
        package="joint_state_publisher",
        executable="joint_state_publisher",
    )

    spawn_entity = Node(
        package="gazebo_ros",
        executable="spawn_entity.py",
        arguments=["-topic", "/robot_description", "-entity", "cartpole"],
        output="screen",
    )
    # rviz_node = Node(
    #     name="rviz2",
    #     package="rviz2",
    #     executable="rviz2",
    #     arguments=["-d", rviz_config],
    # )

    # jsp_gui_node = Node(
    #     name="joint_state_publisher_gui",
    #     package="joint_state_publisher_gui",
    #     executable="joint_state_publisher_gui",
    # )

    return LaunchDescription([rsp_node, jsp_node, gazebo, spawn_entity]) # rviz_node, jsp_gui_node, gazebo])
