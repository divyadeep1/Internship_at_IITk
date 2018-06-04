""" Camera Movement using keyboard and mouse
"""

from OpenGL.GL import *
from OpenGL.GL.ARB import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.GLUT.special import *
from OpenGL.GL.shaders import *
from glew_wish import *

import cube_test_3 as cube
import math
import glm
import common
import glfw
import sys
import os
import params
import Shaders

def main():
	if not common.opengl_init():
		return
	vertex_file_path = "./shaders/CubeOfTriads/TransformVertexShader.vertexshader"
	fragment_file_path = "./shaders/CubeOfTriads/ColorFragmentShader.fragmentshader"
	s = Shaders.Shader(vertex_file_path, fragment_file_path)
	c = cube.Cube(s)
	while glfw.get_key(params.window,glfw.KEY_ESCAPE) != glfw.PRESS and not glfw.window_should_close(params.window):
		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
		c.render()
		glfw.swap_buffers(params.window)
		glfw.poll_events()
	glfw.terminate()
	c.release()

if __name__ == "__main__":
	main()
