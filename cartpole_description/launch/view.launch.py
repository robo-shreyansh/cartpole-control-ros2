from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os
import xacro

def generate_launch_description():

    description_pkg_path = os.path.join(get_package_share_directory("cartpole_description"))
    description_pkg_path = get_package_share_directory("cartpole_description")

    # print(description_pkg_path, "And")
    # print(os.path.join(description_pkg_path))
    xacro_file = os.path.join(description_pkg_path, "xacro", "robot.xacro")
    rviz_config = os.path.join(description_pkg_path, "config", "default.cartpole.rviz")
    doc = xacro.parse(open(xacro_file))
    xacro.process_doc(doc)
    cartpole_description = doc.toxml()
    print("Desc: ", cartpole_description)
    rsp_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        output="screen",
        parameters=[{"robot_description" : cartpole_description},],
    )

    jsp_node = Node(
        name="joint_state_publisher",
        package="joint_state_publisher",
        executable="joint_state_publisher",
    )

    rviz_node = Node(
        name="rviz2",
        package="rviz2",
        executable="rviz2",
        arguments=["-d", rviz_config],
    )

    jsp_gui_node = Node(
        name="joint_state_publisher_gui",
        package="joint_state_publisher_gui",
        executable="joint_state_publisher_gui",
    )

    return LaunchDescription([rsp_node, jsp_node, rviz_node, jsp_gui_node])
    pass