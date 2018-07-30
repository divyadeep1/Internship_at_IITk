"""
	Takes as input a json file that lists the vertices and edges of a 
	graph (adjacency list representation) and outputs a 3d object in '.ply' format corresponding
	to the graph.
"""
from face_maker import face_maker
import numpy as np
import copy
import json
import sys
d = 10 #wall width

#vertices = [[-2.,0.],[-1.,0.],[0.,-1.],[0.,1.],[1.,0.],[2.,0.]]
#edges = [[1],[0,2,3],[4,1],[1,4],[2,5,3],[4]]

#vertices = [[-1,-1],[-1,1],[0,0],[1,-1],[1,1]]
#edges = [[2],[2],[0,3,4,1],[2],[2]]

def get_normals(p1, p2):
	#print("p1, p2: ",p1,p2)
	l_hat = (p2-p1)/np.linalg.norm(p2-p1)
	#print("l_hat: ",l_hat)
	r_hat_above = np.array([-l_hat[1],l_hat[0]])
	r_hat_below = -r_hat_above
	return r_hat_above, r_hat_below

def get_intersection_point(a1,a2,b1,b2):
	#find intersection pt. of two vectors
	#intersection will be near point p01 and p11 i.e. a2,b2
	p00 = np.array(a1)
	p01 = np.array(a2)
	p10 = np.array(b1)
	p11 = np.array(b2)
	rhs = p01-p10
#	print("p00,p01,p10,p11: ",p00,p01,p10,p11)
	a = p00[0] - p01[0]
	b = p11[0] - p10[0]
	c = p00[1] - p01[1]
	d = p11[1] - p10[1]
	A = np.array([[a,b],[c,d]])
	#print("A,rhs",A,rhs)
	try:
		res = np.linalg.solve(A,rhs)
	except Exception as e:
		print("p00,p01,p10,p11: ",p00,p01,p10,p11)
		print(str(e))
		if(p00[0]==p10[0] and p00[1]==p10[1] or p00[0]==p11[0] and p00[1]==p11[1]):
			return (p00[0],p00[1])
		elif(p01[0]==p10[0] and p01[1]==p10[1] or p01[0]==p11[0] and p01[1]==p11[1]):
			return (p01[0],p01[1])
		else:
			#s = "Problem is in this line: [{} {}], [{} {}]".format(p00,p01,p10,p11)
			#sys.exit(s)
			raise Exception("Two colinear lines encountered. continuing.")
	alpha = -res[0]
	#print(round(alpha*p00[0] + (1-alpha)*p01[0]) , round(alpha*p00[1] + (1-alpha)*p01[1]))
	#print("\n")
	return (round(alpha*p00[0] + (1-alpha)*p01[0]) , round(alpha*p00[1] + (1-alpha)*p01[1]))

def get_vectors(a, o):
	a = np.array(a)
	o = np.array(o)
	return a-o

def prnt(i,j):
	#print(i,j[0])
	return

def traverse_edges(new_edges, new_vertices, normals, func = prnt):
	edge_traversed = [False] * len(new_edges)
	for i, j in enumerate(new_edges):
		if not edge_traversed[i]:
			edge_traversed[i] = edge_traversed[j[0]] = True
			func(new_vertices[i], new_vertices[j[0]], normals[i])

def extrude_1d_walls_in_3d(file_name):
	#for k in range(len(vertices)):
	#	new_edges.append([])

	path_to_input_file = "./json/To extrude/"
	path_to_output_file = "./PLY source files/Generated/"
	_graph = "_graph"
	_ply = "_ply"
	dot_json = ".json"
	dot_ply = ".ply"

	with open(path_to_input_file+file_name+_graph+dot_json, 'r') as f:
		data = json.load(f)

	vertices = data['vertices']
	edges = data['edges']
	weights = data['weights']

	new_vertices = []
	new_edges = []
	normals = []

	double_indices = copy.deepcopy(edges)
	#print(edges == double_indices)
	for i,v in enumerate(vertices):
		vertices[i][0], vertices[i][1] = round(vertices[i][0]), round(vertices[i][1])
	for i in range(len(edges)):
		for j in edges[i]:
			##print("i, j: ", i, j)
			if double_indices[i][edges[i].index(j)] != j :
				continue
			
			p1 = np.array(vertices[i])
			p2 = np.array(vertices[j])
			normal_above, normal_below = get_normals(p1, p2)
			offset = d/2*normal_above#weights[i][edges[i].index(j)]*d/2*normal_above
			offset = (round(offset[0]), round(offset[1]))
			pts = np.array([p1,p2])
			if offset[0]*10%10!=0 or offset[1]*10%10!=0:
				print("offset: ", offset)
			if(np.nan not in offset):
				#Step 1.
				
				pts_high = pts+offset
				pts_low = pts-offset
				##print(pts_high[0])
				new_vertices.append(pts_high[0])
				new_vertices.append(pts_low[0])
				new_vertices.append(pts_high[1])
				new_vertices.append(pts_low[1])
				normals.append(normal_above.tolist())
				normals.append(normal_below.tolist())
				normals.append(normal_above.tolist())
				normals.append(normal_below.tolist())
				
				#if(vertices[i]==[484,217] or vertices[i]==[484,265]):
				print("new vertices for",vertices[i]," and",vertices[j]," are", new_vertices[-4:])
				
				#Step 2.
				n = len(new_vertices)
				p10, p00, p11, p01 = list(range(n - 4, n))
				new_edges += [[], [], [], []]
				new_edges[p10].append(p11)
				new_edges[p11].append(p10)
				new_edges[p00].append(p01)
				new_edges[p01].append(p00)


				if(vertices[i]==[484,217] or vertices[i]==[484,265]):
					v = [new_vertices[p10], new_vertices[p11], new_vertices[p00], new_vertices[p01]]
					print("New edges:")
					for _ in v:
						print(_)
				#Step 3.
				#print("i,j,edges[i]: ",i,j,edges[i])
#				#print("i,double_indices[i]: ",i,double_indices[i])
				double_indices[i][edges[i].index(j)] = (p10,p00)
				double_indices[j][edges[j].index(i)] = (p11,p01)
				
				if(vertices[i]==[484,217] or vertices[i]==[484,265]):
					print("Double indices[i]",double_indices[i])
				print("\n")

	#print(new_vertices)

#	print("1.")
#	for v in new_vertices:
#			if v[0]*10%10!=0 or v[1]*10%10!=0:
#				print(v)

	for i, v in enumerate(new_vertices):
		#if v[0]*10%10!=0 or v[1]*10%10!=0:
		new_vertices[i][0], new_vertices[i][1] = round(new_vertices[i][0]),round(new_vertices[i][1])

	#print(edges)
	add_triads_later = []
	s=-1
	for i in range(len(edges)):
		edges_connected_to_i = len(edges[i])
		if edges_connected_to_i > 1:
			if edges_connected_to_i>2 :
				#print("{} has > 2 edges.".format(edges[i]))
				print ("edges[i]: ", vertices[i],vertices[edges[i][0]],vertices[edges[i][1]],vertices[edges[i][2]])
				s = s+1
				add_triads_later.append([])
				exception_occured = False
				for j in range(edges_connected_to_i):
					try:
						a, o, b = edges[i][j], i, edges[i][(j+1)%edges_connected_to_i]
						vec_a = get_vectors(vertices[a],vertices[o])
						vec_b = get_vectors(vertices[b],vertices[o])
						a1, a2 = double_indices[a][edges[a].index(o)][0], double_indices[a][edges[a].index(o)][1]
						b1, b2 = double_indices[b][edges[b].index(o)][0], double_indices[b][edges[b].index(o)][1]
						vec_a1 = get_vectors(new_vertices[a1],vertices[o])
						vec_a2 = get_vectors(new_vertices[a2],vertices[o])
						vec_b1 = get_vectors(new_vertices[b1],vertices[o])
						vec_b2 = get_vectors(new_vertices[b2],vertices[o])
						#try:
						#print("points a, o, b: ",vertices[a],vertices[o],vertices[b])
		#				if a==87 and o==60 and b==59:
						print("In the loop.",new_vertices[a1],new_vertices[new_edges[a1][0]],new_vertices[b1],new_vertices[new_edges[b1][0]])
						if np.cross(vec_a,vec_a1) > 0 and np.cross(vec_b1,vec_b) > 0:
							#print("Case a1,b1")
							itrsec_pt = get_intersection_point(
															   new_vertices[a1],
															   new_vertices[new_edges[a1][0]],
															   new_vertices[b1],
															   new_vertices[new_edges[b1][0]]
															   
															)
							k , l = 0 , 0
						elif np.cross(vec_a,vec_a1) > 0 and np.cross(vec_b2,vec_b) > 0:
							#print("Case a1,b2")
							itrsec_pt = get_intersection_point(
															   new_vertices[a1],
															   new_vertices[new_edges[a1][0]],
															   new_vertices[b2],
															   new_vertices[new_edges[b2][0]]
															)
							k , l = 0 , 1
						elif np.cross(vec_a,vec_a2) > 0 and np.cross(vec_b1,vec_b) > 0:
							#print("Case a2,b1")
							itrsec_pt = get_intersection_point(
															   new_vertices[a2],
															   new_vertices[new_edges[a2][0]],
															   new_vertices[b1],
															   new_vertices[new_edges[b1][0]]
															)
							k , l = 1 , 0
						else:
							#print("Case a2,b2")
							itrsec_pt = get_intersection_point(
															   new_vertices[a2],
															   new_vertices[new_edges[a2][0]],
															   new_vertices[b2],
															   new_vertices[new_edges[b2][0]]
															)
							k , l = 1 , 1
						#if itrsec_pt[1]>550.:
							#print ("itrsec_pt, a, o, b, k, l:",itrsec_pt, a, o, b, k, l)
						new_vertices[double_indices[o][edges[o].index(a)][k]] = itrsec_pt
						new_vertices[double_indices[o][edges[o].index(b)][l]] = itrsec_pt
					except Exception as e:
						print("Exception: ",str(e))
						exception_occured = True
						continue
				if edges_connected_to_i>2 and not exception_occured:
					add_triads_later[s].append(itrsec_pt)
				print("\n\n")


#	print("2.")
#	for v in new_vertices:
#			if v[0]==489 or v[1]>550:
#				print(v)

	#print(add_triads_later)
	#print(type(np.array([1,2])))
	for i in range(len(new_vertices)):
		if (type(new_vertices[i])) == type(np.array([1,2])):
			#print(new_vertices[i])
			new_vertices[i] = new_vertices[i].tolist()
		else:
			new_vertices[i] = list(new_vertices[i])

	# Capping endings
	for i in range(len(edges)):
		edges_connected_to_i = len(edges[i])
		if edges_connected_to_i == 1:
			new_vertices.append(new_vertices[double_indices[i][0][0]])
			new_vertices.append(new_vertices[double_indices[i][0][1]])
			new_edges.append([len(new_vertices)-1])
			new_edges.append([len(new_vertices)-2])

			p00 = np.array(new_vertices[double_indices[i][0][0]])
			p01 = np.array(new_vertices[new_edges[double_indices[i][0][0]][0]])
			p10 = np.array(new_vertices[double_indices[i][0][1]])
			p11 = np.array(new_vertices[new_edges[double_indices[i][0][1]][0]])

			n1 = p00-p01 / np.linalg.norm(p00-p01)
			n2 = p10-p11 / np.linalg.norm(p10-p11)
			normals.append(n1.tolist())
			normals.append(n2.tolist())


	print("3.")
	for v in new_vertices:
			if v[0]>850 or v[1]>550:
				print(v)


	data = {"vertices" : new_vertices,
			"normals" : normals,
			"edges" : new_edges}

	##print(data)
	#with open("./vertices_edges_and_normals.json", 'w') as f:
	#	json.dump(data, f)
	#with open("./vertices_and_edges_2.json", 'w') as f:
	#	json.dump(data, f)

	#print("Number of edges after capping: ", len(new_edges))
	#for i in new_edges:
	#	#print(i)

	#print("\n\n")

	fm = face_maker(0.0,100.0)

	traverse_edges(new_edges, new_vertices, normals, fm.quad)

	#capping top and bottom
	edge_traversed = copy.deepcopy(edges)
	for i in range(len(edges)):
		for j in range(len(edges[i])):
			edge_traversed[i][j] = False

	#print(edges)
	for i in range(len(edges)):
		for j in range(len(edges[i])):
			if not edge_traversed[i][j]:
				#print("i,j: ",i,j)
				v00 = new_vertices[double_indices[i][j][0]]
				v01 = new_vertices[double_indices[i][j][1]]
				v10 = new_vertices[double_indices[edges[i][j]][edges[edges[i][j]].index(i)][0]]
				v11 = new_vertices[double_indices[edges[i][j]][edges[edges[i][j]].index(i)][1]]
				fm.top_bottom_quads(v00,v01,v10,v11)
				edge_traversed[i][j] = True
				edge_traversed[edges[i][j]][edges[edges[i][j]].index(i)] = True

	#filling polygonal shapes formed in between the capped quads
	if(len(add_triads_later) > 0):
		fm.add_triads(add_triads_later)
	##print(add_triads_later)

	#fm.generate_ply(path_to_ply+file+"_ply.ply")
	fm.generate_ply(path_to_output_file+file_name+_ply+dot_ply)

if __name__ == "__main__":
#	extrude_1d_walls_in_3d("ada290-lvl1-li-bl-lg_1.png")
	extrude_1d_walls_in_3d("final_data_s")
