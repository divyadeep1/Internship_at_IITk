from OpenGL.GL import *
from OpenGL.GL.ARB import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.GLUT.special import *
from OpenGL.GL.shaders import *

import params
import math
import glm
import Shaders

null = c_void_p(0)

class Cube():
	def __init__(self, Shader):
		self.vertices = [-1.0, -1.0, -1.0,
						 -1.0, 1.0, -1.0,
						 1.0, 1.0, -1.0,
						 1.0, -1.0, -1.0,
						 -1.0, -1.0, -1.0,
						 1.0, -1.0, -1.0, 
						 1.0, -1.0, 1.0, 
						 -1.0, -1.0, 1.0, 
						 1.0, -1.0, -1.0, 
						 1.0, 1.0, -1.0, 
						 1.0, 1.0, 1.0, 
						 1.0, -1.0, 1.0, 
						 -1.0, -1.0, -1.0, 
						 -1.0, -1.0, 1.0, 
						 -1.0, 1.0, 1.0, 
						 -1.0, 1.0, -1.0, 
						 1.0, 1.0, -1.0, 
						 -1.0, 1.0, -1.0, 
						 -1.0, 1.0, 1.0, 
						 1.0, 1.0, 1.0, 
						 -1.0, -1.0, 1.0, 
						 1.0, -1.0, 1.0, 
						 1.0, 1.0, 1.0, 
						 -1.0, 1.0, 1.0,
						 50.0,-1.5,50.0,
						 50.0,-1.5,-50.0,
						 -50.0,-1.5,-50.0,
						 -50.0,-1.5,50.0]
						 
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
		 			   0.2, 0.57, 0.76,
		 			   0.3, 0.3, 0.3,
		 			   0.3, 0.3, 0.3,
		 			   0.3, 0.3, 0.3,
		 			   0.3, 0.3, 0.3]
		
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
						0.0,1.0,0.0,
						0.0,1.0,0.0,
						0.0,1.0,0.0,
						0.0,1.0,0.0]
		
		
		self.shader = Shader
		
		self.vertex_buffer = glGenBuffers(1)
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
		
		
		######DIFFERENT CODE FROM cube_test_1.py file BEGINS######
		
		###Shadow texture + framebufferobject
		self.shadow_shader = Shaders.Shader('./shaders/Test2/StandardShadowShading.vertexshader', 
											'./shaders/Test2/StandardShadowShading.fragmentshader')
		self.depthMapFBO = glGenFramebuffers(1)
		self.SHADOW_WIDTH = 1024
		self.SHADOW_HEIGHT = 1024
		
		self.depthMap = glGenTextures(1)
		glBindTexture(GL_TEXTURE_2D, self.depthMap)
		glTexImage2D(GL_TEXTURE_2D, 0, GL_DEPTH_COMPONENT, self.SHADOW_WIDTH, self.SHADOW_HEIGHT, 0, GL_DEPTH_COMPONENT, GL_FLOAT, null)
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_BORDER)
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_BORDER)
		borderColor = [ 1.0, 1.0, 1.0, 1.0 ]
		glTexParameterfv(GL_TEXTURE_2D, GL_TEXTURE_BORDER_COLOR, borderColor);  

		#attach depth texture as FBO's depth buffer
		glBindFramebuffer(GL_FRAMEBUFFER, self.depthMapFBO)
		glFramebufferTexture2D(GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT, GL_TEXTURE_2D, self.depthMap, 0)
		glDrawBuffer(GL_NONE)
		glReadBuffer(GL_NONE)
		glBindFramebuffer(GL_FRAMEBUFFER, 0)
		
		###Quad Shader for rendering the shadow map made by the texture. Uses a 3rd shader.
		self.quadVertices = [
					-1.0,  1.0, 0.0, 0.0, 1.0,
            		-1.0, -1.0, 0.0, 0.0, 0.0,
             		1.0,  1.0, 0.0, 1.0, 1.0,
             		1.0, -1.0, 0.0, 1.0, 0.0]
		self.quadVBO = 0
		self.quadVAO = 0
		self.quad = Shaders.Shader('./shaders/Test2/QuadVertexShader.vertexshader','./shaders/Test2/QuadFragmentShader.fragmentshader')
		
	def rotate(self,angle,axis):
		self.model = glm.rotate(self.model, angle, axis)
		
	def translate(self,position):	
		self.model = glm.translate(self.model, position)
	
	def mvp(self):
		return (params.projection() * params.view() * params.model())
		
	def render(self):
		light_color = glm.vec3(1.0, 1.0, 1.0)
		params.t = (params.t+1)%1000000000
		light_position = glm.vec3(0.0,5.0,1.0)#glm.vec3(0.0, 5*math.sin(0.0002*params.t), 5*math.cos(0.0002*params.t))#glm.vec3(6.0,6.0,0.0)
		
		
		######RENDERING DEPTH OF SCENE FROM LIGHT'S PERSPECTIVE######
		glClearColor(0.1, 0.1, 0.1, 1.0)
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

		near_plane = 1.0
		far_plane = 7.5
		lightProjection = glm.ortho(-10.0, 10.0, -10.0, 10.0, near_plane, far_plane)
		lightView = glm.lookAt(light_position, glm.vec3(0.0), glm.vec3(0.0, 1.0, 0.0))
		
		###Trying out bias matrix
		#bias = glm.mat4(
		#	0.5, 0.0, 0.0, 0.0, 
		#	0.0, 0.5, 0.0, 0.0,
		#	0.0, 0.0, 0.5, 0.0,
		#	0.5, 0.5, 0.5, 1.0
		#)

		lightSpaceMatrix = lightProjection * lightView
		#lightSpaceMatrix = bias * lightSpaceMatrix
		###render scene from light's point of view###
		glUseProgram(self.shadow_shader.ID)
		glUniformMatrix4fv(glGetUniformLocation(self.shadow_shader.ID, "lightSpaceMatrix"), 1, GL_FALSE, glm.value_ptr(lightSpaceMatrix))

		glViewport(0, 0, self.SHADOW_WIDTH, self.SHADOW_HEIGHT)
		#glEnable(GL_CULL_FACE)
		#glCullFace(GL_BACK)
		glBindFramebuffer(GL_FRAMEBUFFER, self.depthMapFBO)
		glClear(GL_DEPTH_BUFFER_BIT)
		#glActiveTexture(GL_TEXTURE0)
		#glBindTexture(GL_TEXTURE_2D, self.depthMap)
		glEnableVertexAttribArray(0)
		glBindBuffer(GL_ARRAY_BUFFER, self.vertex_buffer);
		glVertexAttribPointer(0, 3,	GL_FLOAT, GL_FALSE,	0, null)
		glDrawArrays(GL_QUADS, 0, 6*5)
		glDisableVertexAttribArray(0)
		glBindFramebuffer(GL_FRAMEBUFFER, 0)
		
		###reset viewport###
		glViewport(0, 0, 1024, 768)
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
		
		######RENDERING SCENE AS NORMAL USING SHADOWS CREATED######
		
		#TODO: Move all the uniforms outside the rendering function and into the __init__() function.
		glUseProgram(self.shader.ID)
		glUniformMatrix4fv(glGetUniformLocation(self.shader.ID, "model"), 1, GL_FALSE, glm.value_ptr(params.model()))
		glUniformMatrix4fv(glGetUniformLocation(self.shader.ID, "MVP"), 1, GL_FALSE, glm.value_ptr(self.mvp()))
		glUniform3f(glGetUniformLocation(self.shader.ID, "lightColor"), light_color.x, light_color.y, light_color.z)
		glUniform3f(glGetUniformLocation(self.shader.ID, "lightPosition"), light_position.x, light_position.y, light_position.z)
		glUniform3f(glGetUniformLocation(self.shader.ID, "viewPos"), params.position.x, params.position.y, params.position.z)
		glUniformMatrix4fv(glGetUniformLocation(self.shader.ID, "lightSpaceMatrix"), 1, GL_FALSE, glm.value_ptr(lightSpaceMatrix))
		
		glActiveTexture(GL_TEXTURE0)
		glBindTexture(GL_TEXTURE_2D, self.depthMap)
		glUniform1i(glGetUniformLocation(self.shader.ID, "shadowMap"), 0)
		
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
		glDrawArrays(GL_QUADS, 0, 6*5)
		glEnable(GL_DEPTH_TEST)
		glDisableVertexAttribArray(0)
		glDisableVertexAttribArray(1)
		glDisableVertexAttribArray(2)
		
		
		#####RENDERING THE SHADOWMAP#####
		glViewport(0,0,512,512)
		glUseProgram(self.quad.ID)
		glActiveTexture(GL_TEXTURE0)
		glBindTexture(GL_TEXTURE_2D, self.depthMap)
		glUniform1i(glGetUniformLocation(self.quad.ID, "depthMap"), 0)
		self.quadVBO = glGenBuffers(1)
		self.quadVAO = glGenVertexArrays(1)
		glBindVertexArray(self.quadVAO)
		glBindBuffer(GL_ARRAY_BUFFER, self.quadVBO)
		array_type = GLfloat * len(self.quadVertices)
		glBufferData(GL_ARRAY_BUFFER, len(self.quadVertices), array_type(*self.quadVertices), GL_STATIC_DRAW)
		
		glEnableVertexAttribArray(0);
		glBindBuffer(GL_ARRAY_BUFFER, self.quadVBO);
		glVertexAttribPointer(0,3,GL_FLOAT,	GL_FALSE,5*4,null)     
		glEnableVertexAttribArray(1)
		glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 5 * 4, c_void_p(3 * 4))
		
		glBindVertexArray(self.quadVAO)
		glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)
		glBindVertexArray(0)
		#glDisableVertexAttribArray(0)
		#glDisableVertexAttribArray(1)
		
		
	def release(self):
		glDeleteBuffers(1, [self.vertex_buffer])
		glDeleteBuffers(1, [self.color_buffer])
		glDeleteBuffers(1, [self.normal_buffer])
		print("Cube's buffers deleted")

