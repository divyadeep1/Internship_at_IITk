"""
Thinning the box-thresh output.
"""
import cv2 as cv
import numpy as np

img = cv.imread('./Input_images/testing.png',0)
size = np.size(img)
skel = np.zeros(img.shape,np.uint8)
element = cv.getStructuringElement(cv.MORPH_CROSS, (3,3))
done = False

for i in range(3):
	done = False
	ctr = 0
	print("entering while loop, iteration number:", i)
	while not done:
		print("While loop's iteration number: ", ctr)
		ctr += 1
		eroded = cv.erode(img,element)
		temp = cv.dilate(eroded, element)
		temp = cv.subtract(img, temp)
		skel = cv.bitwise_or(skel,temp)
		img = eroded.copy()
		zeros = size-cv.countNonZero(img)
		cv.imshow("result", skel)
		cv.waitKey(0)
		if zeros==size:
			done = True
	img = skel
	skel = np.zeros(img.shape,np.uint8)
	print("While loop ran {} times.".format(ctr))

#cv.imwrite('./result_of_thinning_operation.png', skel)

#cv.imshow("result", skel)
#cv.waitKey(0)
