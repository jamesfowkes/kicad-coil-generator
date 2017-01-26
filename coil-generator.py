#!/usr/bin/env python3

""" coil-generator.py

Usage:
	coil-generator.py by-radius-and-turns <radius> <turns> <track_width> (--plot|--module)
	coil-generator.py by-spacing-and-turns <spacing> <turns> <track_width> (--plot|--module)
	coil-generator.py by-spacing-and-radius <spacing> <radius> <track_width> (--plot|--module)

"""
import plotter
import kicad
import logging
import docopt
from coil import Coil

def measure_to_float(measure):
	if measure.endswith("mm"):
		return float(measure[:-2])

	if measure.endswith("in"):
		return float(measure[:-2]) * 25.4

	if measure.endswith("mil"):
		return float(measure[:-3]) * 25.4 / 1000.0

	return float(measure)

if __name__ == "__main__":

	args = docopt.docopt(__doc__)

	logging.basicConfig(level=logging.INFO)
	net = 'coil'

	start_x = 100
	start_y = 100

	segment_length = 1

	track_width = args["<track_width>"]

	layer = "F.Cu"

	if args["by-radius-and-turns"]:
		radius = measure_to_float(args["<radius>"])
		turns = float(args["<turns>"])
		track_spacing = radius / turns

	elif args["by-spacing-and-turns"]:
		track_spacing = measure_to_float(args["<spacing>"])
		turns = float(args["<turns>"])
		radius = track_spacing * turns

	elif args["by-spacing-and-radius"]:
		track_spacing = measure_to_float(args["<spacing>"])
		radius = measure_to_float(args["<radius>"])

	logging.info("Generating coil of radius {}mm, {} turns (spacing {}mm)".format(radius, turns, track_spacing))
	
	coil = Coil.get_by_spacing_and_max_radius(track_spacing, radius)

	plotter.plot_coil(coil.x, coil.y)
