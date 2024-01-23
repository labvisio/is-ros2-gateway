from __future__ import print_function
import pytest
from is_bridge_lib.conversions import rosmsg_to_proto, proto_to_rosmsg
from geometry_msgs.msg import PoseWithCovariance, Point32
from sensor_msgs.msg import PointCloud, JoyFeedback, JoyFeedbackArray


def _messages():
    pose = PoseWithCovariance()
    pose.pose.position.x = 1
    pose.pose.position.y = 2
    pose.pose.position.z = 3
    pose.pose.orientation.x = 4
    pose.pose.orientation.y = 5.0
    pose.pose.orientation.z = 6
    pose.pose.orientation.w = 7
    pose.covariance = range(36)

    cloud = PointCloud()
    point = Point32()
    point.x = 1
    point.y = 2
    point.z = 3
    cloud.points.append(point)

    jfa = JoyFeedbackArray()
    jf = JoyFeedback()
    jf.type  = JoyFeedback.TYPE_BUZZER
    jf.id = 1
    jfa.array.append(jf)

    return [pose, cloud, jfa]


def test_conversion():
    for rosmsg in _messages():
        newrosmsg = proto_to_rosmsg(rosmsg_to_proto(rosmsg), type(rosmsg))
        assert rosmsg == newrosmsg
