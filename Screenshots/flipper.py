import cv2 as cv
import os

input_path = "./Cleaned_lines/"
output_path = "./Flipped_bulk/"

images = os.listdir(input_path)

for img in images:
	image = cv.imread(input_path+img)
	t = cv.flip(image, 0)
	cv.imwrite(output_path+img, t)
