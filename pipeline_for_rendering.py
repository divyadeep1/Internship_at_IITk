""" Camera Movement using keyboard and mouse
"""

from OpenGL.GL import *
from OpenGL.GL.ARB import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.GLUT.special import *
from OpenGL.GL.shaders import *
from glew_wish import *

import ply_model as cube
import common
import glfw
import params
import Shaders


def main():
	path = './PLY source files/Generated/'
	files = os.listdir(path)
	for file_name in files:
		if file_name in ["test","aha815-lvl1-li-bl-lg.png"]:
			continue
		try:
			if not common.opengl_init():
				return
			vertex_file_path = "./shaders/PlyTest/LightVertexShader.vertexshader"
			fragment_file_path = "./shaders/PlyTest/LightFragmentShader.fragmentshader"
		#	vertex_file_path = "./shaders/PlyTest/shadow/StandardColorShading.vertexshader"
		#	fragment_file_path = "./shaders/PlyTest/shadow/StandardColorShading.fragmentshader"
			s = Shaders.Shader(vertex_file_path, fragment_file_path)
			params.screenshot_taken = False
			#f = "{}_ply".format(file_name)
			c = cube.Cube(s,file_name[:-4])
			while glfw.get_key(params.window,glfw.KEY_ESCAPE) != glfw.PRESS and not glfw.window_should_close(params.window) and not params.screenshot_taken:
				glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
				c.render()
				glfw.swap_buffers(params.window)
				glfw.poll_events()
			glfw.terminate()
			c.release()
		except Exception as e:
			print("Failed for file: ",file_name)
			print("Exception: ", str(e))
			break

if __name__ == "__main__":
	main()
