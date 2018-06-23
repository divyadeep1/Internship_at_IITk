from OpenGL.GL import *
from OpenGL.GL.ARB import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.GLUT.special import *
from OpenGL.GL.shaders import *

from plyfile import PlyData
from PIL import Image
import params
import glm
import pandas as pd
import numpy as np
import math
import Shaders
import datetime
import os
null = c_void_p(0)

class backproject():
	def __init__(self, Shader, fname):
#		pd = PlyData.read("./PLY source files/3d_render raghav sir.ply")
		path_to_input_file = "./PLY source files/Generated/"
		self.file_name = fname
		dot_ply = ".ply"
		pd = PlyData.read(path_to_input_file+self.file_name+dot_ply)
		self.vertices = []
		self.faces = []
		self.max_x = self.max_y = self.max_z = min_x = min_y = min_z = 0
		self.cx = self.cy = self.cz = 0
		ctr = 0
		scale = 0.04
		#Get vertices and normals
		for i in pd.elements[0]:
			self.vertices.append(scale*float(i[0]))
			self.cx += scale*float(i[0])
			self.max_x = max(scale*float(i[0]), self.max_x)
			min_x = min(scale*float(i[0]), min_x)
			self.vertices.append(scale*float(i[1]))
			self.cy += scale*float(i[1])
			self.max_y = max(scale*float(i[1]), self.max_y)
			min_y = min(scale*float(i[1]), min_y)
			self.vertices.append(scale*float(i[2]))
			self.cz += scale*float(i[2])
			self.max_z = max(scale*float(i[2]), self.max_z)
			min_z = min(scale*float(i[2]), min_z)
			ctr += 1
		#print(max_x , max_y , max_z , min_x , min_y , min_z)
		self.cx = self.cx/ctr
		self.cy = self.cy/ctr
		self.cz = self.cz/ctr
		
		#Get faces
		for i in pd.elements[1]:
			#print(i[0])
			for j in range(4):
				self.faces.append(i[0][j])

		self.screenshot_timer = 0
		
		self.shader = Shader
		
		self.vertex_buffer = glGenBuffers(1)
		array_type = GLfloat * len(self.vertices)
		glBindBuffer(GL_ARRAY_BUFFER, self.vertex_buffer)
		glBufferData(GL_ARRAY_BUFFER, len(self.vertices) * 4, array_type(*self.vertices), GL_STATIC_DRAW)
		
		self.element_buffer = glGenBuffers(1)
		array_type = GLuint * len(self.faces)
		glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.element_buffer)
		glBufferData(GL_ELEMENT_ARRAY_BUFFER, len(self.faces) * 4, array_type(*self.faces), GL_STATIC_DRAW)

	def mvp(self):
		return (params.ortho_projection() * params.ortho_view() * params.model())

	def take_screenshot(self):
		path_to_output_screenshot = "./Screenshots/Backprojections"
		print("Taking sceenshot")
		data = glReadPixels(0, 0, 1024, 768, GL_RGB, GL_UNSIGNED_BYTE)
		image = Image.frombytes("RGB", (1024, 768), data)
		image = image.transpose(Image.FLIP_TOP_BOTTOM)
		name = str(self.file_name[:-4]) + ".png"
		#name = "co_ordinates_line0.png"
		image.save(os.path.join(path_to_output_screenshot, name), format='png')
		params.screenshot_taken = True
		print("Sceenshot taken")

	def render(self):
		glUseProgram(self.shader.ID)
		glUniformMatrix4fv(glGetUniformLocation(self.shader.ID, "MVP"), 1, GL_FALSE, glm.value_ptr(self.mvp()))
		
		glEnableVertexAttribArray(0)
		glBindBuffer(GL_ARRAY_BUFFER, self.vertex_buffer);
		glVertexAttribPointer(0, 3,	GL_FLOAT, GL_FALSE,	0, null)
		
		glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.element_buffer)
		
		
		# Draw the figure !
		glDrawElements(GL_QUADS, len(self.faces), GL_UNSIGNED_INT, None) #Important! - The last arguement will be 'None', not 0!
		glDisableVertexAttribArray(0)
		glEnable(GL_DEPTH_TEST)

		if self.screenshot_timer==100:
			self.take_screenshot()
			self.screenshot_timer += 1
		else:
			if self.screenshot_timer<100:
				self.screenshot_timer += 1

	def release(self):
		glDeleteBuffers(1, [self.vertex_buffer])
		print("Cube's buffers deleted")
