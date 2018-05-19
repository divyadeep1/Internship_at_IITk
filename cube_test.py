from OpenGL.GL import *
from OpenGL.GL.ARB import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.GLUT.special import *
from OpenGL.GL.shaders import *

import params
import math
import glm

null = c_void_p(0)

class Cube():
	def __init__(self, Shader):
		self.vertices = [-1.0, -1.0, -1.0,
						 1.0, -1.0, -1.0,
						 1.0, 1.0, -1.0,
						 -1.0, 1.0, -1.0,
						 -1.0, -1.0, -1.0,
						 1.0, -1.0, -1.0, 
						 1.0, -1.0, 1.0, 
						 -1.0, -1.0, 1.0, 
						 1.0, -1.0, -1.0, 
						 1.0, 1.0, -1.0, 
						 1.0, 1.0, 1.0, 
						 1.0, -1.0, 1.0, 
						 -1.0, -1.0, -1.0, 
						 -1.0, 1.0, -1.0, 
						 -1.0, 1.0, 1.0, 
						 -1.0, -1.0, 1.0, 
						 1.0, 1.0, -1.0, 
						 -1.0, 1.0, -1.0, 
						 -1.0, 1.0, 1.0, 
						 1.0, 1.0, 1.0, 
						 -1.0, -1.0, 1.0, 
						 1.0, -1.0, 1.0, 
						 1.0, 1.0, 1.0, 
						 -1.0, 1.0, 1.0]
						 #100.0,-1.0,100.0,
						 #-100.0,-1.0,100.0,
						 #-100.0,-1.0,-100.0,
						 #100.0,-1.0,-100.0]
		
		self.colors = [0.67, 0.92, 0.46,
					   0.67, 0.92, 0.46,
					   0.67, 0.92, 0.46,
					   0.67, 0.92, 0.46,
		 			   0.29, 0.44, 0.19,
		 			   0.29, 0.44, 0.19,
		 			   0.29, 0.44, 0.19,
		 			   0.29, 0.44, 0.19,
		 			   0.4, 0.4, 0.48,
		 			   0.4, 0.4, 0.48,
		 			   0.4, 0.4, 0.48,
		 			   0.4, 0.4, 0.48,
		 			   0.53, 0.9, 0.98,
		 			   0.53, 0.9, 0.98,
		 			   0.53, 0.9, 0.98,
		 			   0.53, 0.9, 0.98,
		 			   0.99, 0.3, 0.15,
		 			   0.99, 0.3, 0.15,
		 			   0.99, 0.3, 0.15,
		 			   0.99, 0.3, 0.15,
		 			   0.2, 0.57, 0.76,
		 			   0.2, 0.57, 0.76,
		 			   0.2, 0.57, 0.76,
		 			   0.2, 0.57, 0.76]
		 			   #0.3, 0.3, 0.3,
		 			   #0.3, 0.3, 0.3,
		 			   #0.3, 0.3, 0.3,
		 			   #0.3, 0.3, 0.3]
		
		self.normals = [0.0,0.0,-1.0,
						0.0,0.0,-1.0,
						0.0,0.0,-1.0,
						0.0,0.0,-1.0,
						0.0,-1.0,0.0,
						0.0,-1.0,0.0,
						0.0,-1.0,0.0,
						0.0,-1.0,0.0,
						1.0,0.0,0.0,
						1.0,0.0,0.0,
						1.0,0.0,0.0,
						1.0,0.0,0.0,
						-1.0,0.0,0.0,
						-1.0,0.0,0.0,
						-1.0,0.0,0.0,
						-1.0,0.0,0.0,
						0.0,1.0,0.0,
						0.0,1.0,0.0,
						0.0,1.0,0.0,
						0.0,1.0,0.0,
						0.0,0.0,1.0,
						0.0,0.0,1.0,
						0.0,0.0,1.0,
						0.0,0.0,1.0,
						]
		
		
		self.shader = Shader
		
		self.vertex_buffer = glGenBuffers(1);
		array_type = GLfloat * len(self.vertices)
		glBindBuffer(GL_ARRAY_BUFFER, self.vertex_buffer)
		glBufferData(GL_ARRAY_BUFFER, len(self.vertices) * 4, array_type(*self.vertices), GL_STATIC_DRAW)
	
		self.color_buffer = glGenBuffers(1)
		array_type = GLfloat * len(self.colors)
		glBindBuffer(GL_ARRAY_BUFFER, self.color_buffer)
		glBufferData(GL_ARRAY_BUFFER, len(self.colors) * 4, array_type(*self.colors), GL_STATIC_DRAW)
		
		self.normal_buffer = glGenBuffers(1)
		array_type = GLfloat * len(self.normals)
		glBindBuffer(GL_ARRAY_BUFFER, self.normal_buffer)
		glBufferData(GL_ARRAY_BUFFER, len(self.normals) * 4, array_type(*self.normals), GL_STATIC_DRAW)
		
	def rotate(self,angle,axis):
		self.model = glm.rotate(self.model, angle, axis)
		
	def translate(self,position):	
		self.model = glm.translate(self.model, position)
	
	def mvp(self):
		return (params.projection() * params.view() * params.model())
		
	def render(self):
		glUseProgram(self.shader.ID)
		glUniformMatrix4fv(glGetUniformLocation(self.shader.ID, "model"), 1, GL_FALSE, glm.value_ptr(params.model()))
		glUniformMatrix4fv(glGetUniformLocation(self.shader.ID, "MVP"), 1, GL_FALSE, glm.value_ptr(self.mvp()))
		light_color = glm.vec3(1.0, 1.0, 1.0)
		glUniform3f(glGetUniformLocation(self.shader.ID, "lightColor"), light_color.x, light_color.y, light_color.z)
		params.t = (params.t+1)%1000000000
		light_position = glm.vec3(5*math.sin(0.0002*params.t), 1.0, 5*math.cos(0.0002*params.t))
		glUniform3f(glGetUniformLocation(self.shader.ID, "lightPosition"), light_position.x, light_position.y, light_position.z)
		glUniform3f(glGetUniformLocation(self.shader.ID, "viewPos"), params.position.x, params.position.y, params.position.z)

		glEnableVertexAttribArray(0)
		glBindBuffer(GL_ARRAY_BUFFER, self.vertex_buffer);
		glVertexAttribPointer(0, 3,	GL_FLOAT, GL_FALSE,	0, null)

		glEnableVertexAttribArray(1)
		glBindBuffer(GL_ARRAY_BUFFER, self.color_buffer);
		glVertexAttribPointer(1, 3,	GL_FLOAT, GL_FALSE,	0, null)
		
		glEnableVertexAttribArray(2)
		glBindBuffer(GL_ARRAY_BUFFER, self.normal_buffer);
		glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, 0, null)
		
		# Draw the cube !
		glDrawArrays(GL_QUADS, 0, 6*4)
		glEnable(GL_DEPTH_TEST)
		glDisableVertexAttribArray(0)
		glDisableVertexAttribArray(1)
		glDisableVertexAttribArray(2)
		
	def release(self):
		glDeleteBuffers(1, [self.vertex_buffer])
		glDeleteBuffers(1, [self.color_buffer])
		glDeleteBuffers(1, [self.normal_buffer])
		print("Cube's buffers deleted")

