import logging

import matplotlib

matplotlib.use('TkAgg')

import matplotlib.pyplot as plt

def get_module_logger():
	return logging.getLogger(__name__)

def plot_coil(coil, linewidth_mm):
	linewidth_points = linewidth_mm * 72 / 25.4
	
	plt.plot([v.start.x for v in coil], [v.start.y for v in coil], linestyle='solid', linewidth=linewidth_mm)
	plt.axis('equal')
	plt.grid(True)
	plt.show()
