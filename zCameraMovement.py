""" Camera Movement using keyboard and mouse
"""

from OpenGL.GL import *
from OpenGL.GL.ARB import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.GLUT.special import *
from OpenGL.GL.shaders import *
from glew_wish import *

import math
import glm
import common
import glfw
import sys
import os


# Global window
window = None
null = c_void_p(0)

#for camera
position = glm.vec3(0,0,10)
front = glm.vec3(0,0,-1)
up = glm.vec3(0,1,0)

#for mouse movements
lastX = 512
lastY = 256
pitch = 0
yaw = 3.14
firstmouse = True

def opengl_init():
	global window
	# Initialize the library
	if not glfw.init():
		print("Failed to initialize GLFW\n",file=sys.stderr)
		return False

	# Open Window and create its OpenGL context
	window = glfw.create_window(1024, 768, "Tutorial 03", None, None) #(in the accompanying source code this variable will be global)
	glfw.window_hint(glfw.SAMPLES, 4)
	glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
	glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
	glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)
	glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

	if not window:
		print("Failed to open GLFW window. If you have an Intel GPU, they are not 3.3 compatible. Try the 2.1 version of the tutorials.\n",file=sys.stderr)
		glfw.terminate()
		return False

	# Initialize GLEW
	glfw.make_context_current(window)
	glewExperimental = True

	# GLEW is a framework for testing extension availability.  Please see tutorial notes for
	# more information including why can remove this code.
	if glewInit() != GLEW_OK:
		print("Failed to initialize GLEW\n",file=sys.stderr);
		return False
	return True


def mouse_events(window, xpos, ypos):
	global lastX
	global lastY
	global pitch
	global yaw
	global front
	global firstmouse
	
	if firstmouse:
		lastX=xpos
		lastY=ypos
		firstmouse = False
	mousespeed = 0.005
	
	xOffset =  (xpos - lastX)
	yOffset = (lastY - ypos)
	
	lastX = xpos
	lastY = ypos
	
	yaw -= (xOffset * mousespeed)
	pitch += (yOffset * mousespeed)
	
	if pitch>=89:
		pitch = 89
	if pitch<=-89:
		pitch = -89
		
	front.x = math.cos(pitch) * math.sin(yaw)
	front.y = math.sin(pitch)
	front.z = math.cos(pitch) * math.cos(yaw)
	
	

def key_events(window,key,scancode,action,mods):
	global position
	global front
	global up
	
	#depth test
	if action == glfw.PRESS and key == glfw.KEY_D:
		if glIsEnabled (GL_DEPTH_TEST): glDisable(GL_DEPTH_TEST)
		else: glEnable(GL_DEPTH_TEST)

		glDepthFunc(GL_LESS)

		#glDepthFunc(GL_LESS)
	
	#camera control
	cameraSpeed = 0.05
	if glfw.get_key( window, glfw.KEY_UP ) == glfw.PRESS:
		position += cameraSpeed * front 
	if glfw.get_key( window, glfw.KEY_DOWN ) == glfw.PRESS:
		position -= cameraSpeed * front
	if glfw.get_key( window, glfw.KEY_RIGHT ) == glfw.PRESS:
		position -= glm.normalize(glm.cross(position, up)) * cameraSpeed
	if glfw.get_key( window, glfw.KEY_LEFT ) == glfw.PRESS:
		position += glm.normalize(glm.cross(position, up)) * cameraSpeed



def main():
	if not opengl_init():
		return
	
	#setting input modes (using keyboard+mouse)
	glfw.set_input_mode(window,glfw.STICKY_KEYS,GL_TRUE)
	glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)
	
	#setting callback functions
	glfw.set_key_callback(window,key_events)
	glfw.set_cursor_pos_callback(window,mouse_events)
	
	vertex_array_id = glGenVertexArrays(1)
	glBindVertexArray( vertex_array_id )

	program_id = common.LoadShaders( "./shaders/CubeOfTriads/TransformVertexShader.vertexshader",
		"./shaders/CubeOfTriads/ColorFragmentShader.fragmentshader" )
	
	# Get a handle for our "MVP" uniform
	matrix_id= glGetUniformLocation(program_id, "MVP");

	# Projection matrix : 45 Field of View, 4:3 ratio, display range : 0.1 unit <-> 100 units
	projection = glm.perspective(45.0, 4.0 / 3.0, 0.1, 100.0)
	
	# Camera matrix
	view = glm.lookAt(position, position+front, (0,1,0)) 
	
	# Model matrix : an identity matrix (model will be at the origin)
	model = glm.mat4(1.0)
	
	vertex_data = [ 
		-1.0,-1.0,-1.0,
		-1.0,-1.0, 1.0,
		-1.0, 1.0, 1.0,
		 1.0, 1.0,-1.0,
		-1.0,-1.0,-1.0,
		-1.0, 1.0,-1.0,
		 1.0,-1.0, 1.0,
		-1.0,-1.0,-1.0,
		 1.0,-1.0,-1.0,
		 1.0, 1.0,-1.0,
		 1.0,-1.0,-1.0,
		-1.0,-1.0,-1.0,
		-1.0,-1.0,-1.0,
		-1.0, 1.0, 1.0,
		-1.0, 1.0,-1.0,
		 1.0,-1.0, 1.0,
		-1.0,-1.0, 1.0,
		-1.0,-1.0,-1.0,
		-1.0, 1.0, 1.0,
		-1.0,-1.0, 1.0,
		 1.0,-1.0, 1.0,
		 1.0, 1.0, 1.0,
		 1.0,-1.0,-1.0,
		 1.0, 1.0,-1.0,
		 1.0,-1.0,-1.0,
		 1.0, 1.0, 1.0,
		 1.0,-1.0, 1.0,
		 1.0, 1.0, 1.0,
		 1.0, 1.0,-1.0,
		-1.0, 1.0,-1.0,
		 1.0, 1.0, 1.0,
		-1.0, 1.0,-1.0,
		-1.0, 1.0, 1.0,
		 1.0, 1.0, 1.0,
		-1.0, 1.0, 1.0,
		 1.0,-1.0, 1.0]

	# One color for each vertex. They were generated randomly.
	color_data = [ 
		0.583,  0.771,  0.014,
		0.609,  0.115,  0.436,
		0.327,  0.483,  0.844,
		0.822,  0.569,  0.201,
		0.435,  0.602,  0.223,
		0.310,  0.747,  0.185,
		0.597,  0.770,  0.761,
		0.559,  0.436,  0.730,
		0.359,  0.583,  0.152,
		0.483,  0.596,  0.789,
		0.559,  0.861,  0.639,
		0.195,  0.548,  0.859,
		0.014,  0.184,  0.576,
		0.771,  0.328,  0.970,
		0.406,  0.615,  0.116,
		0.676,  0.977,  0.133,
		0.971,  0.572,  0.833,
		0.140,  0.616,  0.489,
		0.997,  0.513,  0.064,
		0.945,  0.719,  0.592,
		0.543,  0.021,  0.978,
		0.279,  0.317,  0.505,
		0.167,  0.620,  0.077,
		0.347,  0.857,  0.137,
		0.055,  0.953,  0.042,
		0.714,  0.505,  0.345,
		0.783,  0.290,  0.734,
		0.722,  0.645,  0.174,
		0.302,  0.455,  0.848,
		0.225,  0.587,  0.040,
		0.517,  0.713,  0.338,
		0.053,  0.959,  0.120,
		0.393,  0.621,  0.362,
		0.673,  0.211,  0.457,
		0.820,  0.883,  0.371,
		0.982,  0.099,  0.879]

	
	vertex_buffer = glGenBuffers(1);
	
	# GLFloat = c_types.c_float
	array_type = GLfloat * len(vertex_data)
	glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer)
	glBufferData(GL_ARRAY_BUFFER, len(vertex_data) * 4, array_type(*vertex_data), GL_STATIC_DRAW)
	

	color_buffer = glGenBuffers(1)
	array_type = GLfloat * len(color_data)
	glBindBuffer(GL_ARRAY_BUFFER, color_buffer)
	glBufferData(GL_ARRAY_BUFFER, len(color_data) * 4, array_type(*color_data), GL_STATIC_DRAW)
	
	while glfw.get_key(window,glfw.KEY_ESCAPE) != glfw.PRESS and not glfw.window_should_close(window):
		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

		glUseProgram(program_id)

		view = glm.lookAt(position, position+front,	up)
		mvp = projection * view * model

		glUniformMatrix4fv(matrix_id, 1, GL_FALSE, glm.value_ptr(mvp))

		glEnableVertexAttribArray(0)
		glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer);
		glVertexAttribPointer(
			0,                  # attribute 0. No particular reason for 0, but must match the layout in the shader.
			3,                  # len(vertex_data)
			GL_FLOAT,           # type
			GL_FALSE,           # ormalized?
			0,                  # stride
			null           		# array buffer offset (c_type == void*)
			)

		glEnableVertexAttribArray(1)
		glBindBuffer(GL_ARRAY_BUFFER, color_buffer);
		glVertexAttribPointer(
			1,
			3,
			GL_FLOAT,
			GL_FALSE,
			0,
			null
			)
		
		# Draw the cube !
		glDrawArrays(GL_TRIANGLES, 0, 12*3)

		glDisableVertexAttribArray(0)
		glDisableVertexAttribArray(1)
	
		glfw.swap_buffers(window)

		glfw.poll_events()

	glDeleteBuffers(1, [vertex_buffer])
	glDeleteBuffers(1, [color_buffer])
	glDeleteProgram(program_id)
	glDeleteVertexArrays(1, [vertex_array_id])
	glfw.terminate()

if __name__ == "__main__":
	main()
