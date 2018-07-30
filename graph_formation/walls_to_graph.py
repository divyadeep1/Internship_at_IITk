"""
	Converts walls, provided in json format, to a graph
	(adjacency list representation).
"""

import json

def make_graph_from_1d_walls(file_name):
	path_to_input_file = "./json/Make graph/"
	path_to_output_file = "./json/To extrude/"
	_walls = "_walls"
	dot_json = ".json"
	
	with open(path_to_input_file+file_name+_walls+dot_json, 'r') as f:
		data = json.load(f)

	# Diamond shape's data for testing purpose
	#data = [[0,-2,-1,0,0,1],#                  /\
	#		[1,-1,0,0,1,1],  #shape --->   ____/  \____
	#		[2,-1,0,0,-1,1], #                 \  /
	#		[3,0,1,1,0,1],   #                  \/
	#		[4,0,1,-1,0,1],
	#		[5,1,2,0,0,1]
	#		]

	vertices = []
	wts = []
	weights = []
	edges_old = []
	edges_new = []

	for d in data:
		_,x1,x2,y1,y2,w = d
		p1 = [x1,y1]
		p2 = [x2,y2]
		if p1!=p2:
			if w > 0.0:
				if p1 not in vertices:
					vertices.append(p1)
				if p2 not in vertices:
					vertices.append(p2)
				edges_old.append([vertices.index(p1), vertices.index(p2),w])
				#wts.append(w)

	#print("Edges: ", edges_old)

	edges_new = [[] for i in range(len(vertices))] ##!!NOTE!!- a = [[]]*4 creates an element with 3 more references to it!!!
	weights = [[] for i in range(len(vertices))]
	for i,edge in enumerate(edges_old):
		p1i, p2i, w = edge #'i' stands for index
		#print (p1i,p2i)
		#print("edges_new[p1i]:",edges_new[p1i])
		if p2i not in edges_new[p1i]:
			weights[p1i].append(w)
			weights[p2i].append(w)
			edges_new[p1i].append(p2i)
			edges_new[p2i].append(p1i)

	data_out = {"vertices" : vertices, 
				"weights" : weights,
				"edges" : edges_new}
			
#	for v in vertices:
#		if v[0]>500 or v[1]>500:
#			print(v)
	with open(path_to_output_file+file_name+"_graph"+dot_json, 'w') as f:
		json.dump(data_out,f)

if __name__ == "__main__":
	#make_graph_from_1d_walls("ada290-lvl1-li-bl-lg_1.png")
	make_graph_from_1d_walls("final_data_s")
