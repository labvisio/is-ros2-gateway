from is_ros2_gateway.conversions import topic_is_to_ros
from is_msgs.common_pb2 import ConsumerList


class SubscriptionTracker(object):
    def __init__(self, subscription):
        def no_op(topics):
            pass

        subscription.subscribe("BrokerEvents.Consumers")
        self._topics = set()
        self.on_new_subscription = no_op
        self.on_del_subscription = no_op

    def update(self, consumer_list):
        new_topics = set(
            [
                key
                for key in consumer_list.info
                if key.startswith("ros.") and "*" not in key
            ]
        )
        added = new_topics - self._topics
        deleted = self._topics - new_topics

        self.on_new_subscription([topic_is_to_ros(t) for t in added])
        # self.on_del_subscription([topic_is_to_ros(t) for t in deleted])
        self._topics = new_topics

    def run(self, message):
        if message.topic == "BrokerEvents.Consumers":
            self.update(message.unpack(ConsumerList))
