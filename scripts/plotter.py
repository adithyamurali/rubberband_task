#!/usr/bin/env python

# Authors: Adithya Murali and Siddarth Sen
# UC Berkeley, 2014

import matplotlib.pyplot as plt
import matplotlib as mpl
import IPython
from state_space import State, Peg, Contour, make_pegs, make_state_space
import numpy as np

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

peg_coord = {(0.0127, 0.0499) : 1,
			(0.0150, 0.0321): 2,
			(0.0124, 0.0146) : 3,
			(0.0419, 0.0500) : 4,
			(0.0397, 0.0319) : 5,
			(0.0407, 0.0136) : 6,
			(0.0596                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        , 0.0420) : 7,
			(0.0594, 0.0201) : 8, 
			(0.0768, 0.0566) : 9,
			(0.0765, 0.0054) : 10,
			(0.0932, 0.0414) : 11,
			(0.0934, 0.0191) : 12,
			 }

class Plotter:
	def __init__(self, file_name):
		self.fig = plt.figure(figsize=(10,7)) # figure object
		plt.axis([0.0, 0.1, 0.0, 0.07]) # set the axis
		self.file_name = file_name
	def plot(self, state_space):
		self.plot_pegs(state_space)
		self.plot_lines(state_space.get_in_order_edges())
		self.plot_labels()
		self.fig.savefig(self.file_name)

	def plot_pegs(self, state_space):		
		fig = self.fig
		rubberband_pegs = state_space.contour.peg_order
		for key in peg_locations:
			x,y = peg_locations[key]
			if key in rubberband_pegs:
				circle = plt.Circle((x,y), 0.001, color='b')
			else:
				circle = plt.Circle((x,y), 0.001, color='r')
			fig.gca().add_artist(circle)

	def plot_labels(self):
		fig = self.fig
		for peg in peg_locations.keys():
			coord = peg_locations[peg]
			fig.gca().text(coord[0], coord[1] + 0.002, str(peg), color='r')

	def plot_lines(self, lines):
		edges = []
		for line in lines:
			start = peg_locations[line[0]]
			end = peg_locations[line[1]]
			edges.append((start, end))

		true_points = []	
		for i in range(len(edges)):
			p1 = edges[i-1][0]
			p2 = edges[i][0]
			p3 = edges[i][1]
			v1 = [p2[0]-p1[0], p2[1]-p1[1]]
			v2 = [p2[0]-p3[0], p2[1]-p3[1]]

			v = [v1[0]+v2[0], v1[1]+v2[1]] # form the vector
			v_mag = np.sqrt((np.power(v[0],2) + np.power(v[1], 2))) # get its magnitude
			v = [v[0]/v_mag, v[1]/v_mag] # normalize it

			pt = (p2[0]+0.003*v[0], p2[1]+0.003*v[1])
			true_points.append(pt)

		edges = []
		for i in range(len(true_points)):
			edges.append((true_points[i-1], true_points[i]))
		lc = mpl.collections.LineCollection(edges, linewidths = 2, color="g")
		fig = plt.gcf()
		fig.gca().add_collection(lc)

def make_pegs(pegs):
    result = []
    for elem in pegs:
        result.append(Peg(elem[0], elem[1], elem[2]))
    return result

if __name__ == '__main__':
    num = 5
    examples = make_state_space()
    default_state_space = examples[num]
    a = Plotter('example_' + str(num) + '.png')
    a.plot(default_state_space)

