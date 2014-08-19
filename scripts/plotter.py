import matplotlib.pyplot as plt
import matplotlib as mpl
import IPython

peg_locations = {1: (0.0127, 0.0499),
				 2: (0.0121, 0.0321),
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
			circle = plt.Circle((x,y), 0.003, color='b')
			fig.gca().add_artist(circle)

		

	def plot_lines(self, lines):
		lc = mpl.collections.LineCollection(edges, linewidths=2)
		fig = plt.gcf()
		fig.gca().add_collection(lc)
		fig.savefig('test.png')




if __name__ == '__main__':
	a = Plotter()
	a.plot_pegs()
	a.plot_lines([((0.0127,0.0499), (0.0121,0.0321))])