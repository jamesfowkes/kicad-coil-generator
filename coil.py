import math
import numpy as np
from collections import namedtuple

def get_required_radius_for_spacing(spacing):
	return spacing / (2 * np.pi)

def get_turns_at_coil_y(y, r):
	return y / (2*np.pi*r)

Point = namedtuple("Point", ["x", "y"])

class Vector(namedtuple("Vector", ["start", "end"])):
	
	__slots__ = ()

	@property
	def midpoint(self):
		midx = (self.start.x + self.end.x) / 2
		midy = (self.start.y + self.end.y) / 2
		return Point(midx, midy)

	@property
	def dx(self):
		return self.end.x - self.start.x
	
	@property
	def dy(self):
		return self.end.y - self.start.y

	@property
	def length(self):
		return math.hypot(self.dx, self.dy)

	@property
	def angle(self):
		return math.degrees(math.atan2(self.dy, self.dx))

class Coil(namedtuple("Coil", ["x", "y", "a"])):

	__slots__ = ()

	@classmethod
	def get_by_radius_and_turns(cls, r, turns, angular_resolution=1):
		thetas = np.arange(0, 2*np.pi*turns, np.deg2rad(angular_resolution))
		xs = [r * (np.cos(theta) + theta * np.sin(theta)) for theta in thetas]
		ys = [r * (np.sin(theta) - theta * np.cos(theta)) for theta in thetas]

		iterator = zip(xs, ys)
		end = Point(*next(iterator))

		vectors = []

		while True:
			try:
				start = end
				end = Point(*next(iterator))

				vectors.append(Vector(start, end))

			except StopIteration:
				break; 

		return vectors

	@classmethod
	def get_by_spacing_and_turns(cls, spacing, turns, angular_resolution=1):
		r = get_required_radius_for_spacing(spacing)
		return cls.get_by_radius_and_turns(r, turns, angular_resolution)

	@classmethod
	def get_by_spacing_and_max_radius(cls, spacing, max_r, angular_resolution=1):
		r = get_required_radius_for_spacing(spacing)
		turns = get_turns_at_coil_y(max_r, r)
		return cls.get_by_radius_and_turns(r, turns, angular_resolution)
