"""
	Draw original lines and the lines formed after performing cleaning operations.
"""

import cv2
import numpy as np
import json
import random
img = np.zeros((768,1024,3), np.uint8)
imgs = np.zeros((768,1024,3), np.uint8)

path_to_input_file = "./json/Make walls/"
path_to_output_file = "./json/Make graph/"

dot_json = ".json"
def draw(file_name):
	img = np.zeros((553,828,3), np.uint8)
	imgs = np.zeros((553,828,3), np.uint8)
	imgu = np.zeros((553,828,3), np.uint8)
	imgvs = np.zeros((553,828,3), np.uint8)
	imgi = np.zeros((553,828,3), np.uint8)
	
	with open(path_to_input_file+file_name+dot_json) as f:
		old = json.load(f)
	with open(path_to_output_file+file_name+"_walls"+dot_json) as f:
		new = json.load(f)

	with open(path_to_output_file+file_name+"_union"+dot_json) as f:
		new1 = json.load(f)
	with open(path_to_output_file+file_name+"_vertices_snapped"+dot_json) as f:
		new2 = json.load(f)
	with open(path_to_output_file+file_name+"_intersections"+dot_json) as f:
		new3 = json.load(f)

	for i in range(len(old)):
		for j in range(len(old[i])):
			old[i][j] = round(old[i][j])
	for i in range(len(new)):
		for j in range(len(new[i])):
			new[i][j] = round(new[i][j])
	for i in range(len(new1)):
		for j in range(len(new1[i])):
			new1[i][j] = round(new1[i][j])
	for i in range(len(new2)):
		for j in range(len(new2[i])):
			new2[i][j] = round(new2[i][j])
	for i in range(len(new3)):
		for j in range(len(new3[i])):
			new3[i][j] = round(new3[i][j])

#	print(old)
#	print(new)


	for line in old:
		img1 = cv2.line(img,(line[1],line[3]), (line[2],line[4]), (random.randint(0,255),random.randint(0,255),random.randint(0,255)),3)
	cv2.imwrite('./Screenshots/Snapped_hough_lines/'+file_name+'.png',img1)
	#cv2.imshow("ss", img)
	#cv2.waitKey()

	for line in new:
	#	if line[5]>0:
		img2 = cv2.line(imgs,(line[1],line[3]), (line[2],line[4]), (random.randint(0,255),random.randint(0,255),random.randint(0,255)),3)
	cv2.imwrite('./Screenshots/Cleaned_lines/'+file_name+'.png',img2)

	for line in new1:
		img3 = cv2.line(imgu,(line[1],line[3]), (line[2],line[4]), (random.randint(0,255),random.randint(0,255),random.randint(0,255)),3)
	cv2.imwrite('./Screenshots/Cleaned_lines/'+file_name+'_1_union.png',img3)

	for line in new2:
	#	if line[5]>0:
		img4 = cv2.line(imgvs,(line[1],line[3]), (line[2],line[4]), (random.randint(0,255),random.randint(0,255),random.randint(0,255)),3)
	cv2.imwrite('./Screenshots/Cleaned_lines/'+file_name+'_2_vertices_snapped.png',img4)

	for line in new3:
	#	if line[5]>0:
		img5 = cv2.line(imgi,(line[1],line[3]), (line[2],line[4]), (random.randint(0,255),random.randint(0,255),random.randint(0,255)),3)
	cv2.imwrite('./Screenshots/Cleaned_lines/'+file_name+'_3_intersections.png',img5)

if __name__=='__main__':
	draw("final_data_s")
