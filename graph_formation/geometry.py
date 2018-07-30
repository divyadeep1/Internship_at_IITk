"""
Geometry functions helper file.
"""
#print (__name__)
import sys
import math
if __name__ == 'geometry':
	import constants
else:
	from graph_formation import constants
import numpy as np
import copy

def init(wall_number):
	constants.wall_number = wall_number

def distance(x1,y1,x2,y2):
	return(math.sqrt((x1-x2)**2 + (y1-y2)**2))

def get_intersection_point_new(a1,a2,b1,b2):
	#find intersection pt. of two vectors
	#intersection will be near point p01 and p11 i.e. a2,b2
	p00 = np.array(a1)
	p01 = np.array(a2)
	p10 = np.array(b1)
	p11 = np.array(b2)
	rhs = p01-p10
	#print("p00,p01,p10,p11: ",p00,p01,p10,p11)
	a = p00[0] - p01[0]
	b = p11[0] - p10[0]
	c = p00[1] - p01[1]
	d = p11[1] - p10[1]
	A = np.array([[a,b],[c,d]])
	#print("A,rhs",A,rhs)
	res = np.linalg.solve(A,rhs)
	if np.nan in res:
		return (np.nan,np.nan)
	alpha = -res[0]
	#print(alpha*p00[0] + (1-alpha)*p01[0] , alpha*p00[1] + (1-alpha)*p01[1])
	#print("\n")
	return (alpha*p00[0] + (1-alpha)*p01[0] , alpha*p00[1] + (1-alpha)*p01[1])


def parallel_and_close(line_one, line_two):
	"""Checks if 2 lines are parallel and close to one another. (NOT BEING USED AS OF NOW)"""
	d1 = math.sqrt((line_one[1]-line_two[1])**2 + (line_one[3]-line_two[3])**2) # sqrt((x11 - x21)**2 + (y11 - y21))
	d2 = math.sqrt((line_one[2]-line_two[2])**2 + (line_one[4]-line_two[4])**2) # sqrt((x12 - x22)**2 + (y12 - y22))
	d3 = math.sqrt((line_one[1]-line_two[2])**2 + (line_one[3]-line_two[4])**2) # sqrt((x11 - x21)**2 + (y11 - y21))
	d4 = math.sqrt((line_one[2]-line_two[1])**2 + (line_one[4]-line_two[3])**2) # sqrt((x11 - x21)**2 + (y11 - y21))
	
	if abs(d1-d2) < constants.epsilon and (d1+d2)/2 < constants.epsilon2:
		return True
	elif abs(d3-d4) < constants.epsilon and (d3+d4)/2 < constants.epsilon2:
		return True
	else:
		return False


def fuse_lines(line_one, line_two):
	"""Fuses two parallel lines into a single wall. (NOT BEING USED AS OF NOW)"""
	constants.wall_number += 1
	if abs(math.sqrt((line_one[1]-line_two[1])**2 + (line_one[3]-line_two[3])**2) -
		math.sqrt((line_one[2]-line_two[2])**2 + (line_one[4]-line_two[4])**2)) < constants.epsilon:
		weight = round((math.sqrt((line_one[1]-line_two[1])**2 + (line_one[3]-line_two[3])**2) + 
		math.sqrt((line_one[2]-line_two[2])**2 + (line_one[4]-line_two[4])**2) )/2)
		return  [
				constants.wall_number, 
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
				constants.wall_number, 
				round((line_one[1]+line_two[2])/2),
				round((line_one[2]+line_two[1])/2),
				round((line_one[3]+line_two[4])/2),
				round((line_one[4]+line_two[3])/2),
				weight
			   ]


def check_angled_and_fuse(line_one, line_two):
	"""Check if end points of two lines are close to each other 
	and fuse them if they are (NOT BEING USED AS OF NOW)"""
	
	d1 = math.sqrt((line_one[1]-line_two[1])**2 + (line_one[3]-line_two[3])**2) # sqrt((x11 - x21)**2 + (y11 - y21))
	d2 = math.sqrt((line_one[2]-line_two[2])**2 + (line_one[4]-line_two[4])**2) # sqrt((x12 - x22)**2 + (y12 - y22))
	d3 = math.sqrt((line_one[1]-line_two[2])**2 + (line_one[3]-line_two[4])**2) # sqrt((x11 - x21)**2 + (y11 - y21))
	d4 = math.sqrt((line_one[2]-line_two[1])**2 + (line_one[4]-line_two[3])**2) # sqrt((x11 - x21)**2 + (y11 - y21))
	if (d1 < constants.max_dist_between_two_nodes and d1>0):
		####print(line_one, line_two, "fused to ")
		line_one = [line_one[0], round((line_one[1]+line_two[1])/2), line_one[2], round((line_one[3]+line_two[3])/2), line_one[4], line_one[5]] 
		line_two = [line_two[0], round((line_one[1]+line_two[1])/2), line_two[2], round((line_one[3]+line_two[3])/2), line_two[4], line_two[5]]
		####print(line_one, line_two)
		return (line_one,line_two, True)
	elif (d2 < constants.max_dist_between_two_nodes and d2>0):
#		####print(line_one, line_two, "fused to ")
		line_one = [line_one[0], line_one[1], round((line_one[2]+line_two[2])/2), line_one[3], round((line_one[4]+line_two[4])/2), line_one[5]]
		line_two = [line_two[0], line_two[1], round((line_one[2]+line_two[2])/2), line_two[3], round((line_one[4]+line_two[4])/2), line_two[5]]
#		####print(line_one, line_two)
		return (line_one, line_two, True)
	elif (d3 < constants.max_dist_between_two_nodes and d3>0):
#		####print(line_one, line_two, "fused to ")
		line_one = [line_one[0], round((line_one[1]+line_two[2])/2), line_one[2], round((line_one[3]+line_two[4])/2), line_one[4], line_one[5]]
		line_two = [line_two[0], line_two[1], round((line_one[1]+line_two[2])/2), line_two[3], round((line_one[3]+line_two[4])/2), line_two[5]]
#		####print(line_one, line_two)
		return (line_one, line_two,True)
	elif (d4 < constants.max_dist_between_two_nodes and d4>0):
#		####print(line_one, line_two, "fused to ")
		line_one = [line_one[0], line_one[1], round((line_one[2]+line_two[1])/2), line_one[3], round((line_one[4]+line_two[3])/2), line_one[5]]
		line_two = [line_two[0], round((line_one[2]+line_two[1])/2), line_two[2], round((line_one[4]+line_two[3])/2), line_two[4], line_two[5]]
#		####print(line_one, line_two)
		return (line_one, line_two, True)
	else:
		return (line_one, line_two, False)

def line_intersection(line1, line2):
	"""Used to get the intersection point of lines."""
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
	"""
		Finds out all the points located close to the two end points of a line.
	"""
	
	line_one = lines[i]
	line_two = lines[j]
	x00, x01, y00, y01 = line_one[1], line_one[2], line_one[3], line_one[4]
	x10, x11, y10, y11 = line_two[1], line_two[2], line_two[3], line_two[4]

	d00 = math.sqrt((x00-x10)**2 + (y00-y10)**2)
	d01 = math.sqrt((x00-x11)**2 + (y00-y11)**2)
	d10 = math.sqrt((x01-x10)**2 + (y01-y10)**2)
	d11 = math.sqrt((x01-x11)**2 + (y01-y11)**2)
	
	###print("p00: ",x00,y00)
	###print("p01: ",x01,y01)
	###print("p00: ",x10,y10)
	###print("p01: ",x11,y11)
	
	###print("d00,d01,d10,d11: ",d00,d01,d10,d11)
	
	if d00 < constants.max_dist_between_two_nodes and d00 > 0:
		##print("d00")
		current_set_close_to_point_0.append([j,0])
	elif d01 < constants.max_dist_between_two_nodes and d01 > 0:
		##print("d01")
		current_set_close_to_point_0.append([j,1])
	elif d10 < constants.max_dist_between_two_nodes and d10 > 0:
		##print("d10")
		current_set_close_to_point_1.append([j,0])
	elif d11 < constants.max_dist_between_two_nodes and d11 > 0:
		##print("d11")
		current_set_close_to_point_1.append([j,1])

def fuse_angled(lines, i, current_set_close_to_point_0, current_set_close_to_point_1):
	"""
		Fuses all the points close to the end point of a line into a single point.
	"""
	
	new_lines = copy.deepcopy(lines)
	intrsctn_pnt_0 = []
	intrsctn_pnt_1 = []
	line_one = new_lines[i]
	##print("old lines: ",new_lines[i])
	#if len(current_set_close_to_point_0)>0:
		##print("current_set_close_to_point_0:", current_set_close_to_point_0)
		##print(lines[current_set_close_to_point_0[0][0]], lines[i])
	#if len(current_set_close_to_point_1)>0:
		##print("current_set_close_to_point_1: ", current_set_close_to_point_1)
		##print(lines[current_set_close_to_point_1[0][0]], lines[i])

	for j, pt in current_set_close_to_point_0:
		line_two = new_lines[j]
		ip = line_intersection(line_one, line_two)
		#ip = get_intersection_point_new(a1,a2,b1,b2)
		##print(ip)
		print(current_set_close_to_point_0)
		if ip == (np.nan, np.nan): #or ip==None:
			current_set_close_to_point_0.pop(current_set_close_to_point_0.index([j,pt]))
			continue
		else:
			intrsctn_pnt_0.append(ip)
	#NEW
#	for l, [j, pt] in enumerate(current_set_close_to_point_0):
#		line_one1 = lines[j]
#		if l < len(current_set_close_to_point_0)-1:
#			for k in range(l+1, len(current_set_close_to_point_0)):
#				line_two1 = lines[current_set_close_to_point_0[k][0]]
#				ip = line_intersection(line_one1, line_two1)
#				if ip == (np.nan, np.nan):
#					current_set_close_to_point_0[k][1] = 3
#					continue
#				else:
#					intrsctn_pnt_0.append(ip)

	new_pt = None
	if len(intrsctn_pnt_0)>0:
		new_pt = (round(np.average(np.array(intrsctn_pnt_0)[:,0])), round(np.average(np.array(intrsctn_pnt_0)[:,1])))
		new_lines[i][1], new_lines[i][3] = new_pt
		for j, pt in current_set_close_to_point_0:
			if pt!=3:
				new_lines[j][pt+1], new_lines[j][pt+3] = new_pt
		##print(intrsctn_pnt_0)
	##print("new point: ",new_pt)

	for j, pt in current_set_close_to_point_1:
		line_two = lines[j]
		ip = line_intersection(line_one, line_two)
		if ip == (np.nan, np.nan):
			current_set_close_to_point_1.pop(current_set_close_to_point_1.index([j,pt]))
			continue
		else:
			intrsctn_pnt_1.append(ip)

	#NEW
#	for l, [j, pt] in enumerate(current_set_close_to_point_1):
#		line_one1 = lines[j]
#		if l < len(current_set_close_to_point_1)-1:
#			for k in range(l+1, len(current_set_close_to_point_1)):
#				line_two1 = lines[current_set_close_to_point_1[k][0]]
#				ip = line_intersection(line_one1, line_two1)
#				if ip == (np.nan, np.nan):
#					current_set_close_to_point_1[k][1] = 3
#					continue
#				else:
#					intrsctn_pnt_0.append(ip)


	if len(intrsctn_pnt_1)>0:
		new_pt = (round(np.average(np.array(intrsctn_pnt_1)[:,0])), round(np.average(np.array(intrsctn_pnt_1)[:,1])))
		new_lines[i][2], new_lines[i][4] = new_pt
		for j, pt in current_set_close_to_point_1:
			if pt!=3:
				new_lines[j][pt+1], new_lines[j][pt+3] = new_pt
	#changed = new_lines==lines
	#print(changed, type(lines))
		#print(intrsctn_pnt_1)
	##print("new point: ",new_pt)
	#print(new_lines[i]==lines[i])
	return new_lines#, changed

def make_slightly_slanting_lines_straight(line):
	"""
		Makes lines whose end points' 'x' or 'y' values differ by a very small number.
	"""
	
	####print ("Before : ", line)
	####print(constants.eps3)
	if(abs(line[1]-line[2]) < constants.eps3):
		line[1] = line[2]
	if(abs(line[3]-line[4]) < constants.eps3):
		line[3] = line[4]
	####print ("After : ", line)
	return line

def get_line_eqns(line_one, line_two):
	"""
		Used to get the constants of two lines.
		
		Returns:
			a,m and c for the two lines where
			a,m and c are constants in the line equation represented in
			the following format: ay = mx+c
	"""
	
	x00, x01, y00, y01 = line_one[1], line_one[2], line_one[3], line_one[4]
	x10, x11, y10, y11 = line_two[1], line_two[2], line_two[3], line_two[4]
	if (x01!=x00):
		m0 = ((y01-y00)/(x01-x00))
	else:
		m0 = constants.infinity
	if (x11!=x10):
		m1 = ((y11-y10)/(x11-x10))
	else:
		m1 = constants.infinity
	#Non-parallel lines with equations ay-mx = c:
	if m0<constants.infinity:
		c0 = y01-m0*x01
		a0 = 1
		m0 = -m0
	else:
		c0 = x01
		a0 = 0
		m0 = 1
	if m1<constants.infinity:
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
	try:
		intersection_point = np.linalg.solve(A,C) # result is (y,x) and not (x,y)
		x3 = round(intersection_point[1])
		y3 = round(intersection_point[0])
	except:
		return None
	#print(line_one, line_two,intersection_point)
	if (x3-constants.eps>min(x00,x01) and max(x00,x01)-constants.eps>x3 and y3-constants.eps>min(y00,y01) and max(y00,y01)-constants.eps>y3) and (x3-constants.eps>min(x10,x11) and max(x10,x11)-constants.eps>x3 and y3-constants.eps>min(y10,y11) and max(y10,y11)-constants.eps>y3) and not ((x3 in (x00,x01) and x3 in (x10,x11) and y3 in (y00,y01) and y3 in (y10,y11))):
		return(x3,y3)
	else:
		#print("Lines intersect but not in the required range.")
		return None
	#except:
	#	return None

def split_intersecting_lines(line_one, line_two, intersection_point):
	"""
		Splits lines intersecting at a point into 4 new lines,
		having a common end point - the intersection_point.
	"""
	if constants.wall_number > 400:
		raise Exception("Too many walls.")
	
	print("wall number:", constants.wall_number)
	_, x00, x01, y00, y01, w0 = line_one
	_, x10, x11, y10, y11, w1 = line_two
	x3 = intersection_point[0]
	y3 = intersection_point[1]
	new_l1 = [constants.wall_number+1,x00,x3,y00,y3,w0]
	new_l2 = [constants.wall_number+2,x01,x3,y01,y3,w0]
	new_l3 = [constants.wall_number+3,x10,x3,y10,y3,w1]
	new_l4 = [constants.wall_number+4,x11,x3,y11,y3,w1]
	constants.wall_number += 4
	return (new_l1, new_l2, new_l3, new_l4)


def points_away(point00, point01, point10, point11, intersection_point):
	"""
		Checks if the intersection point is not the same as either end point of the two lines.
	"""
	
	if (
		(point00[0]==intersection_point[0] and point00[1]==intersection_point[1]) or
		(point01[0]==intersection_point[0] and point01[1]==intersection_point[1]) or
		(point10[0]==intersection_point[0] and point10[1]==intersection_point[1]) or
		(point11[0]==intersection_point[0] and point11[1]==intersection_point[1])
		):
		return False
	return True


def union_of_overlapping_lines(line_one, line_two):
	"""
		Combines overlapping colinear lines into single lines.
	"""
	
	_, x00, x01, y00, y01, w0 = line_one
	_, x10, x11, y10, y11, w1 = line_two
	a1,m1,c1,a2,m2,c2 = get_line_eqns(line_one, line_two)
	m1 = -m1
	m2 = -m2
	if a1==a2 and m1==m2 and c1==c2:
		###print("{}y = {}x + {}".format(a1,m1,c1))
	#3 cases of same line are possible:
	#1. one line is completely inside the boundries of another.
	#2. the two lines overlap.
	#3. they are separate.
		if m1>=0:
			x_list = [x00, x01,x10, x11]
			y_list = [y00, y01,y10, y11]
			x_list.sort(), y_list.sort()
			###print(x_list, y_list)
			x1,x2,x3,x4 = x_list
			y1,y2,y3,y4 = y_list
			if x1 in line_one[1:3] and x2 in line_two[1:3] and x3 in line_two[1:3] and x4 in line_one[1:3]:
				###print("YES")
				return _,x1,x4,y1,y4,w0
			elif x1 in line_two[1:3] and x2 in line_one[1:3] and x3 in line_one[1:3] and x4 in line_two[1:3]:
				###print("YES")
				return _,x1,x4,y1,y4,w1
		
			if x1 in line_one[1:3] and x2 in line_two[1:3] and x3 in line_one[1:3] and x4 in line_two[1:3]:
				###print("YES")
				return _,x1,x4,y1,y4,(w1+w0)/2
			elif x1 in line_two[1:3] and x2 in line_one[1:3] and x3 in line_two[1:3] and x4 in line_one[1:3]:
				###print("YES")
				return _,x1,x4,y1,y4,(w1+w0)/2
		
			if x1 in line_one[1:3] and x2 in line_one[1:3] and x3 in line_two[1:3] and x4 in line_two[1:3]:
				###print("NO")
				return None
			elif x1 in line_two[1:3] and x2 in line_two[1:3] and x3 in line_one[1:3] and x4 in line_one[1:3]:
				###print("NO")
				return None
		elif(a1==0 and m1==-1):
			x_list = [x00, x01,x10, x11]
			y_list = [y00, y01,y10, y11]
			x_list.sort(), y_list.sort()
			###print(x_list, y_list)
			x1,x2,x3,x4 = x_list
			y1,y2,y3,y4 = y_list
			if y1 in line_one[3:5] and y2 in line_two[3:5] and y3 in line_two[3:5] and y4 in line_one[3:5]:
				###print("YES")
				return _,x1,x4,y1,y4,w0
			elif y1 in line_two[3:5] and y2 in line_one[3:5] and y3 in line_one[3:5] and y4 in line_two[3:5]:
				###print("YES")
				return _,x1,x4,y1,y4,w1
	
			if y1 in line_one[3:5] and y2 in line_two[3:5] and y3 in line_one[3:5] and y4 in line_two[3:5]:
				###print("YES")
				return _,x1,x4,y1,y4,(w1+w0)/2
			elif y1 in line_two[3:5] and y2 in line_one[3:5] and y3 in line_two[3:5] and y4 in line_one[3:5]:
				###print("YES")
				return _,x1,x4,y1,y4,(w1+w0)/2
	
			if y1 in line_one[3:5] and y2 in line_one[3:5] and y3 in line_two[3:5] and y4 in line_two[3:5]:
				#print("NO")
				return None
			elif y1 in line_two[3:5] and y2 in line_two[3:5] and y3 in line_one[3:5] and y4 in line_one[3:5]:
				#print("NO")
				return None
		else:
			x_list = [x00, x01,x10, x11]
			y_list = [y00, y01,y10, y11]
			x_list.sort(), y_list.sort(reverse=True)
			x1,x2,x3,x4 = x_list
			y1,y2,y3,y4 = y_list
			if x1 in line_one[1:3] and x2 in line_two[1:3] and x3 in line_two[1:3] and x4 in line_one[1:3]:
				###print("YES")
				return _,x1,x4,y1,y4,w0
			elif x1 in line_two[1:3] and x2 in line_one[1:3] and x3 in line_one[1:3] and x4 in line_two[1:3]:
				###print("YES")
				return _,x1,x4,y1,y4,w1
		
			if x1 in line_one[1:3] and x2 in line_two[1:3] and x3 in line_one[1:3] and x4 in line_two[1:3]:
				###print("YES")
				return _,x1,x4,y1,y4,(w1+w0)/2
			elif x1 in line_two[1:3] and x2 in line_one[1:3] and x3 in line_two[1:3] and x4 in line_one[1:3]:
				###print("YES")
				return _,x1,x4,y1,y4,(w1+w0)/2
		
			if x1 in line_one[1:3] and x2 in line_one[1:3] and x3 in line_two[1:3] and x4 in line_two[1:3]:
				###print("NO")
				return None
			elif x1 in line_two[1:3] and x2 in line_two[1:3] and x3 in line_one[1:3] and x4 in line_one[1:3]:
				###print("NO")
				return None
	else:
		###print("NOT even parallel")
		return None

def too_close(line):
	"""
		Checks if line is too short to be considered independently.
	"""
	if math.sqrt((line[2]-line[1])**2 + (line[4]-line[3])**2) < constants.min_dist_to_be_called_a_line:
		return True
	###print("Snap! one line gone!")
	return False

