#!/usr/bin/env python

# Authors: Adithya Murali and Siddarth Sen
# UC Berkeley, 2014

import roslib
import time
import rospy
import IPython

class StateSpace:
    def __init__(self, pegs = None, inside = None, outside = None):
        self.contour = Contour(pegs)
        self.inside = inside
        self.outside = outside

    def get_in_order_edges(self):
        return self.contour.get_in_order_edges()

    def get_left_inside_peg(self, peg_num):
        return self.contour.get_left_inside_peg(peg_num)

    def get_right_inside_peg(self, peg_num):
        return self.contour.get_right_inside_peg(peg_num)

class Contour:
    def __init__(self, pegs):
        self.pegs = pegs
        self.peg_order = []
        self.peg_dict = {}
        for peg in pegs:
            self.peg_order.append(peg.peg_num)
            self.peg_dict[peg.peg_num] = peg

    def get_left_inside_peg(self, peg_num):
        i = self.peg_order.index(peg_num)
        i -= 1
        if i == -1:
            i = len(self.peg_order) - 1
        while (i > 0):
            left_peg = self.peg_order[i]
            if self.peg_dict[left_peg].in_or_out == True:
                return left_peg
            i -= 1
        return None

    def get_right_inside_peg(self, peg_num):
        i = self.peg_order.index(peg_num)
        i += 1
        if i == len(self.peg_order):
            i = 0
        while (i < len(self.peg_order)):
            left_peg = self.peg_order[i]
            if self.peg_dict[left_peg].in_or_out == True:
                return left_peg
            i += 1
        return None

    def get_in_order_edges(self):
        i = 0
        noOfEdges = len(self.peg_order) - 2
        edges = []
        while (i <= noOfEdges):
            newEdge = [self.peg_order[i], self.peg_order[i + 1]]
            edges.append(newEdge)
            i += 1
        lastEdge = [self.peg_order[-1], self.peg_order[0]]
        edges.append(lastEdge)
        return edges

class Peg:
    def __init__(self, peg_num = None, in_or_out = False, winding = 0):
        self.peg_num = peg_num
        self.in_or_out = in_or_out
        self.winding = winding

def make_pegs(pegs):
    result = []
    for elem in pegs:
        result.append(Peg(elem[0], elem[1], elem[2]))
    return result

def main():
    pegs = make_pegs([[1, True, 0], [3, True, 0], [6, True, 0], 
        [8, True, 0], [7, True, 0], [5, False, 0], [4, True, 0]])
    a = StateSpace(pegs, [2], [9, 10, 11, 12])
    print a.get_in_order_edges()
    print a.contour.peg_order
    print a.get_right_inside_peg(4)
if __name__ == '__main__':
    main()
