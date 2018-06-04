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
                         50.0, -1., 50.0,
                         50.0, -1., -50.0,
                         -50.0, -1., -50.0,
                         -50.0, -1., 50.0]
                         
        self.colors = [0.33459217,  0.52109137,  0.19287258,  0.90671413,  0.41533494,
                       0.31015218,  0.30972265,  0.13518232,  0.0407303,  0.0729219,
                       0.04188457,  0.40966579,  0.8028398,  0.92307538,  0.4064563,
                       0.18387149,  0.95361129,  0.03470272,  0.10161366,  0.38676869,
                       0.15068039,  0.46669433,  0.79634865,  0.71430582,  0.86256922,
                       0.93558262,  0.67102294,  0.69232786,  0.24447952,  0.00685775,
                       0.46393682,  0.38077464,  0.52903373,  0.42553311,  0.09687797,
                       0.08238901,  0.68573079,  0.35895002,  0.16919371,  0.30924682,
                       0.4181197,  0.26068711,  0.92050772,  0.88765391,  0.82302449,
                       0.82970281,  0.31480517,  0.32702964,  0.72497687,  0.90491857,
                       0.74653115,  0.54174117,  0.56376659,  0.28842234,  0.65365089,
                       0.72726322,  0.14596222,  0.31691812,  0.89520995,  0.05670388,
                       0.55670408,  0.72836696,  0.83389241,  0.49575873,  0.57479909,
                       0.22893076,  0.06169841,  0.73281573,  0.34156023,  0.24480244,
                       0.00138273,  0.23266155,  0.4736198,  0.86236781,  0.95066312, 
                       0.4736198,  0.86236781,  0.95066312, 0.4736198,  0.86236781, 0.95066312]
                       
        self.normals = [0.0, 0.0, -1.0,
                        0.0, 0.0, -1.0,
                        0.0, 0.0, -1.0,
                        0.0, 0.0, -1.0,
                        0.0, -1.0, 0.0,
                        0.0, -1.0, 0.0,
                        0.0, -1.0, 0.0,
                        0.0, -1.0, 0.0,
                        1.0, 0.0, 0.0,
                        1.0, 0.0, 0.0,
                        1.0, 0.0, 0.0,
                        1.0, 0.0, 0.0,
                        -1.0, 0.0, 0.0,
                        -1.0, 0.0, 0.0,
                        -1.0, 0.0, 0.0,
                        -1.0, 0.0, 0.0,
                        0.0, 1.0, 0.0,
                        0.0, 1.0, 0.0,
                        0.0, 1.0, 0.0,
                        0.0, 1.0, 0.0,
                        0.0, 0.0, 1.0,
                        0.0, 0.0, 1.0,
                        0.0, 0.0, 1.0,
                        0.0, 0.0, 1.0,
                        0.0, 1.0, 0.0,
                        0.0, 1.0, 0.0,
                        0.0, 1.0, 0.0,
                        0.0, 1.0, 0.0]

        self.shader = Shader

        self.vertex_buffer = glGenBuffers(1)
        array_type = GLfloat * len(self.vertices)
        glBindBuffer(GL_ARRAY_BUFFER, self.vertex_buffer)
        glBufferData(GL_ARRAY_BUFFER, len(self.vertices) * 4,
                     array_type(*self.vertices), GL_STATIC_DRAW)

        self.color_buffer = glGenBuffers(1)
        array_type = GLfloat * len(self.colors)
        glBindBuffer(GL_ARRAY_BUFFER, self.color_buffer)
        glBufferData(GL_ARRAY_BUFFER, len(self.colors) * 4,
                     array_type(*self.colors), GL_STATIC_DRAW)

        self.normal_buffer = glGenBuffers(1)
        array_type = GLfloat * len(self.normals)
        glBindBuffer(GL_ARRAY_BUFFER, self.normal_buffer)
        glBufferData(GL_ARRAY_BUFFER, len(self.normals) * 4,
                     array_type(*self.normals), GL_STATIC_DRAW)

        ######DIFFERENT CODE FROM cube_test_1.py file BEGINS######

        # Shadow texture + framebufferobject
        self.shadow_shader = Shaders.Shader('./shaders/Shadow/StandardShadowShading.vertexshader',
                                            './shaders/Shadow/StandardShadowShading.fragmentshader')
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

        # Quad Shader for rendering the shadow map made by the texture. Uses a 3rd shader.
        """
        self.quadVertices = [
            -1.0,  1.0, 0.0, 0.0, 1.0,
            -1.0, -1.0, 0.0, 0.0, 0.0,
            1.0,  1.0, 0.0, 1.0, 1.0,
            1.0, -1.0, 0.0, 1.0, 0.0]
        self.quadVBO = 0
        self.quadVAO = 0
        self.quad = Shaders.Shader('./shaders/Shadow/QuadVertexShader.vertexshader',
                                   './shaders/Shadow/QuadFragmentShader.fragmentshader')
        """
    def rotate(self, angle, axis):
        self.model = glm.rotate(self.model, angle, axis)

    def translate(self, position):
        self.model = glm.translate(self.model, position)

    def mvp(self):
        return (params.projection() * params.view() * params.model())


    # This function needs to be called when shadows are required to be rendered.
    def render_with_shadows(self):
        params.t = (params.t+1) % 1000000000
        params.light_position = glm.vec3(
            5*math.sin(0.0007*params.t), 1.0, 5*math.cos(0.0007*params.t))  # glm.vec3(6.0,6.0,0.0)

        ######RENDERING DEPTH OF SCENE FROM LIGHT'S PERSPECTIVE######
        glClearColor(0.1, 0.1, 0.1, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # The lightProjection matrix is actually static but is kept in the render loop for the sake of convinience and easy access
        lightProjection = glm.ortho(-10.0, 10.0, -10.0,
                                    10.0, params.near_plane, params.far_plane)
        lightView = glm.lookAt(params.light_position,
                               glm.vec3(0.0), glm.vec3(0.0, 1.0, 0.0))
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
        glDrawArrays(GL_QUADS, 0, 28)
        glDisableVertexAttribArray(0)
        glBindFramebuffer(GL_FRAMEBUFFER, 0)
        glCullFace(GL_BACK)

        ###reset viewport###
        glViewport(0, 0, 1024, 768)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        ######RENDERING SCENE AS NORMAL USING SHADOWS CREATED######

        # TODO: Move all the uniforms outside the rendering function and into the __init__() function.
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

        glEnableVertexAttribArray(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.color_buffer)
        glVertexAttribPointer(1, 3,	GL_FLOAT, GL_FALSE,	0, null)

        glEnableVertexAttribArray(2)
        glBindBuffer(GL_ARRAY_BUFFER, self.normal_buffer)
        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, 0, null)

        # Draw the cube !
        glDrawArrays(GL_QUADS, 0, 28)
        glEnable(GL_DEPTH_TEST)
        glDisableVertexAttribArray(0)
        glDisableVertexAttribArray(1)
        glDisableVertexAttribArray(2)

        # TODO: Render the shadow map.
        """
		#####RENDERING THE SHADOWMAP#####
		#glViewport(0,0,1024,768)
		#glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
		glUseProgram(self.quad.ID)
		glActiveTexture(GL_TEXTURE0)
		glBindTexture(GL_TEXTURE_2D, self.depthMap)
		glUniform1i(glGetUniformLocation(self.quad.ID, "depthMap"), 0)
		if self.quadVAO == 0:
			#glBindFramebuffer(GL_FRAMEBUFFER, 0)
			self.quadVBO = glGenBuffers(1)
			self.quadVAO = glGenVertexArrays(1)
			glBindVertexArray(self.quadVAO)
			glBindBuffer(GL_ARRAY_BUFFER, self.quadVBO)
			array_type = GLfloat * len(self.quadVertices)
			glBufferData(GL_ARRAY_BUFFER, len(self.quadVertices), array_type(*self.quadVertices), GL_STATIC_DRAW)
			
			print(self.quadVAO, self.quadVBO)
			
			glEnableVertexAttribArray(0)
			glBindBuffer(GL_ARRAY_BUFFER, self.quadVBO)
			glVertexAttribPointer(0,3,GL_FLOAT,	GL_FALSE,5*4,null)
			glEnableVertexAttribArray(1)
			glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 5 * 4, c_void_p(3 * 4))
		
		glBindVertexArray(self.quadVAO)
		glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)
		glBindVertexArray(0)
		#glDisableVertexAttribArray(0)
		#glDisableVertexAttribArray(1)
		"""

    # This function needs to be called when shadows aren't required.
    def render(self):
        glUseProgram(self.shader.ID)
        glUniformMatrix4fv(glGetUniformLocation(
            self.shader.ID, "model"), 1, GL_FALSE, glm.value_ptr(params.model()))
        glUniformMatrix4fv(glGetUniformLocation(
            self.shader.ID, "MVP"), 1, GL_FALSE, glm.value_ptr(self.mvp()))
        glUniform3f(glGetUniformLocation(self.shader.ID, "lightColor"),
                    params.light_color.x, params.light_color.y, params.light_color.z)
        params.t = (params.t+1) % 1000000000
        params.light_position = glm.vec3(
            5*math.sin(0.002*params.t), 0.5, 5*math.cos(0.002*params.t))
        glUniform3f(glGetUniformLocation(self.shader.ID, "lightPosition"),
                    params.light_position.x, params.light_position.y, params.light_position.z)
        glUniform3f(glGetUniformLocation(self.shader.ID, "viewPos"),
                    params.position.x, params.position.y, params.position.z)

        glEnableVertexAttribArray(0)
        glBindBuffer(GL_ARRAY_BUFFER, self.vertex_buffer)
        glVertexAttribPointer(0, 3,	GL_FLOAT, GL_FALSE,	0, null)

        glEnableVertexAttribArray(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.color_buffer)
        glVertexAttribPointer(1, 3,	GL_FLOAT, GL_FALSE,	0, null)

        glEnableVertexAttribArray(2)
        glBindBuffer(GL_ARRAY_BUFFER, self.normal_buffer)
        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, 0, null)

        # Draw the cube !
        glDrawArrays(GL_QUADS, 0, 6*5)
        glEnable(GL_DEPTH_TEST)
        glDisableVertexAttribArray(0)
        glDisableVertexAttribArray(1)
        glDisableVertexAttribArray(2)

    def release(self):
        glDeleteBuffers(1, [self.vertex_buffer])
        glDeleteBuffers(1, [self.color_buffer])
        glDeleteBuffers(1, [self.normal_buffer])
        glDeleteFramebuffers(1, [self.depthMapFBO])
        print("Cube's buffers deleted")

