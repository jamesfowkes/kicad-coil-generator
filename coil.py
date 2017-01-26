import numpy as np
from collections import namedtuple

def get_required_radius_for_spacing(spacing):
	return spacing / (2 * np.pi)

def get_turns_at_coil_y(y, r):
	return y / (2*np.pi*r)

class Coil(namedtuple("Coil", ["x", "y"])):

	__slots__ = ()

	@classmethod
	def get_by_radius_and_turns(cls, r, turns):
		thetas = np.arange(0, 2*np.pi*turns, np.deg2rad(0.1))
		x = [r * (np.cos(theta) + theta * np.sin(theta)) for theta in thetas]
		y = [r * (np.sin(theta) - theta * np.cos(theta)) for theta in thetas]
		return cls(x, y)

	@classmethod
	def get_by_spacing_and_turns(cls, spacing, turns):
		r = get_required_radius_for_spacing(spacing)
		return cls.get_by_radius_and_turns(r, turns)

	@classmethod
	def get_by_spacing_and_max_radius(cls, spacing, max_r):
		r = get_required_radius_for_spacing(spacing)
		turns = get_turns_at_coil_y(max_r, r)
		return cls.get_by_radius_and_turns(r, turns)
