from OpenGL.GL import *
from OpenGL.GL.ARB import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.GLUT.special import *
from OpenGL.GL.shaders import *

from plyfile import PlyData

import params
import glm
import pandas as pd
import numpy as np
import math
import Shaders

null = c_void_p(0)

class Cube():
	def __init__(self, Shader):
		pd = PlyData.read("./PLY source files/co_ordinates_for_struct.ply")
		self.vertices = []
		self.faces = []
		self.normals = []
		max_x = max_y = max_z = min_x = min_y = min_z = 0
		#Get vertices and normals
		for i in pd.elements[0]:
			self.vertices.append(float(i[0])/16)
			max_x = max(float(i[0]), max_x)
			min_x = min(float(i[0]), min_x)
			self.vertices.append(float(i[1])/16)
			max_y = max(float(i[1]), max_y)
			min_y = min(float(i[1]), min_y)
			self.vertices.append(float(i[2])/16)
			max_z = max(float(i[2]), max_z)
			min_z = min(float(i[2]), min_z)
			self.normals.append(float(i[3]))
			self.normals.append(float(i[4]))
			self.normals.append(float(i[5]))
		print(max_x , max_y , max_z , min_x , min_y , min_z)

		"""
		for v in plane_vertices:
			self.vertices.append(v)
		k = len(self.faces)
		for f in plane_faces:
			self.faces.append(f+k)
		for n in plane_normals:
			self.normals.append(n)
		"""
		
		
		self.shader = Shader
		
		
		self.vertex_buffer = glGenBuffers(1)
		array_type = GLfloat * len(self.vertices)
		glBindBuffer(GL_ARRAY_BUFFER, self.vertex_buffer)
		glBufferData(GL_ARRAY_BUFFER, len(self.vertices) * 4, array_type(*self.vertices), GL_STATIC_DRAW)
		
		self.normal_buffer = glGenBuffers(1)
		array_type = GLfloat * len(self.normals)
		glBindBuffer(GL_ARRAY_BUFFER, self.normal_buffer)
		glBufferData(GL_ARRAY_BUFFER, len(self.normals) * 4, array_type(*self.normals), GL_STATIC_DRAW)
		
		######DIFFERENT CODE FROM cube_test_1.py file BEGINS######

		# Shadow texture + framebufferobject
		self.shadow_shader = Shaders.Shader('./shaders/PlyTest/shadow/StandardShadowShading.vertexshader',
				                            './shaders/PlyTest/shadow/StandardShadowShading.fragmentshader')
		self.depthMapFBO = glGenFramebuffers(1)
		self.SHADOW_WIDTH = 1024
		self.SHADOW_HEIGHT = 1024

		self.depthMap = glGenTextures(1)
		glBindTexture(GL_TEXTURE_2D, self.depthMap)
		glTexImage2D(GL_TEXTURE_2D, 0, GL_DEPTH_COMPONENT, self.SHADOW_WIDTH,
				     self.SHADOW_HEIGHT, 0, GL_DEPTH_COMPONENT, GL_FLOAT, null)
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_BORDER)
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_BORDER)
		borderColor = [1.0, 1.0, 1.0, 1.0]
		glTexParameterfv(GL_TEXTURE_2D, GL_TEXTURE_BORDER_COLOR, borderColor)

		# attach depth texture as FBO's depth buffer
		glBindFramebuffer(GL_FRAMEBUFFER, self.depthMapFBO)
		glFramebufferTexture2D(
			GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT, GL_TEXTURE_2D, self.depthMap, 0)
		glDrawBuffer(GL_NONE)
		glReadBuffer(GL_NONE)
		glBindFramebuffer(GL_FRAMEBUFFER, 0)
		if(glCheckFramebufferStatus(GL_FRAMEBUFFER) == GL_FRAMEBUFFER_COMPLETE):
			print("Framebuffer for rendering shadow map successfully created!")
		else:
			print("Framebuffer creation failed")
			return
	def rotate(self,angle,axis):
		self.model = glm.rotate(self.model, angle, axis)
		
	def translate(self,position):
		self.model = glm.translate(self.model, position)
	
	def mvp(self):
		return (params.projection() * params.view() * params.model())
		
	def render(self):
		light_color = glm.vec3(1.0,1.0,1.0)
		params.t = (params.t+1)%1000000000
		light_position = glm.vec3(100.0,10.0,50.0)#glm.vec3(50*math.sin(0.0002*params.t), 20.0, 50*math.cos(0.0002*params.t))#

		glUseProgram(self.shader.ID)
		glUniformMatrix4fv(glGetUniformLocation(self.shader.ID, "MVP"), 1, GL_FALSE, glm.value_ptr(self.mvp()))
		glUniformMatrix4fv(glGetUniformLocation(self.shader.ID, "model"), 1, GL_FALSE, glm.value_ptr(params.model()))
		glUniform3f(glGetUniformLocation(self.shader.ID, "lightColor"), light_color.x, light_color.y,
		light_color.z)
		glUniform3f(glGetUniformLocation(self.shader.ID, "lightPosition"), light_position.x, light_position.y, light_position.z)
		glUniform3f(glGetUniformLocation(self.shader.ID, "viewPos"), params.position.x, params.position.y, params.position.z)
		
		
		glEnableVertexAttribArray(0)
		glBindBuffer(GL_ARRAY_BUFFER, self.vertex_buffer);
		glVertexAttribPointer(0, 3,	GL_FLOAT, GL_FALSE,	0, null)
		
		glEnableVertexAttribArray(1)
		glBindBuffer(GL_ARRAY_BUFFER, self.normal_buffer);
		glVertexAttribPointer(1, 3,	GL_FLOAT, GL_FALSE,	0, null)
		
		# Draw the figure !
		glDrawArrays(GL_QUADS, 0, int(len(self.vertices)/3))
		#glDrawElements(GL_QUADS, len(self.faces), GL_UNSIGNED_INT, None) #Important! - The last arguement will be 'None', not 0!
		glDisableVertexAttribArray(0)
		glDisableVertexAttribArray(1)
		#glDisableVertexAttribArray(2)
		glEnable(GL_DEPTH_TEST)

	def render_with_shadows(self):
		params.t = (params.t+1) % 1000000000
		params.light_position = glm.vec3(30*math.sin(0.0005*params.t), 10.0, 50.0*math.cos(0.0005*params.t))#glm.vec3(20.0,20.0,10.0)

		######RENDERING DEPTH OF SCENE FROM LIGHT'S PERSPECTIVE######
		glClearColor(0.1, 0.1, 0.1, 1.0)
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

		# The lightProjection matrix is actually static but is kept in the render loop for the sake of convinience and easy access
		lightProjection = glm.ortho(-10.0, 10.0, -10.0,
				                    10.0, params.near_plane, params.far_plane)
		lightView = glm.lookAt(params.light_position,
				               glm.vec3(10.0,10.0,0.0), glm.vec3(0.0, 1.0, 0.0))
		lightSpaceMatrix = lightProjection * lightView

		###render scene from light's point of view###
		glUseProgram(self.shadow_shader.ID)
		glUniformMatrix4fv(glGetUniformLocation(self.shadow_shader.ID, "lightSpaceMatrix"),
				           1,
				           GL_FALSE,
				           glm.value_ptr(lightSpaceMatrix))
		glViewport(0, 0, self.SHADOW_WIDTH, self.SHADOW_HEIGHT)
		glEnable(GL_CULL_FACE)
		# glCullFace(GL_BACK)
		# Culling the front face to make shadow map that does not suffer from peter-panning
		glCullFace(GL_FRONT)
		glBindFramebuffer(GL_FRAMEBUFFER, self.depthMapFBO)
		glClear(GL_DEPTH_BUFFER_BIT)

		glEnableVertexAttribArray(0)
		glBindBuffer(GL_ARRAY_BUFFER, self.vertex_buffer)
		glVertexAttribPointer(0, 3,	GL_FLOAT, GL_FALSE,	0, null)

		glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.element_buffer)
		glDrawElements(GL_QUADS, len(self.faces), GL_UNSIGNED_INT, None)

		glDisableVertexAttribArray(0)
		glDisableVertexAttribArray(1)
		
		glEnableVertexAttribArray(0)
		glBindBuffer(GL_ARRAY_BUFFER, self.plane_vertex_buffer);
		glVertexAttribPointer(0, 3,	GL_FLOAT, GL_FALSE,	0, null)
		glDrawArrays(GL_QUADS, 0, 8)

		glDisableVertexAttribArray(0)
		glBindFramebuffer(GL_FRAMEBUFFER, 0)
		glCullFace(GL_BACK)

		###reset viewport###
		glViewport(0, 0, 1024, 768)
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

		######RENDERING SCENE AS NORMAL USING SHADOWS CREATED######

		glUseProgram(self.shader.ID)
		glUniformMatrix4fv(glGetUniformLocation(
			self.shader.ID, "model"), 1, GL_FALSE, glm.value_ptr(params.model()))
		glUniformMatrix4fv(glGetUniformLocation(
			self.shader.ID, "MVP"), 1, GL_FALSE, glm.value_ptr(self.mvp()))
		glUniform3f(glGetUniformLocation(self.shader.ID, "lightColor"),
				    params.light_color.x,
				    params.light_color.y,
				    params.light_color.z
				    )
		glUniform3f(glGetUniformLocation(self.shader.ID, "lightPosition"),
				    params.light_position.x,
				    params.light_position.y,
				    params.light_position.z
				    )
		glUniform3f(glGetUniformLocation(self.shader.ID, "viewPos"),
				    params.position.x, params.position.y, params.position.z)
		glUniformMatrix4fv(glGetUniformLocation(
			self.shader.ID, "lightSpaceMatrix"), 1, GL_FALSE, glm.value_ptr(lightSpaceMatrix))
		glActiveTexture(GL_TEXTURE0)
		glBindTexture(GL_TEXTURE_2D, self.depthMap)
		glUniform1i(glGetUniformLocation(self.shader.ID, "shadowMap"), 0)

		glEnableVertexAttribArray(0)
		glBindBuffer(GL_ARRAY_BUFFER, self.vertex_buffer)
		glVertexAttribPointer(0, 3,	GL_FLOAT, GL_FALSE,	0, null)

#		glEnableVertexAttribArray(1)
#		glBindBuffer(GL_ARRAY_BUFFER, self.color_buffer)
#		glVertexAttribPointer(1, 3,	GL_FLOAT, GL_FALSE,	0, null)

		glEnableVertexAttribArray(1)
		glBindBuffer(GL_ARRAY_BUFFER, self.normal_buffer)
		glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 0, null)
		
		glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.element_buffer)
		
		# Draw the cube !
		glDrawElements(GL_QUADS, len(self.faces), GL_UNSIGNED_INT, None)
		glEnable(GL_DEPTH_TEST)
		glDisableVertexAttribArray(0)
		glDisableVertexAttribArray(1)
		#glDisableVertexAttribArray(2)
		
		glEnableVertexAttribArray(0)
		glBindBuffer(GL_ARRAY_BUFFER, self.plane_vertex_buffer);
		glVertexAttribPointer(0, 3,	GL_FLOAT, GL_FALSE,	0, null)
		
		glEnableVertexAttribArray(1)
		glBindBuffer(GL_ARRAY_BUFFER, self.plane_normal_buffer);
		glVertexAttribPointer(1, 3,	GL_FLOAT, GL_FALSE,	0, null)
		
		glDrawArrays(GL_QUADS, 0, 8)
		glDisableVertexAttribArray(0)
		glDisableVertexAttribArray(1)
		glEnable(GL_DEPTH_TEST)




	def release(self):
		glDeleteBuffers(1, [self.vertex_buffer])
		#glDeleteBuffers(1, [self.color_buffer])
		glDeleteBuffers(1, [self.normal_buffer])
		print("Cube's buffers deleted")
