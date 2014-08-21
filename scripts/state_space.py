#!/usr/bin/env python

# Authors: Adithya Murali and Siddarth Sen
# UC Berkeley, 2014

import roslib
import time
import rospy
import IPython
import numpy as np
import cv2

peg_locations = {1: (0.0127, 0.0499),
                 2: (0.0150, 0.0321),
                 3: (0.0124, 0.0146),
                 4: (0.0419, 0.0500),
                 5: (0.0397, 0.0319),
                 6: (0.0407, 0.0136),
                 7: (0.0596, 0.0420),
                 8: (0.0594, 0.0201),
                 9: (0.0768, 0.0566),
                 10: (0.0765, 0.0054),
                 11: (0.0932, 0.0414),
                 12: (0.0934, 0.0191),
                 }
neighbors_graph = {1: (2, 4, 5),
                 2: (1, 3, 4, 5, 6),
                 3: (2, 5, 6),
                 4: (1, 2, 5, 7),
                 5: (1, 2, 3, 4, 6, 7, 8),
                 6: (2, 3, 5, 8),
                 7: (4, 5, 8, 9, 11, 12),
                 8: (5, 6, 7, 10, 11, 12),
                 9: (7, 11),
                 10: (8, 12),
                 11: (7, 8, 9, 12),
                 12: (7, 8, 10, 11),
                }

peg_coord = {(0.0127, 0.0499) : 1,
            (0.015, 0.0321): 2,
            (0.0124, 0.0146) : 3,
            (0.0419, 0.0500) : 4,
            (0.0397, 0.0319) : 5,
            (0.0407, 0.0136) : 6,
            (0.0596, 0.0420) : 7,
            (0.0594, 0.0201) : 8, 
            (0.0768, 0.0566) : 9,
            (0.0765, 0.0054) : 10,
            (0.0932, 0.0414) : 11,
            (0.0934, 0.0191) : 12,
             }

class State:
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

    def get_left_peg(self, peg_num):
        return self.contour.get_left_peg(peg_num)

    def get_right_peg(self, peg_num):
        return self.contour.get_right_peg(peg_num)

    def get_add_actions(self):
        edges = self.get_in_order_edges()
        add_actions = []
        possible_pegs_to_add = self.inside + self.outside
        for edge in edges:
            for peg in possible_pegs_to_add:
                # form a contour with the 3 points
                pt1 = peg_locations[edge[0]]
                pt2 = peg_locations[edge[1]]
                pt3 = peg_locations[peg]

                contour = self.get_contour([pt1,pt2,pt3])
                pegs_inside_contour = self.get_pegs_inside_contour(contour)
                if len(pegs_inside_contour) == 0: # no pegs inside contour so no additional interactions
                    action = AddAction(edge, peg)
                    add_actions.append(action)
        return add_actions

    def get_convex_add_actions(self):
        """ simply return a list outside pegs that can be added to a convex shape """
        return self.outside

    def get_convex_next_state(self, action):
        """ returns the next state where action is just a peg number to add the convex shape"""
        contour_pegs = self.contour.peg_order
        pts = contour_pegs[:] + [action]
        print pts
        coordinates = [peg_locations[a] for a in pts]
        contour = self.get_contour(coordinates, convex=True)
        peg_list = []
        for pt in contour:
            pt = round_point(pt)
            peg = peg_coord[pt]
            peg_list.append([peg, True, 0])
        pegs_inside_contour = self.get_pegs_inside_contour(contour)
        inside = []
        outside = []
        for key in peg_locations:
            if key in peg_list:
                continue
            if key in pegs_inside_contour:
                inside.append(key)
                continue
            outside.append(key)
        return State(make_pegs(peg_list), inside, outside)


    def get_contour(self, points, convex=False):
        """ returns an cv2 contour given a list of tuples as points """
        # IPython.embed()
        contour = np.array([[a[0], a[1]] for a in points], dtype=np.float32) # convert it to a list of lists
        if convex:
            contour = cv2.convexHull(contour)
            contour = np.array([ a[0] for a in contour], dtype=np.float32)
        return contour

    def get_pegs_inside_contour(self, contour):
        """ returns a list of pegs by number that are inside a given contour """
        pegs_inside_contour = []
        for key in peg_locations:
            pt = peg_locations[key]
            # print cv2.pointPolygonTest(contour, pt, True)
            if cv2.pointPolygonTest(contour, pt, True) > 0:
                pegs_inside_contour.append(key)
        return pegs_inside_contour



class AddAction:
    def __init__(self, edge, peg):
        self.edge = edge # edge to grasp ex: (1,2)
        self.peg = peg # peg to grasp ex: 5

    def __repr__(self):
        return "<Add: [edge:(%d,%d), peg:%d]>"%(self.edge[0], self.edge[1], self.peg)


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

    def get_left_peg(self, peg_num):
        i = self.peg_order.index(peg_num)
        i -= 1
        if i == -1:
            return len(self.peg_order) - 1
        return self.peg_order[i]

    def get_right_peg(self, peg_num):
        i = self.peg_order.index(peg_num)
        i += 1
        if i == len(self.peg_order):
            i = 0
        return self.peg_order[i]

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

def make_state_space():
    examples = {}
    pegs1 = make_pegs([[1, True, 0], [3, True, 0], [6, True, 0], 
        [8, True, 0], [7, True, 0], [5, False, 0], [4, True, 0]])
    state_space_1 = State(pegs1, [2], [9, 10, 11, 12])
    examples[1] = state_space_1

    pegs2 = make_pegs([[2, True, 0], [3, True, 0], [6, True, 0], [12, True, 0], [5, True, 0]])
    state_space_2 = State(pegs2, [8], [1, 4, 7, 9, 10, 11])
    examples[2] = state_space_2

    pegs3 = make_pegs([[1, True, 0], [4, True, 0], [8, True, 0], [6, True, 0], [3, True, 0]])
    state_space_3 = State(pegs3, [5], [7,9,10,11,12])
    examples[3] = state_space_3

    pegs4 = make_pegs([[1, True, 0], [3, True, 0], [10, True, 0], [9, True, 0]])
    state_space_4 = State(pegs4, [2,4,5,6,7,8], [11, 12])
    examples[4] = state_space_4

    pegs5 = make_pegs([[1, True, 0], [3, True, 0], [6, True, 0], [5, False, 0], [7, False, 0],
     [11, True, 0], [4, True, 0]])
    state_space_5 = State(pegs5, [2], [8, 9, 10, 12])

    examples[5] = state_space_5

    return examples

def round_point(point):
    return (round(point[0], 4), round(point[1], 4))

def main():
    examples = make_state_space()
    a = examples[3]
    next_state = a.get_convex_next_state(10)
    # print a.get_add_actions()

if __name__ == '__main__':
    main()
