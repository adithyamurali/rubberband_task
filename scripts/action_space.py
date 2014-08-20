#!/usr/bin/env python

# Authors: Adithya Murali and Siddarth Sen
# UC Berkeley, 2014

import roslib
import time
import rospy
from state_space import StateSpace, Peg, Contour, make_pegs
import cv2
from plotter import peg_locations, peg_coord
import numpy as np
import IPython

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

class ActionSpace:
    def __init__(self, default_state_space = None):
        self.default_state_space = default_state_space

    # #Todo
    # def execute(self, action, start_state, peg):

    # def add_peg(self, start_state, peg):

    def convex_hull(self, start_state = None, peg = None):
        if start_state is None:
            start_state = self.default_state_space
        left_peg = start_state.get_left_inside_peg(peg)
        right_peg = start_state.get_right_inside_peg(peg)
        left_coord = list(peg_locations[left_peg])
        right_coord = list(peg_locations[right_peg])
        start_cnt = []
        start_cnt.append([left_coord])
        start_cnt.append([right_coord])
        start_cnt.append([list(peg_locations[peg])])
        final_cnt = []
        final_cnt.append([left_coord])
        final_cnt.append([right_coord])
        # IPython.embed()
        start_cnt = np.array(start_cnt)
        start_cnt = start_cnt.astype(np.float32)
        final_cnt = np.array(final_cnt)
        final_cnt = final_cnt.astype(np.float32)
        for inside_peg in start_state.inside:
            print start_cnt, inside_peg, peg_locations[inside_peg]
            # IPython.embed()
            dist = cv2.pointPolygonTest(start_cnt, peg_locations[inside_peg], False)
            if (dist == 1) or (dist == 0):
                final_cnt.append([list(peg_locations[inside_peg])])
        hull = cv2.convexHull(final_cnt)
        IPython.embed()
        hull_pegs = []
        for point in hull:
            for peg_num, location in peg_locations.items():
                if location == point:
                    hull_pegs.append(peg_num)
        return hull_pegs

def make_state_space():
    pegs = make_pegs([[1, True, 0], [3, True, 0], [6, True, 0], 
        [8, True, 0], [7, True, 0], [5, False, 0], [4, True, 0]])
    default_state_space = StateSpace(pegs, [2], [9, 10, 11, 12])

def main():
    pegs = make_pegs([[1, True, 0], [3, True, 0], [6, True, 0], 
        [8, True, 0], [7, True, 0], [5, False, 0], [4, True, 0]])
    default_state_space = StateSpace(pegs, [2], [9, 10, 11, 12])
    # a = Plotter('test3.png')
    # a.plot(default_state_space)
    action_space = ActionSpace(default_state_space)
    print action_space.convex_hull(peg=7)


if __name__ == '__main__':
    main()
