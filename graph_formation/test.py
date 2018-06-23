"""
This file is used to fuse :
	1.Parallel lines that have both their end points close to each other.
	2.Points that are within certain range of each other.
And to split intersecting lines into a different set of non-intersecting lines.

Desired -   1. To merge overlapping lines into single lines.
			2. Handling parallel lines that don't have both end points close to each other.
			3. Possibly change the representation of lines to [[x1,y1],[x2,y2],weight]
			4. Change the method of calculation intersection point from equation of line method to vector method.

!!Note!!: The format of representation of a line is -> [line-number, x1, x2, y1, y2, weight]
Where:
	x1 = x-coordinate of first end point of the line.
	x2 = x-coordinate of second end point of the line.
	y1 = y-coordinate of first end point of the line.
	y2 = y-coordinate of second end point of the line. 
"""

import json
import math
import numpy as np
import sys
import copy

#constants
epsilon = 8 #Every point within this pixel range will be considered a single point
epsilon2 = 8
max_dist_between_two_nodes = 8
infinity = 99999999
eps = 0
eps3 = 5
wall_number = None
min_dist_to_be_called_a_line = 13

def parallel_and_close(line_one, line_two):
	"""Checks if 2 lines are parallel and close to one another."""
	d1 = math.sqrt((line_one[1]-line_two[1])**2 + (line_one[3]-line_two[3])**2) # sqrt((x11 - x21)**2 + (y11 - y21))
	d2 = math.sqrt((line_one[2]-line_two[2])**2 + (line_one[4]-line_two[4])**2) # sqrt((x12 - x22)**2 + (y12 - y22))
	d3 = math.sqrt((line_one[1]-line_two[2])**2 + (line_one[3]-line_two[4])**2) # sqrt((x11 - x21)**2 + (y11 - y21))
	d4 = math.sqrt((line_one[2]-line_two[1])**2 + (line_one[4]-line_two[3])**2) # sqrt((x11 - x21)**2 + (y11 - y21))
	
	if abs(d1-d2) < epsilon and (d1+d2)/2 < epsilon2:
		return True
	elif abs(d3-d4) < epsilon and (d3+d4)/2 < epsilon2:
		return True
	else:
		return False


def fuse_lines(line_one, line_two):
	"""Fuses two parallel lines into a single wall."""
	global wall_number
	wall_number += 1
	if abs(math.sqrt((line_one[1]-line_two[1])**2 + (line_one[3]-line_two[3])**2) -
		math.sqrt((line_one[2]-line_two[2])**2 + (line_one[4]-line_two[4])**2)) < epsilon:
		weight = round((math.sqrt((line_one[1]-line_two[1])**2 + (line_one[3]-line_two[3])**2) + 
		math.sqrt((line_one[2]-line_two[2])**2 + (line_one[4]-line_two[4])**2) )/2)
		return  [
				wall_number, 
				round((line_one[1]+line_two[1])/2),
				round((line_one[2]+line_two[2])/2),
				round((line_one[3]+line_two[3])/2),
				round((line_one[4]+line_two[4])/2),
				weight
				]
	else:
		weight = round((math.sqrt((line_one[1]-line_two[2])**2 + (line_one[3]-line_two[4])**2) + 
		math.sqrt((line_one[2]-line_two[1])**2 + (line_one[4]-line_two[3])**2))/2)
		return [
				wall_number, 
				round((line_one[1]+line_two[2])/2),
				round((line_one[2]+line_two[1])/2),
				round((line_one[3]+line_two[4])/2),
				round((line_one[4]+line_two[3])/2),
				weight
			   ]


#def check_angled_and_fuse(line_one, line_two):
#	d1 = math.sqrt((line_one[1]-line_two[1])**2 + (line_one[3]-line_two[3])**2) # sqrt((x11 - x21)**2 + (y11 - y21))
#	d2 = math.sqrt((line_one[2]-line_two[2])**2 + (line_one[4]-line_two[4])**2) # sqrt((x12 - x22)**2 + (y12 - y22))
#	d3 = math.sqrt((line_one[1]-line_two[2])**2 + (line_one[3]-line_two[4])**2) # sqrt((x11 - x21)**2 + (y11 - y21))
#	d4 = math.sqrt((line_one[2]-line_two[1])**2 + (line_one[4]-line_two[3])**2) # sqrt((x11 - x21)**2 + (y11 - y21))
#	if (d1 < max_dist_between_two_nodes and d1>0):
#		###print(line_one, line_two, "fused to ")
#		line_one = [line_one[0], round((line_one[1]+line_two[1])/2), line_one[2], round((line_one[3]+line_two[3])/2), line_one[4], line_one[5]] 
#		line_two = [line_two[0], round((line_one[1]+line_two[1])/2), line_two[2], round((line_one[3]+line_two[3])/2), line_two[4], line_two[5]]
#		###print(line_one, line_two)
#		return (line_one,line_two, True)
#	elif (d2 < max_dist_between_two_nodes and d2>0):
##		###print(line_one, line_two, "fused to ")
#		line_one = [line_one[0], line_one[1], round((line_one[2]+line_two[2])/2), line_one[3], round((line_one[4]+line_two[4])/2), line_one[5]]
#		line_two = [line_two[0], line_two[1], round((line_one[2]+line_two[2])/2), line_two[3], round((line_one[4]+line_two[4])/2), line_two[5]]
##		###print(line_one, line_two)
#		return (line_one, line_two, True)
#	elif (d3 < max_dist_between_two_nodes and d3>0):
##		###print(line_one, line_two, "fused to ")
#		line_one = [line_one[0], round((line_one[1]+line_two[2])/2), line_one[2], round((line_one[3]+line_two[4])/2), line_one[4], line_one[5]]
#		line_two = [line_two[0], line_two[1], round((line_one[1]+line_two[2])/2), line_two[3], round((line_one[3]+line_two[4])/2), line_two[5]]
##		###print(line_one, line_two)
#		return (line_one, line_two,True)
#	elif (d4 < max_dist_between_two_nodes and d4>0):
##		###print(line_one, line_two, "fused to ")
#		line_one = [line_one[0], line_one[1], round((line_one[2]+line_two[1])/2), line_one[3], round((line_one[4]+line_two[3])/2), line_one[5]]
#		line_two = [line_two[0], round((line_one[2]+line_two[1])/2), line_two[2], round((line_one[4]+line_two[3])/2), line_two[4], line_two[5]]
##		###print(line_one, line_two)
#		return (line_one, line_two, True)
#	else:
#		return (line_one, line_two, False)

def line_intersection(line1, line2):
	line1 = ([line1[1], line1[3]], [line1[2], line1[4]])
	line2 = ([line2[1], line2[3]], [line2[2], line2[4]])
	xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
	ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

	def det(a, b):
		return a[0] * b[1] - a[1] * b[0]

	div = det(xdiff, ydiff)
	if div == 0:
		return (np.nan, np.nan)

	d = (det(*line1), det(*line2))
	x = det(d, xdiff) / div
	y = det(d, ydiff) / div
	return (x, y)

def check_angled(lines, i, j, current_set_close_to_point_0, current_set_close_to_point_1):
	line_one = lines[i]
	line_two = lines[j]
	x00, x01, y00, y01 = line_one[1], line_one[2], line_one[3], line_one[4]
	x10, x11, y10, y11 = line_two[1], line_two[2], line_two[3], line_two[4]

	d00 = math.sqrt((x00-x10)**2 + (y00-y10)**2)
	d01 = math.sqrt((x00-x11)**2 + (y00-y11)**2)
	d10 = math.sqrt((x01-x10)**2 + (y01-y10)**2)
	d11 = math.sqrt((x01-x11)**2 + (y01-y11)**2)
	
	##print("p00: ",x00,y00)
	##print("p01: ",x01,y01)
	##print("p00: ",x10,y10)
	##print("p01: ",x11,y11)
	
	##print("d00,d01,d10,d11: ",d00,d01,d10,d11)
	
	if d00 < max_dist_between_two_nodes and d00 > 0:
		#print("d00")
		current_set_close_to_point_0.append([j,0])
	elif d01 < max_dist_between_two_nodes and d01 > 0:
		#print("d01")
		current_set_close_to_point_0.append([j,1])
	elif d10 < max_dist_between_two_nodes and d10 > 0:
		#print("d10")
		current_set_close_to_point_1.append([j,0])
	elif d11 < max_dist_between_two_nodes and d11 > 0:
		#print("d11")
		current_set_close_to_point_1.append([j,1])

def fuse_angled(lines, i, current_set_close_to_point_0, current_set_close_to_point_1):
	new_lines = copy.deepcopy(lines)
	intrsctn_pnt_0 = []
	intrsctn_pnt_1 = []
	line_one = new_lines[i]
	#print("old lines: ",new_lines[i])
	#if len(current_set_close_to_point_0)>0:
		#print("current_set_close_to_point_0:", current_set_close_to_point_0)
		#print(lines[current_set_close_to_point_0[0][0]], lines[i])
	#if len(current_set_close_to_point_1)>0:
		#print("current_set_close_to_point_1: ", current_set_close_to_point_1)
		#print(lines[current_set_close_to_point_1[0][0]], lines[i])

	for j, pt in current_set_close_to_point_0:
		line_two = new_lines[j]
		ip = line_intersection(line_one, line_two)
		#print(ip)
		if ip == (np.nan, np.nan):
			current_set_close_to_point_0.pop(current_set_close_to_point_0.index([j,pt]))
			continue
		else:
			intrsctn_pnt_0.append(ip)
	new_pt = None
	if len(intrsctn_pnt_0)>0:
		new_pt = (np.average(np.array(intrsctn_pnt_0)[:,0]), np.average(np.array(intrsctn_pnt_0)[:,1]))
		new_lines[i][1], new_lines[i][3] = new_pt
		for j, pt in current_set_close_to_point_0:
			new_lines[j][pt+1], new_lines[j][pt+3] = new_pt
		#print(intrsctn_pnt_0)
	#print("new point: ",new_pt)

	for j, pt in current_set_close_to_point_1:
		line_two = lines[j]
		ip = line_intersection(line_one, line_two)
		#print("ip for {} and {} is {}".format(line_one, line_two,ip))
		if ip == (np.nan, np.nan):
			current_set_close_to_point_1.pop(current_set_close_to_point_1.index([j,pt]))
			continue
		else:
			intrsctn_pnt_1.append(ip)
	if len(intrsctn_pnt_1)>0:
		new_pt = (np.average(np.array(intrsctn_pnt_1)[:,0]), np.average(np.array(intrsctn_pnt_1)[:,1]))
		new_lines[i][2], new_lines[i][4] = new_pt
		for j, pt in current_set_close_to_point_1:
			new_lines[j][pt+1], new_lines[j][pt+3] = new_pt
		print(intrsctn_pnt_1)
	#print("new point: ",new_pt)
	print(new_lines[i]==lines[i])
	return new_lines

def make_slightly_slanting_lines_straight(line):
	###print ("Before : ", line)
	###print(eps3)
	if(abs(line[1]-line[2]) < eps3):
		line[1] = line[2]
	if(abs(line[3]-line[4]) < eps3):
		line[3] = line[4]
	###print ("After : ", line)
	return line

def get_line_eqns(line_one, line_two):
	x00, x01, y00, y01 = line_one[1], line_one[2], line_one[3], line_one[4]
	x10, x11, y10, y11 = line_two[1], line_two[2], line_two[3], line_two[4]
	if (x01!=x00):
		m0 = ((y01-y00)/(x01-x00))
	else:
		m0 = infinity
	if (x11!=x10):
		m1 = ((y11-y10)/(x11-x10))
	else:
		m1 = infinity
	#Parallel lines:
	#if m1==m0:
	#	#print("Lines are parallel")
		#return(a1,m1,c1,a2,m2,c2)
	#Non-parallel lines with equations ay-mx = c:
	if m0<infinity:
		c0 = y01-m0*x01
		a0 = 1
		m0 = -m0
	else:
		c0 = x01
		a0 = 0
		m0 = 1
	if m1<infinity:
		c1 = y11-m1*x11
		a1 = 1
		m1 = -m1
	else:
		c1 = x11
		a1 = 0
		m1 = 1
	return(a0,m0,c0,a1,m1,c1)


def get_intersection_point(line_one, line_two):
	x00, x01, y00, y01 = line_one[1], line_one[2], line_one[3], line_one[4]
	x10, x11, y10, y11 = line_two[1], line_two[2], line_two[3], line_two[4]
	
	a0,m0,c0,a1,m1,c1 = get_line_eqns(line_one, line_two)
	if m1==m0: #Lines are parallel
		return None
	
	A = np.array([[a1,m1],[a0,m0]],dtype=np.int32)
	C = np.array([c1,c0], dtype=np.int32)
	#try:
	intersection_point = np.linalg.solve(A,C) # result is (y,x) and not (x,y)
	x3 = round(intersection_point[1])
	y3 = round(intersection_point[0])
	if (x3-eps>min(x00,x01) and max(x00,x01)-eps>x3 and y3-eps>min(y00,y01) and max(y00,y01)-eps>y3) and (x3-eps>min(x10,x11) and max(x10,x11)-eps>x3 and y3-eps>min(y10,y11) and max(y10,y11)-eps>y3):
		####print(intersection_point)
		return(x3,y3)
	else:
		####print("Lines intersect but not in the required range.")
		return None
	#except:
	#	return None

def split_intersecting_lines(line_one, line_two, intersection_point):
	global wall_number
	_, x00, x01, y00, y01, w0 = line_one
	_, x10, x11, y10, y11, w1 = line_two
	x3 = intersection_point[0]
	y3 = intersection_point[1]
	new_l1 = [wall_number+1,x00,x3,y00,y3,w0]
	new_l2 = [wall_number+2,x01,x3,y01,y3,w0]
	new_l3 = [wall_number+3,x10,x3,y10,y3,w1]
	new_l4 = [wall_number+4,x11,x3,y11,y3,w1]
	wall_number += 4
	return (new_l1, new_l2, new_l3, new_l4)


def points_away(point00, point01, point10, point11, intersection_point):
	if (
		(point00[0]==intersection_point[0] and point00[1]==intersection_point[1]) or
		(point01[0]==intersection_point[0] and point01[1]==intersection_point[1]) or
		(point10[0]==intersection_point[0] and point10[1]==intersection_point[1]) or
		(point11[0]==intersection_point[0] and point11[1]==intersection_point[1])
		):
		return False
	return True


def union_of_overlapping_lines(line_one, line_two):
	_, x00, x01, y00, y01, w0 = line_one
	_, x10, x11, y10, y11, w1 = line_two
	a1,m1,c1,a2,m2,c2 = get_line_eqns(line_one, line_two)
	m1 = -m1
	m2 = -m2
	if a1==a2 and m1==m2 and c1==c2:
		##print("{}y = {}x + {}".format(a1,m1,c1))
	#3 cases of same line are possible:
	#1. one line is completely inside the boundries of another.
	#2. the two lines overlap.
	#3. they are separate.
		if m1>=0:
			x_list = [x00, x01,x10, x11]
			y_list = [y00, y01,y10, y11]
			x_list.sort(), y_list.sort()
			##print(x_list, y_list)
			x1,x2,x3,x4 = x_list
			y1,y2,y3,y4 = y_list
			if x1 in line_one[1:3] and x2 in line_two[1:3] and x3 in line_two[1:3] and x4 in line_one[1:3]:
				##print("YES")
				return _,x1,x4,y1,y4,w0
			elif x1 in line_two[1:3] and x2 in line_one[1:3] and x3 in line_one[1:3] and x4 in line_two[1:3]:
				##print("YES")
				return _,x1,x4,y1,y4,w1
		
			if x1 in line_one[1:3] and x2 in line_two[1:3] and x3 in line_one[1:3] and x4 in line_two[1:3]:
				##print("YES")
				return _,x1,x4,y1,y4,(w1+w0)/2
			elif x1 in line_two[1:3] and x2 in line_one[1:3] and x3 in line_two[1:3] and x4 in line_one[1:3]:
				##print("YES")
				return _,x1,x4,y1,y4,(w1+w0)/2
		
			if x1 in line_one[1:3] and x2 in line_one[1:3] and x3 in line_two[1:3] and x4 in line_two[1:3]:
				##print("NO")
				return None
			elif x1 in line_two[1:3] and x2 in line_two[1:3] and x3 in line_one[1:3] and x4 in line_one[1:3]:
				##print("NO")
				return None
		elif(a1==0 and m1==-1):
			x_list = [x00, x01,x10, x11]
			y_list = [y00, y01,y10, y11]
			x_list.sort(), y_list.sort()
			##print(x_list, y_list)
			x1,x2,x3,x4 = x_list
			y1,y2,y3,y4 = y_list
			if y1 in line_one[3:5] and y2 in line_two[3:5] and y3 in line_two[3:5] and y4 in line_one[3:5]:
				##print("YES")
				return _,x1,x4,y1,y4,w0
			elif y1 in line_two[3:5] and y2 in line_one[3:5] and y3 in line_one[3:5] and y4 in line_two[3:5]:
				##print("YES")
				return _,x1,x4,y1,y4,w1
	
			if y1 in line_one[3:5] and y2 in line_two[3:5] and y3 in line_one[3:5] and y4 in line_two[3:5]:
				##print("YES")
				return _,x1,x4,y1,y4,(w1+w0)/2
			elif y1 in line_two[3:5] and y2 in line_one[3:5] and y3 in line_two[3:5] and y4 in line_one[3:5]:
				##print("YES")
				return _,x1,x4,y1,y4,(w1+w0)/2
	
			if y1 in line_one[3:5] and y2 in line_one[3:5] and y3 in line_two[3:5] and y4 in line_two[3:5]:
				print("NO")
				return None
			elif y1 in line_two[3:5] and y2 in line_two[3:5] and y3 in line_one[3:5] and y4 in line_one[3:5]:
				print("NO")
				return None
		else:
			x_list = [x00, x01,x10, x11]
			y_list = [y00, y01,y10, y11]
			x_list.sort(), y_list.sort(reverse=True)
			x1,x2,x3,x4 = x_list
			y1,y2,y3,y4 = y_list
			if x1 in line_one[1:3] and x2 in line_two[1:3] and x3 in line_two[1:3] and x4 in line_one[1:3]:
				##print("YES")
				return _,x1,x4,y1,y4,w0
			elif x1 in line_two[1:3] and x2 in line_one[1:3] and x3 in line_one[1:3] and x4 in line_two[1:3]:
				##print("YES")
				return _,x1,x4,y1,y4,w1
		
			if x1 in line_one[1:3] and x2 in line_two[1:3] and x3 in line_one[1:3] and x4 in line_two[1:3]:
				##print("YES")
				return _,x1,x4,y1,y4,(w1+w0)/2
			elif x1 in line_two[1:3] and x2 in line_one[1:3] and x3 in line_two[1:3] and x4 in line_one[1:3]:
				##print("YES")
				return _,x1,x4,y1,y4,(w1+w0)/2
		
			if x1 in line_one[1:3] and x2 in line_one[1:3] and x3 in line_two[1:3] and x4 in line_two[1:3]:
				##print("NO")
				return None
			elif x1 in line_two[1:3] and x2 in line_two[1:3] and x3 in line_one[1:3] and x4 in line_one[1:3]:
				##print("NO")
				return None
	else:
		##print("NOT even parallel")
		return None

def too_close(line):
	if math.sqrt((line[2]-line[1])**2 + (line[4]-line[3])**2) < min_dist_to_be_called_a_line:
		return True
	##print("Snap! one line gone!")
	return False


def turn_lines_to_1d_walls(file_name):
	path_to_input_file = "./json/Make walls/"
	path_to_output_file = "./json/Make graph/"
	dot_json = ".json"

	global wall_number

	with open(file_name+dot_json, 'r') as f:
		lines = json.load(f)

	#for line in lines:
	#	line.append(0.3) #Weight of each line

	wall_number = len(lines)-1

	###print ("Number of lines: ",len(lines))

	###print("Pass 0.5: Making slightly slanting lines straight:")
	for i in range(len(lines)):
		lines[i] = make_slightly_slanting_lines_straight(lines[i])

	while i < (len(lines)):
		##print(lines[i], too_close(lines[i]))
		if too_close(lines[i]):
			#print("Before: ",len(lines))
			lines.pop(i)
			#print("After: ",len(lines))
		else:
			i+=1

	##print("Pass 1: To fuse parallel lines")
#	while True:
#		changes_made = False
#		i = 0
#		while i<len(lines)-1:
#			lines_fused = False
#			for j in range(i+1,len(lines)):
#				if parallel_and_close(lines[i], lines[j]):
#					wall_points = fuse_lines(lines[i],lines[j])
#					lines.append(wall_points)
#					####print(lines[i], " and ", lines[j], "fused, new line: ",wall_points, "\n")
#					lines = lines[0:i] + lines[i+1:j] + lines[j+1:]
#					lines_fused = True
#					changes_made = True
#					break
#			if not lines_fused:
#				i += 1
#		if not changes_made:
#			break

	while True:
		changes_made = False
		i=0
		while i<len(lines)-1:
			lines_fused = False
			j = i+1
			while j < len(lines):
				if union_of_overlapping_lines(lines[i], lines[j]) is not None:
					#print ("merging lines {},{}".format(lines[i],lines[j]))
					lines.append(list(union_of_overlapping_lines(lines[i], lines[j])))
					lines = lines[0:i] + lines[i+1:j] + lines[j+1:]
					lines_fused = True
					changes_made = True
				j += 1
			if not lines_fused:
				i += 1
		if not changes_made:
			break
#	with open(path_to_output_file+file_name+"_walls_overlap"+dot_json, 'w') as f:
#		json.dump(lines, f)
	
	while i < (len(lines)):
	##print(lines[i], too_close(lines[i]))
		if too_close(lines[i]):
			#print("Before: ",len(lines))
			lines.pop(i)
			#print("After: ",len(lines))
		else:
			i+=1


	###print("Pass 1.5: Making slightly slanting lines straight:")
	for i in range(len(lines)):
		lines[i] = make_slightly_slanting_lines_straight(lines[i])

	###print("Number of lines after first pass:", len(lines))

	###print("Pass 2: To fuse end points of angled lines")
#	while True:
#		changes_made = False
#		i = 0
#		while i < len(lines)-1:
#			for j in range(i+1,len(lines)):
#				lines[i], lines[j], changed = check_angled_and_fuse(lines[i], lines[j])
#				if changed and not changes_made:
#					changes_made = True
#			i += 1
#		if not changes_made:
#			break

	i = 0
	while i < len(lines)-1:
		current_set_close_to_point_0 = []
		current_set_close_to_point_1 = []
		for j in range(i+1,len(lines)):
			##print("line_one, line_two: ", i, j)
			check_angled(lines, i, j,current_set_close_to_point_0, current_set_close_to_point_1)
		lines = fuse_angled(lines, i, current_set_close_to_point_0, current_set_close_to_point_1)
		i += 1

#	with open(path_to_output_file+file_name+"_walls_fuse"+dot_json, 'w') as f:
#		json.dump(lines, f)

	while i < (len(lines)):
		##print(lines[i], too_close(lines[i]))
		if too_close(lines[i]):
			#print("Before: ",len(lines))
			lines.pop(i)
			#print("After: ",len(lines))
		else:
			i+=1
		
	###print("Pass 2.5: Making slightly slanting lines straight:")
	for i in range(len(lines)):
		lines[i] = make_slightly_slanting_lines_straight(lines[i])

	###print("Number of lines after second pass:", len(lines))

	####print (lines)
	###print("Pass 3: To split intersecting lines")
	#Steps:
	#	1. Check if the intersecting point of two lines lies within the range of end points of the line, if it doesn't, go to step 5.
	#	2. Form 4 new lines using the original end points and the intersection point.
	#	3. Remove the original two lines and add the new 4 lines
	changes_made = True
	while changes_made:
		i = 0
		intersected_walls = []
		changes_made = False
		while i < len(lines)-1:
			lines_fused = False
			j = i+1
			while j < len(lines):
				point00 = (lines[i][1],lines[i][3])
				point01 = (lines[i][2],lines[i][4])
				point10 = (lines[j][1],lines[j][3])
				point11 = (lines[j][2],lines[j][4])
				intersection_point = get_intersection_point(lines[i], lines[j])
				#print(intersection_point)
				if intersection_point is not None:# and points_away(point00, point01, point10, point11, intersection_point):
					###print("Splitting lines: \n", lines[i],"and \n",lines[j],"having intersection at:\n",intersection_point)
					new_l1, new_l2, new_l3, new_l4 = split_intersecting_lines(lines[i], lines[j], intersection_point)
					#lines[i][5] = 0
					#lines[j][5] = 0
					if not too_close(new_l1):
						print("Inserting line 1: ", new_l1)
						lines.append(new_l1)
					else:
						print("Line 1 :",new_l1,"didn't make it.")
					if not too_close(new_l2):
						print("Inserting line 2: ", new_l2)
						lines.append(new_l2)
					else:
						print("Line 2 :",new_l2,"didn't make it.")
					if not too_close(new_l3):
						print("Inserting line 3: ", new_l3)
						lines.append(new_l3)
					else:
						print("Line 3 :",new_l3,"didn't make it.")
					if not too_close(new_l4):
						print("Inserting line 4: ", new_l4)
						lines.append(new_l4)
					else:
						print("Line  4:",new_l4,"didn't make it.")
					print("\n\n")
					lines = lines[:i] + lines[i+1:j] + lines[j+1:]
					lines_fused = True
					if not changes_made:
						changes_made = True
				j = j+1
			#i+=1
			if not lines_fused:
				i += 1
#	##print("Number of lines that intersect:", len(intersected_walls)/2)
#	###print(lines)
#	for wall in intersected_walls:
#		lines.append(wall)
#	
	while i < (len(lines)):
	##print(lines[i], too_close(lines[i]))
		if too_close(lines[i]):
			#print("Before: ",len(lines))
			lines.pop(i)
			#print("After: ",len(lines))
		else:
			i+=1
	
	with open(file_name+"_walls"+dot_json, 'w') as f:
		json.dump(lines, f)

if __name__ == "__main__":
	#turn_lines_to_1d_walls("ada290-lvl1-li-bl-lg_1.png")
	turn_lines_to_1d_walls("test")
