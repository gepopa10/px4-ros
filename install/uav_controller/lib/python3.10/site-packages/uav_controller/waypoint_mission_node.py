import time

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy, DurabilityPolicy
from rclpy.clock import Clock

from px4_msgs.msg import TrajectorySetpoint
from px4_msgs.msg import OffboardControlMode
from std_srvs.srv import Trigger

class WaypointMission(Node):

    def __init__(self):
        super().__init__('minimal_publisher')
        qos_profile = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            durability=DurabilityPolicy.TRANSIENT_LOCAL,
            history=HistoryPolicy.KEEP_LAST,
            depth=1
        )

        self.way_point_mission_publisher = self.create_publisher(TrajectorySetpoint, '/fmu/in/trajectory_setpoint', qos_profile)
        self.publisher_offboard_mode = self.create_publisher(OffboardControlMode, '/fmu/in/offboard_control_mode', qos_profile)

        self.srv = self.create_service(Trigger, 'launch_mission', self.launch_mission_callback)

    def launch_mission_callback(self, request, response):
        self.launch_mission()
        response.success = True
        response.message = "Message published!"
        return response
    
    def launch_mission(self):
  
    
        t=0
        while(t<5):
            offboard_msg = OffboardControlMode()
            offboard_msg.timestamp = int(Clock().now().nanoseconds / 1000)
            offboard_msg.position = True
            offboard_msg.velocity = False
            offboard_msg.acceleration = False
            self.publisher_offboard_mode.publish(offboard_msg) 
            trajectory_msg = TrajectorySetpoint()
            trajectory_msg.timestamp = int(Clock().now().nanoseconds / 1000)
            trajectory_msg.velocity[0] = float('nan')
            trajectory_msg.velocity[1] = float('nan')
            trajectory_msg.velocity[2] = float('nan')
            trajectory_msg.position[0] = 1.0
            trajectory_msg.position[1] = 0.0
            trajectory_msg.position[2] = -5.0
            trajectory_msg.acceleration[0] = float('nan')
            trajectory_msg.acceleration[1] = float('nan')
            trajectory_msg.acceleration[2] = float('nan')
            trajectory_msg.yaw = 0.0
            trajectory_msg.yawspeed = float('nan')

            self.way_point_mission_publisher.publish(trajectory_msg)
            print("here")
            time.sleep(0.05)
            t+=0.05

        # trajectory_msg.timestamp = int(Clock().now().nanoseconds / 1000)
        # trajectory_msg.position[0] = 2.0
        # self.way_point_mission_publisher.publish(trajectory_msg)
        # time.sleep(2)

        # trajectory_msg.timestamp = int(Clock().now().nanoseconds / 1000)
        # trajectory_msg.position[1] = 2.0
        # self.way_point_mission_publisher.publish(trajectory_msg)
        # time.sleep(2)

        # trajectory_msg.timestamp = int(Clock().now().nanoseconds / 1000)
        # trajectory_msg.position[0] = 0.0
        # trajectory_msg.position[1] = 0.0
        # trajectory_msg.position[2] = -5.0
        # self.way_point_mission_publisher.publish(trajectory_msg)

        
def main(args=None):
    rclpy.init(args=args)
    node = WaypointMission()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()