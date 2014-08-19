#!/usr/bin/env python

# Authors: Adithya Murali and Siddarth Sen
# UC Berkeley, 2014

import roslib
import time
import rospy

class StateSpace:
    def __init__(self, inOrder = None, inside = None, outside = None):
        self.inOrder = inOrder
        self.inside = inside
        self.outside = outside

    #Todo
    def addPeg(self):
        pass
    #Todo
    def removePeg(self):
        pass

    def getInOrderEdges(self):
        inOrderPegs = []
        for peg in self.inOrder:
            inOrderPegs.append(peg[0])
        i = 0
        noOfEdges = len(inOrderPegs) - 2
        edges = []
        while (i <= noOfEdges):
            newEdge = [inOrderPegs[i], inOrderPegs[i + 1]]
            edges.append(newEdge)
            i += 1
        lastEdge = [inOrderPegs[-1], inOrderPegs[0]]
        edges.append(lastEdge)
        return edges

def main():
    defaultStateSpace = StateSpace()
    defaultStateSpace.inOrder = [[1, True, 0], [3, True, 0], [6, True, 0], 
        [8, True, 0], [7, True, 0], [5, False, 0], [4, True, 0]]
    defaultStateSpace.inside = [2]
    defaultStateSpace.outside = [9, 10, 11, 12]
    print defaultStateSpace.getInOrderEdges()
if __name__ == '__main__':
    main()
