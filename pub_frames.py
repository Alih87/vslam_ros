#!/usr/bin/env python
import roslib; roslib.load_manifest('vslam')

from time import sleep
import rospy
from rospy.numpy_msg import numpy_msg
from vslam.msg import Floats
import pyrealsense2 as rs
import numpy as np
import cv2

CAM_ID = 108222250981

# def ascend_key(x):
#     return x.distance

pipeline = rs.pipeline()
config = rs.config()
#config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

pipeline.start(config)

## Get camera intrinsics

# profile = pipeline.get_active_profile()
# depth_prof = rs.video_stream_profile(profile.get_stream(rs.stream.depth))
# depth_intr = depth_prof.get_intrinsics()

def frame_publisher():
    pub = rospy.Publisher('Cframe', numpy_msg(Floats), queue_size=10)
    rospy.init_node('feature_pub')
    rate = rospy.Rate(10)

    while not rospy.is_shutdown():
        frames = pipeline.wait_for_frames()
        color = np.asanyarray(frames.get_color_frame().get_data())
        gray = cv2.resize(cv2.cvtColor(color, cv2.COLOR_RGB2GRAY), (240,320))
        frame = np.asanyarray(gray.reshape((240*320, 1)))
        pub.publish(frame)
        rate.sleep()

if __name__ == '__main__':
    try:
        frame_publisher()
    except rospy.ROSInterruptException:
        pass
    