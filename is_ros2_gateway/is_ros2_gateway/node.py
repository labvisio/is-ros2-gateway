from __future__ import print_function
import threading
import argparse

import rclpy as ros
from rclpy.executors import SingleThreadedExecutor
from is_wire.core import Channel, Message, Subscription, Logger

from is_ros2_gateway.ros_publishers import RosPublishers
from is_ros2_gateway.ros_subscribers import RosSubscribers
from is_ros2_gateway.subscription_tracker import SubscriptionTracker


def ros_thread():
    executor.spin()


def main(args=None):
    ros.init(args=args)

    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="ROS 2 Gateway")
    parser.add_argument(
        "--uri", type=str, required=True, help="URI for the AMQP server"
    )
    parsed_args = parser.parse_args(args=args)

    uri = parsed_args.uri  # Get URI from command-line argument

    in_channel = Channel(uri)
    out_channel = Channel(uri)
    subscription = Subscription(in_channel)
    publishers = RosPublishers(subscription)
    subscribers = RosSubscribers(out_channel)

    global executor
    executor = SingleThreadedExecutor()
    executor.add_node(publishers)
    executor.add_node(subscribers)

    tracker = SubscriptionTracker(subscription)
    tracker.on_del_subscription = subscribers.on_del_subscription
    tracker.on_new_subscription = subscribers.on_new_subscription

    thread = threading.Thread(target=ros_thread)
    thread.start()

    log = Logger("is_bridge")
    log.info("event=Listening")

    while True:
        message = in_channel.consume()
        tracker.run(message)
        publishers.run(message)


if __name__ == "__main__":
    main()
