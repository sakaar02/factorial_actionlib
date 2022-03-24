#! /usr/bin/env python

from __future__ import print_function
import rospy
import sys

import actionlib

import factorial_actionlib.msg

def factorial_client():
    client = actionlib.SimpleActionClient('idontcare', factorial_actionlib.msg.factorialAction)
    client.wait_for_server()

    goal = factorial_actionlib.msg.factorialGoal(number = 7)
    print("goal published %i" % (goal.number))

    client.send_goal(goal)
    client.wait_for_result()

    n = client.get_result()
    print("hel", n.factorial)
    return n.factorial

if __name__ == '__main__':
    try:
        rospy.init_node('noonecares')
        result = factorial_client()
        print("factorial is",result)
        # print("result",result) 

    except rospy.ROSInterruptException:
        print("program interupted before completion", file = sys.stderr)