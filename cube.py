from OpenGL.GL import *
from OpenGL.GL.ARB import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.GLUT.special import *
from OpenGL.GL.shaders import *

import params
import glm

null = c_void_p(0)

class Cube():
	def __init__(self, Shader):
		self.vertices = [ 
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
		self.colors = [ 
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
		
		self.shader = Shader
		self.vertex_buffer = glGenBuffers(1);
		array_type = GLfloat * len(self.vertices)
		glBindBuffer(GL_ARRAY_BUFFER, self.vertex_buffer)
		glBufferData(GL_ARRAY_BUFFER, len(self.vertices) * 4, array_type(*self.vertices), GL_STATIC_DRAW)
	

		self.color_buffer = glGenBuffers(1)
		array_type = GLfloat * len(self.colors)
		glBindBuffer(GL_ARRAY_BUFFER, self.color_buffer)
		glBufferData(GL_ARRAY_BUFFER, len(self.colors) * 4, array_type(*self.colors), GL_STATIC_DRAW)
		
	def rotate(self,angle,axis):
		self.model = glm.rotate(self.model, angle, axis)
		
	def translate(self,position):
		self.model = glm.translate(self.model, position)
	
	def mvp(self):
		return (params.projection() * params.view() * params.model())
		
	def render(self):
		glUseProgram(self.shader.ID)
		glUniformMatrix4fv(glGetUniformLocation(self.shader.ID, "MVP"), 1, GL_FALSE, glm.value_ptr(self.mvp()))

		glEnableVertexAttribArray(0)
		glBindBuffer(GL_ARRAY_BUFFER, self.vertex_buffer);
		glVertexAttribPointer(0, 3,	GL_FLOAT, GL_FALSE,	0, null)

		glEnableVertexAttribArray(1)
		glBindBuffer(GL_ARRAY_BUFFER, self.color_buffer);
		glVertexAttribPointer(1, 3,	GL_FLOAT, GL_FALSE,	0, null)
		
		# Draw the cube !
		glDrawArrays(GL_TRIANGLES, 0, 12*3)
		glDisableVertexAttribArray(0)
		glDisableVertexAttribArray(1)
		glEnable(GL_DEPTH_TEST)
		
	def release(self):
		glDeleteBuffers(1, [self.vertex_buffer])
		glDeleteBuffers(1, [self.color_buffer])
		print("Cube's buffers deleted")
