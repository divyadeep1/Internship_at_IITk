from OpenGL.GL import *
from OpenGL.GL.ARB import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.GLUT.special import *
from OpenGL.GL.shaders import *
from glew_wish import *

from datetime import datetime
import glm
import Shaders
from PIL import Image
import glfw
import common
from plyfile import PlyData
import params
import backprojector

def main():
	if not common.opengl_init():
		return
	vertex_file_path = "./shaders/Backprojection/simplevs.vertexshader"
	fragment_file_path = "./shaders/Backprojection/simplefs.fragmentshader"
	s = Shaders.Shader(vertex_file_path, fragment_file_path)
	f = "test_ply"
	b = backprojector.backproject(s,f)
	while glfw.get_key(params.window,glfw.KEY_ESCAPE) != glfw.PRESS and not glfw.window_should_close(params.window):
		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
		b.render()
		glfw.swap_buffers(params.window)
		glfw.poll_events()
	b.release()
	s.release()
	glfw.terminate()

if __name__ == "__main__":
	main()

