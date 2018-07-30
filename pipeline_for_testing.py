from draw_lines import *
from graph_formation.lines_to_walls import *
import os

path = './json/Make walls/'
files = os.listdir(path)

for i,file in enumerate(files):
	try:
		file_name = file[:-5]
		try:
			turn_lines_to_1d_walls(file_name)
		except Exception as e:
			print ("Failed for file lines_to_walls file Exception:\n", str(e))
		try:
			draw(file_name)
		except Exception as e:
			print("failed for draw. Exception:\n", str(e))
		print("Processing file: ".format(file_name))
		print("{}% files processed...".format(round((i+1)/len(files)*100)))
	except Exception as e:
		print("Failed for file: ",file_name)
