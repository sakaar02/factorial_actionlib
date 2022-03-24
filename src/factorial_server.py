#! /usr/bin/env python

import rospy

import actionlib

import factorial_actionlib.msg

class factorial(object):
    _feedback = factorial_actionlib.msg.factorialFeedback()
    _result = factorial_actionlib.msg.factorialResult()

    def __init__(self,name):
        self.action_name = name
        self.action_server = actionlib.SimpleActionServer(self.action_name, factorial_actionlib.msg.factorialAction, 
                                                          execute_cb = self.server_callback, auto_start = False)
        self.action_server.start()

    def server_callback(self,goal):
        r = rospy.Rate(1)
        success = True

        self._feedback.factorial = 1    

        rospy.loginfo("numbers recieved")      

        for i in range(goal.number):      
            if self.action_server.is_preempt_requested():
                rospy.loginfo("%s Preempted" % self.action_name)
                self.action_server.set_preempted()
                success = False
                break
            
            else:
                self._feedback.factorial = self._feedback.factorial * (i+1)     

            rospy.loginfo("factorial is %i" % self._feedback.factorial)

            self.action_server.publish_feedback(self._feedback)

            r.sleep()

        if success:
            self._result.factorial = self._feedback.factorial
            rospy.loginfo('%s: Succeeded' % self.action_name)
            self.action_server.set_succeeded(self._result)

if __name__ == "__main__":
    rospy.init_node("idontcare")
    server = factorial(rospy.get_name())
    rospy.spin()