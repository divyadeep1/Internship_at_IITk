import glm
from ctypes import c_void_p
# Global window
window = None
null = c_void_p(0)

#for camera
position = glm.vec3(0,0,10)
front = glm.vec3(0,0,-1)
up = glm.vec3(0,1,0)

#for mouse movements
lastX = 512
lastY = 256
pitch = 0
yaw = 3.14
firstmouse = True
