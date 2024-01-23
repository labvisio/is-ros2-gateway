from __future__ import print_function

import rclpy as ros
from rclpy.executors import SingleThreadedExecutor

from is_wire.core import Channel, Message, Subscription, Logger

#from is_bridge_lib import RosPublishers, RosSubscribers, SubscriptionTracker
from ros_publishers import RosPublishers
from ros_subscribers import RosSubscribers
from subscription_tracker import SubscriptionTracker

import threading

def ros_thread():
    executor.spin()

def main(args=None):
    ros.init(args=args)
    uri = "amqp://guest:guest@localhost:5672"
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

if __name__ == '__main__':
    main()            