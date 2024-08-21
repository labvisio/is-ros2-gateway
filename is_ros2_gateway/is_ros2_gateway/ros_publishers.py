import rclpy as ros
from rclpy.node import Node

from rosbridge_library.internal.ros_loader import get_message_class

from is_ros2_gateway.conversions import proto_to_rosmsg, topic_is_to_ros
from is_ros2_gateway.ros_pb2 import ROSMessage


class RosPublishers(Node):
    def __init__(self, subscription):
        super().__init__("RosPublishers")
        subscription.subscribe("ros.*")
        self.pub = {}
        self.types = {}

    def get(self, topic, msgtype):
        topic = topic_is_to_ros(topic)
        if topic not in self.pub:
            self.pub[topic] = self.create_publisher(msgtype, topic, 10)
            self.types[topic] = msgtype
        elif self.types[topic] != msgtype:
            raise RuntimeError("Trying to change topic message type")
        return self.pub[topic]

    def run(self, message):
        if message.topic.startswith("ros."):
            try:
                ros_message = message.unpack(ROSMessage)
                ros_type = get_message_class(ros_message.type)
                ros_topic = message.topic
                self.get(ros_topic, ros_type).publish(
                    proto_to_rosmsg(ros_message.content, ros_type)
                )
            except:
                self.get_logger().info("Invalid topic to unpack " + message.topic)
