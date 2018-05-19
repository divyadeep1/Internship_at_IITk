from OpenGL.GL import *
from OpenGL.GL.ARB import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.GLUT.special import *
from OpenGL.GL.shaders import *
from glew_wish import *

import glfw
import sys
import os
import params
import glm
import math

frame_count = 0

def pre_frame():
    pass
    
def post_fram():
    frame_count += 1

def disable_vsyc():
    import glfw
    glfw.swap_interval(0)

def enable_vsyc():
    import glfw
    glfw.swap_interval(1)

def opengl_init():
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

def mouse_events(window, xpos, ypos):
	global first_mouse_event
	
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
	#if action == glfw.PRESS and key == glfw.KEY_D:
	#	if glIsEnabled (GL_DEPTH_TEST): glDisable(GL_DEPTH_TEST)
	#	else: glEnable(GL_DEPTH_TEST)

	#	glDepthFunc(GL_LESS)

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

#mvp_init() removed
