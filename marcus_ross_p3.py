# Author: Marcus Ross

from time import sleep
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from PIL import Image
import numpy

# arbitrary starting angles
orbitAngle1 = 270.0
orbitAngle2 = 0.0
orbitAngle3 = 90.0
framerate = 60.0 # for capping redraws at 60 per second

def texFromPNG(filename): # not used in current state
	img = Image.open(filename)
	img_data = numpy.array(list(img.getdata()), numpy.uint8)
	texture = glGenTextures(1)
	# glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
	glBindTexture(GL_TEXTURE_2D, texture)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
	glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
	glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img.size[0], img.size[1], 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
	return texture

def initGL():
	glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB | GLUT_DEPTH)
	glutInitWindowSize(700, 700)
	glutInitWindowPosition(300, 0)
	glutCreateWindow("ICSI422 Program 3 by Marcus Ross")

	glClearColor(0.0, 0.0, 0.0, 1.0)
	glShadeModel(GL_SMOOTH)
	glEnable(GL_CULL_FACE)
	glEnable(GL_DEPTH_TEST)
	glEnable(GL_LIGHTING)

	lightPos = [0.0, 0.0, -6.0, 1.0] # light positioned at center of sun, six units in front of camera
	lightAmbient = [0.1, 0.1, 0.1, 1.0] # slight lighting of dark side of planets due to ambient outerspace radiation
	lightDiffuse = [0.75, 0.75, 0.75, 1.0]
	lightSpecular = [0.5, 0.5, 0.5, 1.0]

	glLightfv(GL_LIGHT0, GL_POSITION, lightPos)
	glLightfv(GL_LIGHT0, GL_AMBIENT, lightAmbient)
	glLightfv(GL_LIGHT0, GL_DIFFUSE, lightDiffuse)
	glLightfv(GL_LIGHT0, GL_SPECULAR, lightSpecular)
	glEnable(GL_LIGHT0)

	planetDiffuse = [0.75, 0.75, 0.75, 1.0]
	planetSpecular = [1.0, 1.0, 1.0, 1.0]
	planetShine = 8.0

	glMaterialfv(GL_FRONT, GL_DIFFUSE, planetDiffuse) # because these calls are outside the idle function, the same material is applied to all 3 "planets"
	glMaterialfv(GL_FRONT, GL_SPECULAR, planetSpecular)
	glMaterialfv(GL_FRONT, GL_SHININESS, planetShine)

	# global texture
	# texture = texFromPNG("name.png")

def reshape(x, y):
	glViewport(0, 0, x, y)
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	gluPerspective(90.0, 1.0, 0.1, 20.0)
	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()
	gluLookAt(0.0, 4.0, 6.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
	
def idle():
	global orbitAngle1
	global orbitAngle2
	global orbitAngle3
	global framerate

	sleep(1 / framerate) # redraw at most 60 times per second
	orbitAngle1 += 0.6 # median orbit speed
	orbitAngle2 += 2.75 # fastest orbit
	orbitAngle3 += 0.15 # slowest orbit
	if orbitAngle1 > 360:
		orbitAngle1 -= 360
	if orbitAngle2 > 360:
		orbitAngle2 -= 360
	if orbitAngle3 > 360:
		orbitAngle3 -= 360
	glutPostRedisplay()

def display():
	global orbitAngle1
	global orbitAngle2
	global orbitAngle3
	global framerate
	global texture

	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

	glPushMatrix() # push sun
	glDisable(GL_LIGHTING)
	glutSolidSphere(1.5, 64, 64) # sun is 1.5 units wide
	glEnable(GL_LIGHTING)

	glPushMatrix() # push earth
	glRotatef(orbitAngle1, 0.0, 1.0, 0.0) # earth's orbit is a flat circle
	glTranslatef(3, 0.0, 0.0) # earth is 3 units away from the sun

########### texturing code begin; not working
	# glPushMatrix()
	# Q = gluNewQuadric()
	# gluQuadricTexture(Q, GL_TRUE)
	# glEnable(GL_TEXTURE_2D)
	# glBindTexture(GL_TEXTURE_2D,2)
	# glTexGeni(GL_S, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP)
	# glTexGeni(GL_T, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP)
	# glColor3f (1.0, 1.0, 1.0)
	# glPopMatrix()
########### texturing code end; not working

	glutSolidSphere(0.5, 64, 64) # earth is 0.5 units wide
	#glDisable(GL_TEXTURE_2D)

	glPushMatrix() # push moon
	glRotatef(orbitAngle2, 0.0, 1.0, 0.0) # moon orbits earth in the direction as direction earth orbits sun
	glTranslatef(1, 0.0, 0.0) # 1 unit away from earth
	glutSolidSphere(0.25, 64, 64) # 0.25 units wide
	glPopMatrix() # pop moon
	glPopMatrix() # pop earth

	glPushMatrix() # push mars
	glRotatef(orbitAngle3, -1, 4, 0.0) # mars rotates--unrealistically--at a different angle than earth, to look interesting
	glTranslatef(5, 1, 0.0) # 5 units away from sun
	glutSolidSphere(0.7, 64, 64) # mars is 0.7 units wide

	glPopMatrix() # pop mars
	glPopMatrix() # pop sun
	glutSwapBuffers()

def keyboard(key, x, y):
	if key == chr(27): # press escape to end program
		 sys.exit(0)

def main():
	glutInit(sys.argv)
	initGL()

	glutDisplayFunc(display)
	glutReshapeFunc(reshape)
	glutIdleFunc(idle)
	glutKeyboardFunc(keyboard)
	glutMainLoop()

if __name__ == "__main__":
	main()