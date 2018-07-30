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

if __name__ == '__main__':
	from geometry import *
	from constants import *
else:
	from graph_formation.geometry import *
	from graph_formation.constants import *

def turn_lines_to_1d_walls(file_name):
	path_to_input_file = "./json/Make walls/"
	path_to_output_file = "./json/Make graph/"
	dot_json = ".json"

	global wall_number

	with open(path_to_input_file+file_name+dot_json, 'r') as f:
		lines = json.load(f)
	
	
	for i,l in enumerate(lines):
		lines[i] = [l[0], round(l[1]), round(l[2]), round(l[3]), round(l[4]), l[5]]

	wall_number = len(lines)-1
	init(wall_number)
	####print ("Number of lines: ",len(lines))

	####print("Pass 0.5: Making slightly slanting lines straight:")
#	for i in range(len(lines)):
#		lines[i] = make_slightly_slanting_lines_straight(lines[i])
	
	#Remove lines that are too short in length
	i=0
	while i < (len(lines)):
		###print(lines[i], too_close(lines[i]))
		if too_close(lines[i]):
			##print("Before: ",len(lines))
			lines.pop(i)
			##print("After: ",len(lines))
		else:
			i+=1

	###print("Pass 1: To fuse overlapping colinear lines")

	while True:
		changes_made = False
		i=0
		while i<len(lines)-1:
			lines_fused = False
			j = i+1
			while j < len(lines):
				if union_of_overlapping_lines(lines[i], lines[j]) is not None:
					##print ("merging lines {},{}".format(lines[i],lines[j]))
					lines.append(list(union_of_overlapping_lines(lines[i], lines[j])))
					lines = lines[0:i] + lines[i+1:j] + lines[j+1:]
					lines_fused = True
					changes_made = True
				j += 1
			if not lines_fused:
				i += 1
		if not changes_made:
			break
	with open(path_to_output_file+file_name+"_union"+dot_json, 'w') as f:
		json.dump(lines, f)

#	#Removing lines that are too short to be considered.
#	while i < (len(lines)):
#	###print(lines[i], too_close(lines[i]))
#		if too_close(lines[i]):
#			##print("Before: ",len(lines))
#			lines.pop(i)
#			##print("After: ",len(lines))
#		else:
#			i+=1


	####print("Pass 1.5: Making slightly slanting lines straight:")
#	for i in range(len(lines)):
#		lines[i] = make_slightly_slanting_lines_straight(lines[i])

	####print("Number of lines after first pass:", len(lines))
	#Fusing points that are close to each other.
	i = 0
	while i < len(lines)-1:
		current_set_close_to_point_0 = []
		current_set_close_to_point_1 = []
		for j in range(i+1,len(lines)):
			###print("line_one, line_two: ", i, j)
			check_angled(lines, i, j,current_set_close_to_point_0, current_set_close_to_point_1)
		lines = fuse_angled(lines, i, current_set_close_to_point_0, current_set_close_to_point_1)
		i += 1
		


	for i in range(len(lines)-1):
		for j in range(i+1,len(lines)):
			intersection_point = line_intersection(lines[i], lines[j])
			if intersection_point != (np.nan,np.nan):
				if distance(lines[i][1],lines[i][3], intersection_point[0], intersection_point[1]) < max_dist_between_two_nodes:
					lines[i][1] = intersection_point[0]
					lines[i][3] = intersection_point[1]
				elif distance(lines[i][2],lines[i][4], intersection_point[0], intersection_point[1]) < max_dist_between_two_nodes:
					lines[i][2] = intersection_point[0]
					lines[i][4] = intersection_point[1]
				elif distance(lines[j][1],lines[j][3], intersection_point[0], intersection_point[1]) < max_dist_between_two_nodes:
					lines[j][1] = intersection_point[0]
					lines[j][3] = intersection_point[1]
				elif distance(lines[j][2],lines[j][4], intersection_point[0], intersection_point[1]) < max_dist_between_two_nodes:
					lines[j][2] = intersection_point[0]
					lines[j][4] = intersection_point[1]


	with open(path_to_output_file+file_name+"_vertices_snapped"+dot_json, 'w') as f:
		json.dump(lines, f)
	#Removing lines that are too short to be considered.
#	i=0
#	while i < (len(lines)):
#		###print(lines[i], too_close(lines[i]))
#		if too_close(lines[i]):
#			##print("Before: ",len(lines))
#			lines.pop(i)
#			##print("After: ",len(lines))
#		else:
#			i+=1
		
		#TODO! T section
		
	####print("Pass 2.5: Making slightly slanting lines straight:")
#	for i in range(len(lines)):
#		lines[i] = make_slightly_slanting_lines_straight(lines[i])

	####print("Number of lines after second pass:", len(lines))

	#####print (lines)
	####print("Pass 3: To split intersecting lines")
	#Steps:
	#	1. Check if the intersecting point of two lines lies within the range of end points of the line, if it doesn't, go to step 5.
	#	2. Form 4 new lines using the original end points and the intersection point.
	#	3. Remove the original two lines and add the new 4 lines

	changes_made = True
	while changes_made:
		i = 0
		intersected_walls = []
		changes_made = False
		while i < len(lines):
			lines_fused = False
			j = i+1
			while j < len(lines):
				intersection_point = get_intersection_point(lines[i], lines[j])
				if intersection_point is not None:
					#print("Splitting lines: \n", lines[i],"and \n",lines[j],"having intersection at:\n",intersection_point)
					new_l1, new_l2, new_l3, new_l4 = split_intersecting_lines(lines[i], lines[j], intersection_point)
					#lines[i][5] = 0
					#lines[j][5] = 0
					if not too_close(new_l1):
						#print("Inserting line 1: ", new_l1)
						lines.append(new_l1)
					#else:
						#print("Line 1 :",new_l1,"didn't make it.")
					if not too_close(new_l2):
						#print("Inserting line 2: ", new_l2)
						lines.append(new_l2)
					#else:
						#print("Line 2 :",new_l2,"didn't make it.")
					if not too_close(new_l3):
						#print("Inserting line 3: ", new_l3)
						lines.append(new_l3)
					#else:
						#print("Line 3 :",new_l3,"didn't make it.")
					if not too_close(new_l4):
						#print("Inserting line 4: ", new_l4)
						lines.append(new_l4)
					#else:
						#print("Line  4:",new_l4,"didn't make it.")
					#print("\n\n")
					lines = lines[:i] + lines[i+1:j] + lines[j+1:]
					lines_fused = True
					if not changes_made:
						changes_made = True
				j = j+1
			#i+=1
			if not lines_fused:
				i += 1
				
	with open(path_to_output_file+file_name+"_intersections"+dot_json, 'w') as f:
		json.dump(lines, f)
	i=0
	while i < (len(lines)):
	###print(lines[i], too_close(lines[i]))
		if too_close(lines[i]):
			print("Before: ",len(lines))
			lines.pop(i)
			print("After: ",len(lines))
		else:
			i+=1
#	i = 0
#	while i < len(lines)-1:
#		current_set_close_to_point_0 = []
#		current_set_close_to_point_1 = []
#		for j in range(i+1,len(lines)):
#			###print("line_one, line_two: ", i, j)
#			check_angled(lines, i, j,current_set_close_to_point_0, current_set_close_to_point_1)
#		lines = fuse_angled(lines, i, current_set_close_to_point_0, current_set_close_to_point_1)
#		i += 1
	
#	while True:
#		changes_made = False
#		i=0
#		while i<len(lines)-1:
#			lines_fused = False
#			j = i+1
#			while j < len(lines):
#				if union_of_overlapping_lines(lines[i], lines[j]) is not None:
#					##print ("merging lines {},{}".format(lines[i],lines[j]))
#					lines.append(list(union_of_overlapping_lines(lines[i], lines[j])))
#					lines = lines[0:i] + lines[i+1:j] + lines[j+1:]
#					lines_fused = True
#					changes_made = True
#				j += 1
#			if not lines_fused:
#				i += 1
#		if not changes_made:
#			break
	
	with open(path_to_output_file+file_name+"_walls"+dot_json, 'w') as f:
		json.dump(lines, f)
	#for line in lines:
	#	print("Length of line: ", distance(line[1],line[3],line[2],line[4]))


if __name__ == "__main__":
	#turn_lines_to_1d_walls("ada290-lvl1-li-bl-lg_1.png")
	turn_lines_to_1d_walls("final_data_s")
