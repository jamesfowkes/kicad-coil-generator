START_MODULE_FORMAT = """\
(module {name} (layer {layer}) (tedit 0)
  (descr {desc})
  (attr smd)\
"""

END_MODULE_FORMAT = """
)
"""

PAD_FORMAT = """\
  (pad {name} {type} {shape} (at {x} {y} {a}) (size {w} {h}) (layers {layers}))\
"""

def circular_pad(x, y, diameter, top_layer=True):
	params = {
		"name": "COIL",
		"type": "smd",
		"shape": "circle",
		"x": x,
		"y": y,
		"a": 0,
		"w": diameter,
		"h": diameter,
		"layers": "F.Cu F.Paste F.Mask" if top_layer else "B.Cu B.Paste B.Mask"
	}

	return PAD_FORMAT.format(**params)

def rect_pad(x, y, w, h, a, top_layer=True):
	params = {
		"name": "COIL",
		"type": "smd",
		"shape": "rect",
		"x": x,
		"y": y,
		"a": a,
		"w": w,
		"h": h,
		"layers": "F.Cu F.Paste F.Mask" if top_layer else "B.Cu B.Paste B.Mask"
	}

	return PAD_FORMAT.format(**params)

def link_pad(x, y, length, angle, track_width, top_layer=True):

	return rect_pad(x, y, track_width, length, angle, top_layer)

def make_coil(coil, track_width, module_data, top_layer=True):

	#iterator = zip(coil.x, coil.y, coil.a)
	
	#end = Point(*next(iterator))
	module_strings = []

	module_strings.append(START_MODULE_FORMAT.format(name=module_data["name"], layer="F.Cu" if top_layer else "B.Cu", desc=module_data["desc"]))

	#while True:
#
	#	try:
	#		start = end
	#		end = Point(*next(iterator))
#
	#		start_pad = circular_pad(start.x, start.y, track_width, top_layer)
	#		module_strings.append(start_pad)
	#		link = link_pad(start, end, track_width, top_layer)
	#		module_strings.append(link)
#
	#	except StopIteration:
	#		break

	for vect in coil:
		start_pad = circular_pad(vect.start.x, vect.start.y, track_width, top_layer)
		module_strings.append(start_pad)
		link = link_pad(vect.midpoint.x, vect.midpoint.y, vect.length, 90-vect.angle, track_width, top_layer)
		module_strings.append(link)

	module_strings.append(END_MODULE_FORMAT)

	return '\n'.join(module_strings)