from ros_pb2 import ROSMessage
from google.protobuf.struct_pb2 import Struct

import numpy as np
from is_wire.core import Channel, Message

import time 


ros_message = ROSMessage()
ros_message.type = "geometry_msgs/PoseWithCovarianceStamped"
PoseWithCovariance_dict = {"header": {"frame_id": "map"}, 
                             "pose": {"pose": 
                                        {"position": {"x": 0}}  
                                      }
                            }

PoseWithCovarianceStamped = Struct()
PoseWithCovarianceStamped.update(PoseWithCovariance_dict)

ros_message = ROSMessage(content = PoseWithCovarianceStamped)
ros_message.type = "geometry_msgs/PoseWithCovarianceStamped"


channel = Channel("amqp://10.10.2.211:30000")
message = Message(content = ros_message)

while True:
    print("publishing ros message")
    channel.publish(message, topic="ros.vo")
    time.sleep(0.1)