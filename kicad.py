def get_kicad_segment(start_x, start_y, end_x, end_y, width, layer, net):
	return "(segment (start {:.4f} {:.4f}) (end {:.4f} {:.4f}) (width {:.4f}) (layer {:s}) (net {:s}))".format(
		start_x, start_y, end_x, end_y, width, layer, net)