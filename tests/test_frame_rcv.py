#!/usr/bin/env python
import roslib; roslib.load_manifest('vslam')

import rospy
from rospy.numpy_msg import numpy_msg
from vslam.msg import Floats
import numpy as np

def frames_rcv_callback(data):
    rospy.loginfo("Received : ")
    print(data.data)

def get_frames():
    rospy.init_node('feature_sub')
    rospy.Subscriber('Cframe', numpy_msg(Floats), frames_rcv_callback)
    rospy.spin()

if __name__ == '__main__':
    get_frames()