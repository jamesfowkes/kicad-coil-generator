import matplotlib

matplotlib.use('TkAgg')

import matplotlib.pyplot as plt

def plot_coil(x, y, fmt='ro'):
	plt.plot(x, y, fmt)
	plt.axis('equal')
	plt.show()