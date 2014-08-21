#!/usr/bin/env python

# Authors: Adithya Murali and Siddarth Sen
# UC Berkeley, 2014

import roslib
import time
import rospy
from state_space import State, Peg, Contour, make_pegs, make_state_space, round_point
import cv2
from plotter import peg_locations, peg_coord, Plotter
import numpy as np
import IPython
from numpy import vstack

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

    def remove_convex(self, start_state = None, peg = None):
        left_peg = start_state.get_left_inside_peg(peg)
        right_peg = start_state.get_right_inside_peg(peg)
        new_contour_pegs = self.convex_hull(start_state, peg, left_peg, right_peg)

        pegs_to_be_added = []
        for elem in new_contour_pegs:
            if (elem != left_peg) and (elem != right_peg):
                pegs_to_be_added.append(elem)

        prev_outside = start_state.outside
        prev_inside = start_state.inside
        prev_contour = start_state.contour
        new_outside = prev_outside[:]
        new_outside.append(peg)
        new_inside = []
        for elem in prev_inside:
            if elem not in pegs_to_be_added:
                new_inside.append(elem)
        list_of_new_pegs = []
        for elem in prev_contour.peg_order:
            if elem != peg:
                list_of_new_pegs.append(prev_contour.peg_dict[elem])
            else:
                for new_peg in pegs_to_be_added:
                    list_of_new_pegs.append(Peg(new_peg, True, 0))
        end_state = State(list_of_new_pegs, new_inside, new_outside)
        assert len(new_inside + new_outside + end_state.contour.peg_order) == 12
        return end_state

    def convex_hull(self, start_state = None, peg = None, left_peg = None, right_peg = None):
        left_coord = list(peg_locations[left_peg])
        right_coord = list(peg_locations[right_peg])
        start_cnt = []
        start_cnt.append([left_coord])
        start_cnt.append([right_coord])
        start_cnt.append([list(peg_locations[peg])])
        final_cnt = []
        final_cnt.append([left_coord])
        final_cnt.append([right_coord])
        start_cnt = np.array(start_cnt).astype(np.float32)
        final_cnt = np.array(final_cnt).astype(np.float32)
        for inside_peg in start_state.inside:
            dist = cv2.pointPolygonTest(start_cnt, peg_locations[inside_peg], False)
            if (dist == 1) or (dist == 0):
                inside_peg_location = np.array([[list(peg_locations[inside_peg])]]).astype(np.float32)
                final_cnt = vstack((final_cnt, inside_peg_location))
        hull = cv2.convexHull(final_cnt)
        hull_pegs = []
        for point in hull:
            hull_pegs.append(peg_coord[round_point(point[0])])
        return hull_pegs

def main():
    # num = 2
    # examples = make_state_space()
    # default_state_space = examples[num]
    # action_space = ActionSpace(default_state_space)
    # result = action_space.remove_convex(default_state_space,12)
    num = 4
    remove_peg = 9
    examples = make_state_space()
    default_state_space = examples[num]
    a = Plotter('remove_peg'+str(remove_peg)+'_start_state_' + str(num) + '.png')
    action_space = ActionSpace(default_state_space)
    end_state = action_space.remove_convex(default_state_space,remove_peg)
    a.plot(default_state_space)


if __name__ == '__main__':
    main()
