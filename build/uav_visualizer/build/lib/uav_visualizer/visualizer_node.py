import numpy as np
import math

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy

from px4_msgs.msg import VehicleAttitude
from px4_msgs.msg import VehicleOdometry
from px4_msgs.msg import TrajectorySetpoint
from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import Path, Odometry
from geometry_msgs.msg import TransformStamped
from tf2_ros import TransformBroadcaster, StaticTransformBroadcaster

class UAVVisualizer(Node):

    def __init__(self):
        super().__init__('uav_visualizer')

        ## Configure subscritpions
        qos_profile = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            history=HistoryPolicy.KEEP_LAST,
            depth=1
        )

        self.attitude_sub = self.create_subscription(
            VehicleAttitude,
            '/fmu/out/vehicle_attitude',
            self.vehicle_attitude_callback,
            qos_profile)
        self.local_position_sub = self.create_subscription(
            VehicleOdometry,
            '/fmu/out/vehicle_odometry',
            self.vehicle_local_position_callback,
            qos_profile)
        self.setpoint_sub = self.create_subscription(
            TrajectorySetpoint,
            '/fmu/in/trajectory_setpoint',
            self.trajectory_setpoint_callback,
            qos_profile)
        self.odom_sub = self.create_subscription(
            Odometry,
            '/odom',
            self.odom_callback,
            qos_profile)

        self.vehicle_pose_pub = self.create_publisher(PoseStamped, '/uav_visualizer/vehicle_pose', 10)
        self.vehicle_path_pub = self.create_publisher(Path, '/uav_visualizer/vehicle_path', 10)
        self.setpoint_path_pub = self.create_publisher(Path, '/uav_visualizer/setpoint_path', 10)

        self.vehicle_attitude = np.array([1.0, 0.0, 0.0, 0.0])
        self.vehicle_local_position = np.array([0.0, 0.0, 0.0])
        self.vehicle_global_attitude = np.array([1.0, 0.0, 0.0, 0.0])
        self.vehicle_global_position = np.array([0.0, 0.0, 0.0])
        self.vehicle_local_velocity = np.array([0.0, 0.0, 0.0])
        self.setpoint_position = np.array([0.0, 0.0, 0.0])
        self.vehicle_path_msg = Path()
        self.setpoint_path_msg = Path()
        timer_period = 0.05  # seconds
        self.timer = self.create_timer(timer_period, self.cmdloop_callback)
        
        self.position_time = 0
        self.tf_broadcaster = TransformBroadcaster(self)
        self.static_tf_broadcaster = StaticTransformBroadcaster(self)
        self.FRAME_ID = 'world'

    def vector2PoseMsg(self, position, attitude):
        pose_msg = PoseStamped()
        pose_msg.header.frame_id=self.FRAME_ID
        pose_msg.pose.orientation.w = attitude[0]
        pose_msg.pose.orientation.x = attitude[1]
        pose_msg.pose.orientation.y = attitude[2]
        pose_msg.pose.orientation.z = attitude[3]
        pose_msg.pose.position.x = position[0]
        pose_msg.pose.position.y = position[1]
        pose_msg.pose.position.z = position[2]
        return pose_msg

    def vehicle_attitude_callback(self, msg):
        # TODO: handle NED->ENU transformation 
        self.vehicle_attitude[0] = msg.q[0]
        self.vehicle_attitude[1] = msg.q[1]
        self.vehicle_attitude[2] = -msg.q[2]
        self.vehicle_attitude[3] = -msg.q[3]

    def vehicle_local_position_callback(self, msg):
        # TODO: handle NED->ENU transformation 
        self.position_time = msg.timestamp
        self.vehicle_local_position[0] = msg.position[0]
        self.vehicle_local_position[1] = -msg.position[1]
        self.vehicle_local_position[2] = -msg.position[2]
        self.vehicle_local_velocity[0] = msg.velocity[0]
        self.vehicle_local_velocity[1] = -msg.velocity[1]
        self.vehicle_local_velocity[2] = -msg.velocity[2]

    def trajectory_setpoint_callback(self, msg):
        if(math.isnan(msg.position[0]) or math.isnan(msg.position[1]) or math.isnan(msg.position[2])):
            return
        self.setpoint_position[0] = msg.position[1]
        self.setpoint_position[1] = msg.position[0]
        self.setpoint_position[2] = -msg.position[2]

    def cmdloop_callback(self):
        vehicle_pose_msg = self.vector2PoseMsg(self.vehicle_global_position, self.vehicle_global_attitude)
        self.vehicle_pose_pub.publish(vehicle_pose_msg)

        # Publish time history of the vehicle path
        self.vehicle_path_msg.header = vehicle_pose_msg.header
        self.vehicle_path_msg.poses.append(vehicle_pose_msg) 
        self.vehicle_path_pub.publish(self.vehicle_path_msg)

        # Publish time history of the vehicle path
        setpoint_pose_msg = self.vector2PoseMsg(self.setpoint_position, self.vehicle_attitude)
        self.setpoint_path_msg.header = setpoint_pose_msg.header
        self.setpoint_path_msg.poses.append(setpoint_pose_msg)
        self.setpoint_path_pub.publish(self.setpoint_path_msg)

    def odom_callback(self, msg):       
        self.vehicle_global_position[0] = msg.pose.pose.position.x
        self.vehicle_global_position[1] = msg.pose.pose.position.y
        self.vehicle_global_position[2] = msg.pose.pose.position.z

        self.vehicle_global_attitude[0] = msg.pose.pose.orientation.w
        self.vehicle_global_attitude[1] = msg.pose.pose.orientation.x
        self.vehicle_global_attitude[2] = msg.pose.pose.orientation.y
        self.vehicle_global_attitude[3] = msg.pose.pose.orientation.z

        t = TransformStamped()
        t.header = msg.header
        t.header.frame_id = 'world'
        t.child_frame_id = 'base_link'

        t.transform.translation.x = msg.pose.pose.position.x
        t.transform.translation.y = msg.pose.pose.position.y
        t.transform.translation.z = msg.pose.pose.position.z

        t.transform.rotation = msg.pose.pose.orientation

        # Send the transformation
        self.tf_broadcaster.sendTransform(t)

        static_transform = TransformStamped()
        static_transform.header = msg.header
        static_transform.header.frame_id = 'base_link'  # Parent frame
        static_transform.child_frame_id = 'camera_link'   # Child frame

        static_transform.transform.translation.x = 0.1
        static_transform.transform.translation.y = 0.0
        static_transform.transform.translation.z = 0.0

        static_transform.transform.rotation.x = -0.5
        static_transform.transform.rotation.y = 0.5
        static_transform.transform.rotation.z = -0.5
        static_transform.transform.rotation.w = 0.5

        self.static_tf_broadcaster.sendTransform(static_transform)
        

def main(args=None):
    rclpy.init(args=args)

    uav_visualizer = UAVVisualizer()

    rclpy.spin(uav_visualizer)

    uav_visualizer.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()