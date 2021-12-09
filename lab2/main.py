import sys
import random

from OpenGL.GL import *
from glfw.GLFW import *


def startup():
    glClearColor(0.5, 0.5, 0.5, 1.0)
    update_viewport(None, 400, 400)


def shutdown():
    pass


def render(time):
    glClear(GL_COLOR_BUFFER_BIT)
    carpet_recursion_initialization(0.0, 0.0, 90.0, 30.0, 5)
    carpet_iteration(-100.0, 0.0, 90.0, 30.0, 5)
    glFlush()

    # glClear(GL_COLOR_BUFFER_BIT)
    # rectangle_random(0, 0, 50, 25, 0.0)
    # glFlush()


def carpet_recursion_initialization(x, y, a, b, d):
    rectangle(x, y, a, b, 1.0)
    carpet_recursion(x, y, a, b, d)


def carpet_recursion(x, y, a, b, d):
    if d > 0:
        width = a / 3
        height = b / 3
        for i in range(3):
            carpet_recursion(x + width * i, y, width, height, d - 1)
            carpet_recursion(x + width * i, y + 2 * height, width, height, d - 1)
            if i != 1:
                carpet_recursion(x + width * i, y + height, width, height, d - 1)
    else:
        rectangle(x, y, a, b, 0.0)


def carpet_iteration(x, y, a, b, d):
    rectangle(x, y, a, b, 0.0)
    for i in range(d):
        width = a / (3 ** (i + 1))
        height = b / (3 ** (i + 1))
        for k in range(3 ** i):
            for j in range(3 ** i):
                rectangle(x + (width * (3 * j + 1)), y + (height * (3 * k + 1)), width, height, 1.0)


def rectangle(x, y, a, b, color):
    glColor3f(color, color, color)
    glBegin(GL_TRIANGLES)
    glVertex2f(x, y)
    glVertex2f(x, y + b)
    glVertex2f(x + a, y + b)
    glEnd()

    glBegin(GL_TRIANGLES)
    glColor3f(color, color, color)
    glVertex2f(x, y)
    glVertex2f(x + a, y)
    glVertex2f(x + a, y + b)
    glEnd()


def rectangle_random(x, y, a, b, d):
    rc1 = random.random()
    rc2 = random.random()
    rc3 = random.random()

    if d != 0:
        x = d * random.uniform(-d, d)
        y = d * random.uniform(-d, d)
        a = d * random.randrange(50)
        b = d * random.randrange(50)

    glBegin(GL_TRIANGLES)
    glColor3f(rc1, rc2, rc3)
    glVertex2f(x, y)
    glColor3f(rc3, rc1, rc2)
    glVertex2f(x, x + b)
    glColor3f(rc2, rc3, rc1)
    glVertex2f(x + a, x + b)
    glEnd()

    glBegin(GL_TRIANGLES)
    glColor3f(rc1, rc2, rc3)
    glVertex2f(x, y)
    glColor3f(rc2, rc3, rc1)
    glVertex2f(x + a, x + b)
    glColor3f(rc3, rc1, rc2)
    glVertex2f(x + a, y)
    glEnd()


def triangle3color():
    glBegin(GL_TRIANGLES)
    glColor3f(1.0, 0.0, 0.0)
    glVertex2f(-50.0, 0.0)
    glColor3f(0.0, 1.0, 0.0)
    glVertex2f(0.0, 50.0)
    glColor3f(0.0, 0.0, 1.0)
    glVertex2f(50.0, 0.0)
    glEnd()


def update_viewport(window, width, height):
    if width == 0:
        width = 1
    if height == 0:
        height = 1
    aspect_ratio = width / height

    glMatrixMode(GL_PROJECTION)
    glViewport(0, 0, width, height)
    glLoadIdentity()

    if width <= height:
        glOrtho(-100.0, 100.0, -100.0 / aspect_ratio, 100.0 / aspect_ratio,
                1.0, -1.0)
    else:
        glOrtho(-100.0 * aspect_ratio, 100.0 * aspect_ratio, -100.0, 100.0,
                1.0, -1.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSwapInterval(1)

    startup()
    while not glfwWindowShouldClose(window):
        render(glfwGetTime())
        glfwSwapBuffers(window)
        glfwWaitEvents()
    shutdown()

    glfwTerminate()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
