"""Camera module for creating cameras and handling movement in 3d space
"""
import glm


def make_camera(position, target, head):
	cam = glm.lookAt(position, target, head)
	return cam

def handle_target()
	# ???
