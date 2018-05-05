"""Shaders"""

from OpenGL.GL.shaders import *
from OpenGL.GL import *

class Shader:
	def __init__(self, vertex_file_path, fragment_file_path):
		self.VertexShaderID = glCreateShader(GL_VERTEX_SHADER)
		self.FragmentShaderID = glCreateShader(GL_FRAGMENT_SHADER)

		# Read the Vertex Shader code from the file
		self.VertexShaderCode = ""
		with open(vertex_file_path,'r') as fr:
			for line in fr:
				self.VertexShaderCode += line
			# alternatively you could use fr.readlines() and then join in to a single string 

		self.FragmentShaderCode = ""
		with open(fragment_file_path,'r') as fr:
			for line in fr:
				self.FragmentShaderCode += line
			# alternatively you could use fr.readlines() and then join in to a single string 

		# Compile Vertex Shader
		print("Compiling shader: %s"%(vertex_file_path))
		glShaderSource(self.VertexShaderID, self.VertexShaderCode)
		glCompileShader(self.VertexShaderID)

		# Check Vertex Shader
		result = glGetShaderiv(self.VertexShaderID, GL_COMPILE_STATUS)
		if not result:
			raise RuntimeError(glGetShaderInfoLog(self.VertexShaderID))

		# Compile Fragment Shader
		print("Compiling shader: %s"%(fragment_file_path))
		glShaderSource(self.FragmentShaderID,self.FragmentShaderCode)
		glCompileShader(self.FragmentShaderID)

		# Check Fragment Shader
		result = glGetShaderiv(self.VertexShaderID, GL_COMPILE_STATUS)
		if not result:
			raise RuntimeError(glGetShaderInfoLog(self.FragmentShaderID))



		# Link the program
		print("Linking program")
		self.ID = glCreateProgram()
		glAttachShader(self.ID, self.VertexShaderID)
		glAttachShader(self.ID, self.FragmentShaderID)
		glLinkProgram(self.ID)

		# Check the program
		result = glGetShaderiv(self.VertexShaderID, GL_COMPILE_STATUS)
		if not result:
			raise RuntimeError(glGetShaderInfoLog(self.ID))

		glDeleteShader(self.VertexShaderID);
		glDeleteShader(self.FragmentShaderID);

	def release(self):
		glDeleteProgram(self.ID)
		print("Shader Deleted.")
