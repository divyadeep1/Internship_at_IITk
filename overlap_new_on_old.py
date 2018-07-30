"""
	Module to generate images that are alpha blend of the input image 
	with the outputs of each stage of the pipeline.
"""

import cv2
import numpy as np

path_to_original_image = './Input_images/'
path_to_hough_line_result = './hough_line_output/'
path_to_snapped_hough_line = './Screenshots/Snapped_hough_lines/'
path_to_cleaned_lines = './Screenshots/Cleaned_lines/'
path_to_backprojection = './Screenshots/Backprojections/'
path_to_overlapped_output = './Screenshots/Overlapped/'
dot_png = ".png"

def overlap_images_with_original(file_name):
	original_image = cv2.imread(path_to_original_image+file_name+dot_png,1)
	hough_line_output = cv2.imread(path_to_hough_line_result+file_name+dot_png,1)
	snapped_hough_lines = cv2.imread(path_to_snapped_hough_line+file_name+dot_png,1)
	cleaned_lines = cv2.imread(path_to_cleaned_lines+file_name+dot_png,1)
	#backprojection = cv2.imread(path_to_backprojection+file_name+dot_png,1)
	
	alpha = 0.55
	
	#original_image = cv2.multiply(-alpha, original_image)
	#hough_line_output = cv2.multiply(alpha, hough_line_output)
	#snapped_hough_lines = cv2.multiply(alpha, snapped_hough_lines)
	#cleaned_lines = cv2.multiply(alpha, cleaned_lines)
	#backprojection = cv2.multiply(alpha, backprojection)
	
	hl_overlapped = cv2.addWeighted(hough_line_output, alpha, original_image, 1-alpha, 0.0)
	shl_overlapped = cv2.addWeighted(original_image, alpha, snapped_hough_lines, 1-alpha, 0.0)
	cl_overlapped = cv2.addWeighted(original_image, alpha, cleaned_lines, 1-alpha, 0.0)
	#b_overlapped = cv2.addWeighted(original_image, alpha, backprojection, 1-alpha, 0.0)
	
	cv2.imwrite(path_to_overlapped_output+file_name+"stage_1"+dot_png, hl_overlapped)
	cv2.imwrite(path_to_overlapped_output+file_name+"stage_2"+dot_png, shl_overlapped)
	cv2.imwrite(path_to_overlapped_output+file_name+"stage_3"+dot_png, cl_overlapped)
	
#	cv2.imshow("res",hl_overlapped)
#	cv2.waitKey(0)

if __name__ == '__main__':
	overlap_images_with_original('ada290-lvl1-li-bl-lg_1')
