import threading
import functools

import rclpy as ros
from rclpy.node import Node

# from rostopic import get_topic_type
from is_wire.core import Message

from rosbridge_library.internal.ros_loader import get_message_class

from is_ros2_gateway.conversions import rosmsg_to_proto, topic_ros_to_is


class RosSubscribers(Node):
    def __init__(self, channel):
        super().__init__("RosSubscribers")
        self.subscribers = {}
        self.channel = channel
        self.lock = threading.RLock()

    def on_new_subscription(self, topics):
        for topic in topics:
            self.subscribe(topic)

    def on_del_subscription(self, topics):
        for topic in topics:
            self.unsubscribe(topic)

    def on_new_message(self, topic, message):

        with self.lock:
            struct = rosmsg_to_proto(message)
            topic_is = topic_ros_to_is(topic)
            self.channel.publish(topic=topic_is, message=Message(content=struct))

    def subscribe(self, topic):
        with self.lock:
            if topic not in self.subscribers:

                topic_type = self.get_topic_type(topic)
                if not topic_type:
                    # raise RuntimeError(
                    #     "Trying to subscribe to invalid topic " + topic)
                    self.get_logger().info(
                        "Trying to subscribe to invalid topic " + topic
                    )
                    return None

                msg_type = get_message_class(topic_type[1][0])

                self.subscribers[topic] = self.create_subscription(
                    msg_type, topic, functools.partial(self.on_new_message, topic), 10
                )

    def unsubscribe(self, topic):
        with self.lock:
            if topic in self.subscribers:
                self.subscribers[topic].unregister()

    def get_topic_type(self, topic_name):
        topics = self.get_topic_names_and_types()
        for topic in topics:
            if topic[0] == topic_name:
                return topic
        return None
