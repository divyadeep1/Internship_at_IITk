import cv2
import numpy as np
import json
import random
img = np.zeros((768,1024,3), np.uint8)
imgs = np.zeros((768,1024,3), np.uint8)
ortho = cv2.imread("./ortho.png",1)
x_offset = 95
y_offset = 140


#old = [[0,198,405,300,300,1],
#		 [1,195,403,600,600,1],
#		 [2,200,200,298,603,1],
#		 [3,400,400,297,605,1]]

with open("./test.json") as f:
	old = json.load(f)
with open("./test_walls.json") as f:
	new = json.load(f)
#with open("./json/Make graph/test_walls_fuse.json") as f:
#	new2 = json.load(f)

for i in range(len(old)):
	for j in range(len(old[i])):
		old[i][j] = round(old[i][j])
for i in range(len(new)):
	for j in range(len(new[i])):
		new[i][j] = round(new[i][j])

print(old)
print(new)


for line in old:
	img1 = cv2.line(img,(line[1]+x_offset,800-line[3]-y_offset), (line[2]+x_offset,800-line[4]-y_offset), (random.randint(0,255),random.randint(0,255),random.randint(0,255)),3)
cv2.imwrite('./old.jpg',img1)
#cv2.imshow("ss", img)
#cv2.waitKey()

for line in new:
#	if line[5]>0:
	img2 = cv2.line(imgs,(line[1]+x_offset,800-line[3]-y_offset), (line[2]+x_offset,800-line[4]-y_offset), (random.randint(0,255),random.randint(0,255),random.randint(0,255)),3)
cv2.imwrite("./new.jpg",img2)
#for line in new:
#	img3 = cv2.line(img,(line[1],line[3]), (line[2],line[4]), (255,0,255),1)
#cv2.imwrite("./new2.jpg",img2)

#cv2.imshow("ss", img)
#cv2.waitKey()
