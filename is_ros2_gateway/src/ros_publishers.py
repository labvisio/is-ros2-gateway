import rclpy as ros
from rclpy.node import Node

from rosbridge_library.internal.ros_loader import get_message_class
from conversions import proto_to_rosmsg
from ros_pb2 import ROSMessage


class RosPublishers(Node):
    def __init__(self, subscription):
        super().__init__('RosPublishers')
        subscription.subscribe("ros.*")
        self.pub = {}
        self.types = {}

    def get(self, topic, msgtype):
        if topic not in self.pub:
            self.pub[topic] = self.create_publisher(
                                                    msgtype, 
                                                    topic, 
                                                    10
                                                    )
            self.types[topic] = msgtype
        elif self.types[topic] != msgtype:
            raise RuntimeError("Trying to change topic message type")
        return self.pub[topic]

    def run(self, message):
        if message.topic.startswith("ros."):
            ros_message = message.unpack(ROSMessage)
            ros_type = get_message_class(ros_message.type)
            ros_topic = message.topic[4:]
            self.get(ros_topic, ros_type).publish(
                proto_to_rosmsg(ros_message.content, ros_type)
                )
