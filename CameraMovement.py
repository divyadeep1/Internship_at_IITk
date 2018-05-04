""" Camera Movement using keyboard and mouse
"""

from OpenGL.GL import *
from OpenGL.GL.ARB import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.GLUT.special import *
from OpenGL.GL.shaders import *
from glew_wish import *

import cube
import math
import glm
import common
import glfw
import sys
import os
import params


def opengl_init():
	window = params.window
	# Initialize the library
	if not glfw.init():
		print("Failed to initialize GLFW\n",file=sys.stderr)
		return False

	# Open Window and create its OpenGL context
	params.window = glfw.create_window(1024, 768, "Tutorial 03", None, None)
	glfw.window_hint(glfw.SAMPLES, 4)
	glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
	glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
	glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)
	glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

	if not params.window:
		print("Failed to open GLFW window. If you have an Intel GPU, they are not 3.3 compatible. Try the 2.1 version of the tutorials.\n",file=sys.stderr)
		glfw.terminate()
		return False
	
	glfw.set_input_mode(params.window,glfw.STICKY_KEYS,GL_TRUE)
	glfw.set_input_mode(params.window, glfw.CURSOR, glfw.CURSOR_DISABLED)
	
	#setting callback functions
	glfw.set_key_callback(params.window,key_events)
	glfw.set_cursor_pos_callback(params.window,mouse_events)
	
	# Initialize GLEW
	glfw.make_context_current(params.window)
	glewExperimental = True

	# GLEW is a framework for testing extension availability.  Please see tutorial notes for
	# more information including why can remove this code.
	if glewInit() != GLEW_OK:
		print("Failed to initialize GLEW\n",file=sys.stderr);
		return False
	return True

def mvp_init():
	projection = glm.perspective(45.0, 4.0 / 3.0, 0.1, 100.0)
	view = glm.lookAt(params.position, params.position+params.front, (0,1,0)) 
	model = glm.mat4(1.0)
	return model, view, projection

def mouse_events(window, xpos, ypos):
	
	if params.firstmouse:
		params.lastX=xpos
		params.lastY=ypos
		params.firstmouse = False
	mousespeed = 0.005
	
	xOffset =  (xpos - params.lastX)
	yOffset = (params.lastY - ypos)
	
	params.lastX = xpos
	params.lastY = ypos
	
	params.yaw -= (xOffset * mousespeed)
	params.pitch += (yOffset * mousespeed)
	
	#if pitch>=89:
	#	pitch = 89
	#if pitch<=-89:
	#	pitch = -89
		
	params.front.x = math.cos(params.pitch) * math.sin(params.yaw)
	params.front.y = math.sin(params.pitch)
	params.front.z = math.cos(params.pitch) * math.cos(params.yaw)
	
def key_events(window,key,scancode,action,mods):
	#depth test
	if action == glfw.PRESS and key == glfw.KEY_D:
		if glIsEnabled (GL_DEPTH_TEST): glDisable(GL_DEPTH_TEST)
		else: glEnable(GL_DEPTH_TEST)

		glDepthFunc(GL_LESS)

		#glDepthFunc(GL_LESS)
	
	#camera control
	cameraSpeed = 0.05
	if glfw.get_key( params.window, glfw.KEY_UP ) == glfw.PRESS:
		params.position += cameraSpeed * params.front 
	if glfw.get_key( params.window, glfw.KEY_DOWN ) == glfw.PRESS:
		params.position -= cameraSpeed * params.front
	if glfw.get_key( params.window, glfw.KEY_RIGHT ) == glfw.PRESS:
		params.position -= glm.normalize(glm.cross(params.position, params.up)) * cameraSpeed
	if glfw.get_key( params.window, glfw.KEY_LEFT ) == glfw.PRESS:
		params.position += glm.normalize(glm.cross(params.position, params.up)) * cameraSpeed



def main():
	if not opengl_init():
		return

	program_id = common.LoadShaders( "./shaders/CubeOfTriads/TransformVertexShader.vertexshader",
		"./shaders/CubeOfTriads/ColorFragmentShader.fragmentshader" )
	
	# Get a handle for our "MVP" uniform
	matrix_id= glGetUniformLocation(program_id, "MVP");

	m, v, p = mvp_init()	
	c = cube.Cube(m, v, p)
	
	vertex_buffer = glGenBuffers(1);
	array_type = GLfloat * len(c.vertices)
	glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer)
	glBufferData(GL_ARRAY_BUFFER, len(c.vertices) * 4, array_type(*c.vertices), GL_STATIC_DRAW)
	

	color_buffer = glGenBuffers(1)
	array_type = GLfloat * len(c.colors)
	glBindBuffer(GL_ARRAY_BUFFER, color_buffer)
	glBufferData(GL_ARRAY_BUFFER, len(c.colors) * 4, array_type(*c.colors), GL_STATIC_DRAW)

	while glfw.get_key(params.window,glfw.KEY_ESCAPE) != glfw.PRESS and not glfw.window_should_close(params.window):
		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

		glUseProgram(program_id)

		c.view = glm.lookAt(params.position, params.position+params.front, params.up)

		c.render(program_id, vertex_buffer, color_buffer)
		glDisableVertexAttribArray(0)
		glDisableVertexAttribArray(1)
	
		glfw.swap_buffers(params.window)

		glfw.poll_events()

	glDeleteBuffers(1, [vertex_buffer])
	glDeleteBuffers(1, [color_buffer])
	glDeleteProgram(program_id)
	glfw.terminate()

if __name__ == "__main__":
	main()
