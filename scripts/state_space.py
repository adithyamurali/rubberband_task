#!/usr/bin/env python

# Authors: Adithya Murali and Siddarth Sen
# UC Berkeley, 2014

import roslib
import time
import rospy

class StateSpace:
    def __init__(self):
        self.inOrder = []
        self.inside = []
        self.outside = []

    #Todo
    def addPeg(self):
        pass
    #Todo
    def removePeg(self):
        pass

    def getInOrderEdges(self):
        inOrderPegs = []
        for peg in self.inOrderPegs:
            inOrderPegs.append(peg)

def main():
    defaultStateSpace = StateSpace()
    defaultStateSpace.inOrder = [[1, True, 0], [3, True, 0], [6, True, 0], 
        [8, True, 0], [7, True, 0], [5, False, 0], [4, True, 0]]
    defaultStateSpace.inside = [2]
    defaultStateSpace.outside = [9, 10, 11, 12]
    print defaultStateSpace.getInOrderEdges()
if __name__ == '__main__':
    main()
