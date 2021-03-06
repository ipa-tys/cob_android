#!/usr/bin/env python
import time

import roslib
roslib.load_manifest('cob_android_script_server')
import rospy
import actionlib

from cob_android_script_server.srv import *
from simple_script_server import *

sss = simple_script_server()

## Script server class which inherits from script class.
#
# Implements actionlib interface for the script server.
#
class script_server():
	## Initializes the actionlib interface of the script server.
	#
	def __init__(self):
		rospy.Service('/script_server_android/script_service', Script, self.service_cb)

	def service_cb(self, req):
		res = ScriptResponse()
		if req.function_name == "trigger":
			if req.parameter_name == "init":
				handle01 = sss.init(req.component_name)
			elif req.parameter_name == "stop":
				handle01 = sss.stop(req.component_name)
			elif req.function_name == "recover":
				handle01 = sss.recover(req.component_name)				
		elif req.function_name == "move":
			handle01 = sss.move(req.component_name,req.parameter_name,mode=req.mode)
		else:
				rospy.logerr("function <<%s>> not supported", req.function_name)
				res.error_code = -1
				return res

                res.error_code = handle01.get_error_code()
                if res.error_code == 0:
                        rospy.logdebug("service result success")
                else:
                        rospy.logerr("service result error")
		return res

## Main routine for running the script server
#
if __name__ == '__main__':
	rospy.init_node('script_server')
	script_server()
	rospy.loginfo("script_server is running")
	rospy.spin()
