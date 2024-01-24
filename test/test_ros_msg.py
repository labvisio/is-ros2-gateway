from ros_pb2 import ROSMessage
from google.protobuf.struct_pb2 import Struct

from rosbridge_library.internal.ros_loader import get_message_class
from rosbridge_library.internal.message_conversion import extract_values, populate_instance

import numpy as np


from google.protobuf.json_format import MessageToDict
import numbers
import collections.abc as collections


def _convert_integers(ob):
    if isinstance(ob, collections.Mapping):
        return {k: _convert_integers(v) for k, v in ob.items()}
    else:
        if isinstance(ob, numbers.Number):
            return int(ob) if ob.is_integer() else ob
        elif isinstance(ob, list):
            return [_convert_integers(el) for el in ob]
        return ob


def proto_to_rosmsg(proto, rostype):
    dicti = _convert_integers(MessageToDict(proto))
    return populate_instance(dicti, rostype())



def rosmsg_to_proto(rosmsg):
    struct = Struct()
    struct.update(extract_values(rosmsg))
    return struct

ros_message = ROSMessage()
ros_message.type = "geometry_msgs/PoseWithCovarianceStamped"




PoseWithCovariance_dict = {"header": {"frame_id": "map"}, 
                             "pose": {"pose": 
                                        {"position": {"x": 0}}  
                                      }
                            }

print(PoseWithCovariance_dict["header"]["frame_id"])
print(PoseWithCovariance_dict["pose"]["pose"]["position"]["x"])

PoseWithCovarianceStamped = Struct()
PoseWithCovarianceStamped.update(PoseWithCovariance_dict)

ros_message = ROSMessage(content = PoseWithCovarianceStamped)
ros_message.type = "geometry_msgs/PoseWithCovarianceStamped"


ros_message.content = PoseWithCovarianceStamped
ros_msg = get_message_class(ros_message.type)
print(ros_msg)
a = proto_to_rosmsg(ros_message.content, ros_msg)
print(a)