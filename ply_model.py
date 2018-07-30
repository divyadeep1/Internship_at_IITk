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

class Cube():
	def __init__(self, Shader, fname):
#		pd = PlyData.read("./PLY source files/3d_render raghav sir.ply")
		path_to_input_file = "./PLY source files/Generated/"
		self.file_name = fname
		dot_ply = ".ply"
		pd = PlyData.read(path_to_input_file+self.file_name+dot_ply)
		self.vertices = []
		self.faces = []
		self.normals = []
		self.triads = []
		self.max_x = self.max_y = self.max_z = min_x = min_y = min_z = 0
		self.cx = self.cy = self.cz = 0
		ctr = 0
		scale = 0.02
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
			self.normals.append(float(i[3]))
			self.normals.append(float(i[4]))
			self.normals.append(float(i[5]))
			ctr += 1
		#print(max_x , max_y , max_z , min_x , min_y , min_z)
		self.cx = self.cx/ctr
		self.cy = self.cy/ctr
		self.cz = self.cz/ctr
		#params.position = glm.vec3(self.max_x/4,self.max_y/3,4*self.max_z)
		params.position = glm.vec3(self.cx,self.cy,self.cz*2)
		#plane vertices, faces and normals
		self.plane_vertices = [-100.0,50.0,0.0,
						  -100.0,-14.0,0.0,
						  100.0,-14.0,0.0,
						  100.0,50.0,0.0]
#						  100.0,-14.0,0.0,
#						  -100.0,-14.0,0.0,
#						  -100.0,-14.0,50.,
#						  100.0,-14.0,50.0]
		#self.plane_faces = [0,1,2,3,
		#			   4,5,6,7]
		self.plane_normals = [0,0,1,
						 0,0,1,
						 0,0,1,
						 0,0,1]
#						 0,1,0,
#						 0,1,0,
#						 0,1,0,
#						 0,1,0]
		
		#Get faces
		for i in pd.elements[1]:
			#print(i[0])
			for j in range(4):
				self.faces.append(i[0][j])
		
		
		print(len(pd.elements))
		#Get triads
		if(len(pd.elements)>2):
			for i in pd.elements[2]:
				for j in range(3):
					self.triads.append(i[0][j])
					self.triads.append(i[0][2])
		print(self.triads)
		"""
		for v in plane_vertices:
			self.vertices.append(v)
		k = len(self.faces)
		for f in plane_faces:
			self.faces.append(f+k)
		for n in plane_normals:
			self.normals.append(n)
		"""
		self.screenshot_timer = 0
		
		self.shader = Shader
		
		#self.vao = glGenVertexArrays(1)
		#glBindVertexArray(self.vao)
		
		self.vertex_buffer = glGenBuffers(1)
		array_type = GLfloat * len(self.vertices)
		glBindBuffer(GL_ARRAY_BUFFER, self.vertex_buffer)
		glBufferData(GL_ARRAY_BUFFER, len(self.vertices) * 4, array_type(*self.vertices), GL_STATIC_DRAW)
		
		self.normal_buffer = glGenBuffers(1)
		array_type = GLfloat * len(self.normals)
		glBindBuffer(GL_ARRAY_BUFFER, self.normal_buffer)
		glBufferData(GL_ARRAY_BUFFER, len(self.normals) * 4, array_type(*self.normals), GL_STATIC_DRAW)
		
		self.element_buffer = glGenBuffers(1)
		array_type = GLuint * len(self.faces)
		glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.element_buffer)
		glBufferData(GL_ELEMENT_ARRAY_BUFFER, len(self.faces) * 4, array_type(*self.faces), GL_STATIC_DRAW)
		
		if len(self.triads)>0:
			self.triad_buffer = glGenBuffers(1)
			array_type = GLuint * len(self.triads)
			glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.triad_buffer)
			glBufferData(GL_ELEMENT_ARRAY_BUFFER, len(self.triads) * 4, array_type(*self.triads), GL_STATIC_DRAW)
		
		#Plane's buffers:
		self.plane_vertex_buffer = glGenBuffers(1)
		array_type = GLfloat * len(self.plane_vertices)
		glBindBuffer(GL_ARRAY_BUFFER, self.plane_vertex_buffer)
		glBufferData(GL_ARRAY_BUFFER, len(self.plane_vertices) * 4, array_type(*self.plane_vertices), GL_STATIC_DRAW)
		
		self.plane_normal_buffer = glGenBuffers(1)
		array_type = GLfloat * len(self.plane_normals)
		glBindBuffer(GL_ARRAY_BUFFER, self.plane_normal_buffer)
		glBufferData(GL_ARRAY_BUFFER, len(self.plane_normals) * 4, array_type(*self.plane_normals), GL_STATIC_DRAW)
		
		######DIFFERENT CODE FROM cube_test_1.py file BEGINS######

		# Shadow texture + framebufferobject
		self.shadow_shader = Shaders.Shader('./shaders/PlyTest/shadow/StandardShadowShading.vertexshader',
				                            './shaders/PlyTest/shadow/StandardShadowShading.fragmentshader')
		self.depthMapFBO = glGenFramebuffers(1)
		self.SHADOW_WIDTH = 2046
		self.SHADOW_HEIGHT = 2046

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
			GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT, GL_TEXTURE_2D, self.depthMap, 3)
		glDrawBuffer(GL_NONE)
		glReadBuffer(GL_NONE)
		glBindFramebuffer(GL_FRAMEBUFFER, 0)
		if(glCheckFramebufferStatus(GL_FRAMEBUFFER) == GL_FRAMEBUFFER_COMPLETE):
			print("Framebuffer for rendering shadow map successfully created!")
		else:
			print("Framebuffer creation failed")
			return
		params.position = glm.vec3(8.34048, 2.24112, 15.9789)
		params.front = glm.vec3(0.00150267, 0.331372, -0.943499)

	
	def rotate(self,angle,axis):
		self.model = glm.rotate(self.model, angle, axis)
		
	def translate(self,position):
		self.model = glm.translate(self.model, position)
	
	def mvp(self):
		return (params.projection() * params.view() * params.model())

	def take_screenshot(self):
		path_to_output_screenshot = "./Screenshots/Bulk"
		print("Taking sceenshot")
		data = glReadPixels(0, 0, 1024, 768, GL_RGB, GL_UNSIGNED_BYTE)
		image = Image.frombytes("RGB", (1024, 768), data)
		image = image.transpose(Image.FLIP_TOP_BOTTOM)
		name = str(self.file_name[:-4]) + ".png"
		#name = "co_ordinates_line0.png"
		image.save(os.path.join(path_to_output_screenshot, name), format='png')
		params.screenshot_taken = True

	def render(self):
		light_color = glm.vec3(1.0,1.0,1.0)
		params.t = (params.t+1)%1000000000
		light_position = glm.vec3(-1.0,2.0,15.0)#glm.vec3(50*math.sin(0.0002*params.t), 20.0, 50*math.cos(0.0002*params.t))#

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
		
		#if self.screenshot_timer %5000 < 2500:
		glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.element_buffer)
		
		
		# Draw the figure !
		glDrawElements(GL_QUADS, len(self.faces), GL_UNSIGNED_INT, None) #Important! - The last arguement will be 'None', not 0!
		
		if(len(self.triads)>0):
			glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.triad_buffer)
			glDrawElements(GL_TRIANGLES, len(self.triads), GL_UNSIGNED_INT, None)
		
		glDisableVertexAttribArray(0)
		glDisableVertexAttribArray(1)
		#glDisableVertexAttribArray(2)
		glEnable(GL_DEPTH_TEST)


		#Draw the plane
		glEnableVertexAttribArray(0)
		glBindBuffer(GL_ARRAY_BUFFER, self.plane_vertex_buffer);
		glVertexAttribPointer(0, 3,	GL_FLOAT, GL_FALSE,	0, null)
		
		glEnableVertexAttribArray(1)
		glBindBuffer(GL_ARRAY_BUFFER, self.plane_normal_buffer);
		glVertexAttribPointer(1, 3,	GL_FLOAT, GL_FALSE,	0, null)
		
		glDrawArrays(GL_QUADS, 0, 8)
		glDisableVertexAttribArray(0)
		glDisableVertexAttribArray(1)
		if self.screenshot_timer==100:
			self.take_screenshot()
			self.screenshot_timer += 1
		else:
			if self.screenshot_timer!=100:
				self.screenshot_timer += 1

		#print(params.ortho_position, params.ortho_front)


	def render_with_shadows(self):
		params.t = (params.t+1) % 1000000000
		params.light_position = glm.vec3(10.0,-5.0,20.0)#glm.vec3(100.0,10.0,50.0)#glm.vec3(self.max_x*math.sin(0.0005*params.t), self.max_y*math.cos(0.0005*params.t), 2*self.max_z)#

		######RENDERING DEPTH OF SCENE FROM LIGHT'S PERSPECTIVE######
		glClearColor(0.1, 0.1, 0.1, 1.0)
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

		# The lightProjection matrix is actually static but is kept in the render loop for the sake of convinience and easy access
		lightProjection = glm.ortho(-20.0, 30.0, -20.0,
				                    30.0, params.near_plane, params.far_plane)
		lightView = glm.lookAt(params.light_position,
				               glm.vec3(self.cx,self.cy,self.cz), glm.vec3(0.0, 1.0, 0.0))
		lightSpaceMatrix = lightProjection * lightView
#		lightSpaceMatrix = lightSpaceMatrix * glm.mat4(
#							0.5, 0.0, 0.0, 0.0,
#							0.0, 0.5, 0.0, 0.0,
#							0.0, 0.0, 0.5, 0.0,
#							0.5, 0.5, 0.5, 1.0
#							)
		###render scene from light's point of view###
		glUseProgram(self.shadow_shader.ID)
		glUniformMatrix4fv(glGetUniformLocation(self.shadow_shader.ID, "lightSpaceMatrix"),
				           1,
				           GL_FALSE,
				           glm.value_ptr(lightSpaceMatrix))
		glViewport(0, 0, self.SHADOW_WIDTH, self.SHADOW_HEIGHT)
		glEnable(GL_CULL_FACE)
		#glCullFace(GL_BACK)
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
		
#		if self.screenshot_timer==100:
#			print("Calling backproject...")
#			backproject(self.vertex_buffer,
#						len(self.vertices),
#						self.normal_buffer,
#						len(self.normals),
#						self.element_buffer,
#						len(self.faces),
#						self.cx,
#						self.cy
#						)
#			self.screenshot_timer += 1
#		else:
#			if self.screenshot_timer<100:
#				self.screenshot_timer += 1




	def release(self):
		glDeleteBuffers(1, [self.vertex_buffer])
		#glDeleteBuffers(1, [self.color_buffer])
		glDeleteBuffers(1, [self.normal_buffer])
		print("Cube's buffers deleted")
