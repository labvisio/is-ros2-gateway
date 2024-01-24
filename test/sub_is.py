from is_wire.core import Channel, Subscription
from google.protobuf.struct_pb2 import Struct
channel = Channel("amqp://10.10.2.211:30000")

subscription = Subscription(channel)
subscription.subscribe(topic="ros.topic")

while True:
    message = channel.consume()
    print(message.unpack(Struct))
    