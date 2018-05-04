import numpy

def generate_vertices(vertices, surfaces):
	object_vertices = []
	for s in surface:
		for v in s:
			object_vertices.append(v)
	return object_vertices

