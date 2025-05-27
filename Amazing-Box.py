import random
import time
import numpy as np
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

window_width, window_height = 700, 600
points = []
speed = 0.01

is_frozen = False

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = [random.random(),random.random(),random.random()]
        self.direction = [random.choice([-1, 1])*speed,random.choice([-1, 1])*speed]
        self.blink = False
        self.blink_start_time = 0

    def movement(self):
        if not is_frozen:
            self.x += self.direction[0]
            self.y += self.direction[1]

            if self.x<=-1 or self.x>=1:
                self.direction[0] = -self.direction[0]
            if self.y<=-1 or self.y>=1:
                self.direction[1] = -self.direction[1]

    def draw(self):
        if self.blink and time.time()-self.blink_start_time>=1:
            self.blink = False
        glColor3f(0.0,0.0,0.0) if self.blink else glColor3f(*self.color)
        glBegin(GL_POINTS)
        glVertex2f(self.x, self.y)
        glEnd()

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    for point in points:
        point.movement()
        point.draw()
    glutSwapBuffers()

def timer(value):
    glutPostRedisplay()
    glutTimerFunc(16, timer, 0)

def keyboard(key, x, y):
    global speed, is_frozen
    if key == b'\x1b': #ESC dile off 
        glutLeaveMainLoop()
    elif key == b' ':
        is_frozen = not is_frozen

def special_keys(key, x, y):
    global speed
    if key == GLUT_KEY_UP:
        speed += 0.01
    elif key == GLUT_KEY_DOWN:
        speed = max(0.01, speed - 0.01)
    for point in points:
        point.direction[0] = speed if point.direction[0] > 0 else -speed
        point.direction[1] = speed if point.direction[1] > 0 else -speed


def mouse(button, state, x, y):
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        gl_x = (x/window_width)*2-1
        gl_y = 1-(y/window_height)*2
        points.append(Point(gl_x, gl_y))
    elif button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        for point in points:
            point.blink = True
            point.blink_start_time = time.time()

def init():
    glClearColor(0.0,0.0,0.0,1.0)
    glPointSize(5)

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(window_width, window_height)
    glutCreateWindow(b"Amazing Box")
    init()
    glutDisplayFunc(display)
    glutTimerFunc(16, timer, 0)
    glutKeyboardFunc(keyboard)
    glutSpecialFunc(special_keys)
    glutMouseFunc(mouse)
    glutMainLoop()

if __name__ == "__main__":
    main()