import matplotlib.pyplot as plt
import matplotlib as mpl
import IPython
from state_space import StateSpace

peg_locations = {1: (0.0127, 0.0499),
				 2: (0.013, 0.0321),
				 3: (0.0124, 0.0146),
				 4: (0.0419, 0.0500),
				 5: (0.0417, 0.0319),
				 6: (0.0407, 0.0136),
				 7: (0.0596, 0.0420),
				 8: (0.0594, 0.0201),
				 9: (0.0768, 0.0566),
				 10: (0.0765, 0.0054),
				 11: (0.0932, 0.0414),
				 12: (0.0934, 0.0191),
				 }

class Plotter:
	def __init__(self):
		self.fig = plt.figure(figsize=(10,7)) # figure object
		plt.axis([0.0, 0.1, 0.0, 0.07]) # set the axis

	def plot_pegs(self):		
		fig = self.fig
		fig.gca().set_autoscale_on(False)
		for key in peg_locations:
			x,y = peg_locations[key]
			circle = plt.Circle((x,y), 0.0015, color='b')
			fig.gca().add_artist(circle)

		
	def plot_lines(self, lines):
		edges = []
		for line in lines:
			start = peg_locations[line[0]]
			end = peg_locations[line[1]]
			edges.append((start, end))
		lc = mpl.collections.LineCollection(edges, linewidths = 2, color="g")
		fig = plt.gcf()
		fig.gca().add_collection(lc)
		fig.savefig('test2.png')

	def get_coord_edges(self, edges):
		
		coord = ()
		for edge in edges:
			line = (start, end)
			IPython.embed()
			coord += (line,)
		return coord

if __name__ == '__main__':
    defaultStateSpace = StateSpace([[1, True, 0], [3, True, 0], [6, True, 0], 
        [8, True, 0], [7, True, 0], [5, False, 0], [4, True, 0]], [2], [9, 10, 11, 12])
    a = Plotter()
    a.plot_pegs()
    a.plot_lines(defaultStateSpace.getInOrderEdges())