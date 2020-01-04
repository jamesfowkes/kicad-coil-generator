#!/usr/bin/env python3

""" coil-generator.py

Usage:
	coil-generator.py (--plot|--module=<name> [--desc=<desc>]) by-radius-and-turns <radius_mm> <turns_mm> <track_width_mm> [<angular_resolution>]
	coil-generator.py (--plot|--module=<name> [--desc=<desc>]) by-spacing-and-turns <spacing_mm> <turns_mm> <track_width_mm> [<angular_resolution>]
	coil-generator.py (--plot|--module=<name> [--desc=<desc>]) by-spacing-and-radius <spacing_mm> <radius_mm> <track_width_mm> [<angular_resolution>]

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

	track_width = measure_to_float(args["<track_width>"])
	angular_resolution = float(args.get("[<angular_resolution>]", 5))

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

	logging.info("Generating coil of radius {}mm, {} turns, spacing {}mm, track width {}mm)".format(radius, turns, track_spacing, track_width))

	coil = Coil.get_by_spacing_and_max_radius(track_spacing, radius, angular_resolution=angular_resolution)

	if args["--plot"]:
		plotter.plot_coil(coil, track_width)
	elif args["--module"]:
		module_data = {
			"name": args["--module"],
			"desc": args.get("--desc", "")
		}

		module = kicad.make_coil(coil, track_width, module_data)

		print(module)