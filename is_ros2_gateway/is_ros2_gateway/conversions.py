import numbers
import collections.abc as collections

from google.protobuf.struct_pb2 import Struct
from google.protobuf.json_format import MessageToDict

from rosbridge_library.internal.message_conversion import extract_values, populate_instance

def topic_is_to_ros(topic):
    return topic[3:].replace(".", "/")


def topic_ros_to_is(topic):
    return "ros" + topic.replace("/", ".")


def rosmsg_to_proto(rosmsg):
    struct = Struct()
    struct.update(extract_values(rosmsg))
    return struct


# Traverse the object searching for numbers that can be converted to integers 
# to avoid a type mismatch when converting back to ros messages.
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
