#from graph_formation.lines_to_walls import *
from graph_formation.walls_to_graph import *
#from extruder import *
import os
from draw_lines import *
from overlap_new_on_old import *
#from hline import *
from extruder_old import *
from graph_formation.lines_to_walls_old import *
#base_string = "co_ordinates_line"
error = ""
number_of_errors = 0
errorneous_files = []
path = './json/Make walls/'

def log_error(file_name, e):
	global number_of_errors
	global error
	number_of_errors += 1
	error += str(number_of_errors) + "{}".format(file_name) + "\n" + str(e) + "\n"
	print("File: {} failed to be processed!".format(file_name))
	print("Exception: {}".format(e))
	errorneous_files.append('\"'+file_name+'\"')

files = os.listdir(path)

#hline()

for i,file in enumerate(files):
	try:
		file_name = file[:-5]
#		try:
		turn_lines_to_1d_walls(file_name)
		draw(file_name)
#		except Exception as e:
#			print ("Failed for file lines_to_walls file: ", file_name, str(e))
#		try:
		make_graph_from_1d_walls(file_name)
#		except Exception as e:
#			print("failed for file walls_to_graph: ", file_name, str(e))
#		try: 
		extrude_1d_walls_in_3d(file_name)
#		except Exception as e:
#			print("failed for extrude: ", file_name)
#			print(str(e))
		print("Processing file: {}".format(file_name))
		print("{}% files processed...".format(round((i+1)/len(files)*100)))
	except Exception as e:
		log_error(file_name,e)

#print("Processing complete, overlapping results with the original image...\nCheck Screenshots/Overlapped\n")
#for i,file in enumerate(files):
#	file_name = file[:-5]
#	try:
#		overlap_images_with_original(file_name)
#	except Exception as e:
#		print("Failed for file {} with exception {}.".format(file_name, str(e)))

print("number_of_errors: ", number_of_errors)
with open("error_log.txt", 'w') as f:
	f.write(error)
with open("error_log.txt", 'a+') as f:
	f.write("number_of_errors: {}".format(number_of_errors))
	for i in errorneous_files:
		f.write(str(i)+",")
