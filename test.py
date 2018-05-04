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

def main():
	if not common.opengl_init():
		return
	
	program_id = common.LoadShaders( "./shaders/CubeOfTriads/TransformVertexShader.vertexshader",
		"./shaders/CubeOfTriads/ColorFragmentShader.fragmentshader" )
	
	m, v, p = common.mvp_init()	
	c = cube.Cube(m, v, p)

	while glfw.get_key(params.window,glfw.KEY_ESCAPE) != glfw.PRESS and not glfw.window_should_close(params.window):
		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

		glUseProgram(program_id)

		c.view = glm.lookAt(params.position, params.position+params.front, params.up)

		c.render(program_id, c.vertex_buffer, c.color_buffer)

		glfw.swap_buffers(params.window)

		glfw.poll_events()

	c.__del__()
	glDeleteProgram(program_id)
	glfw.terminate()

if __name__ == "__main__":
	main()
