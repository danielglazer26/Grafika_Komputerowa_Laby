import sys
import math
import random

import numpy as numpy
from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)


def shutdown():
    pass


def spin_sphere(angle):
    #glRotate(angle, 0.0, 1.0, 0.0)
    glRotate(angle, 0.0, 0.0, 1.0)


def spin(angle):
    glRotate(angle, 1.0, 0.0, 0.0)
    glRotate(angle, 0.0, 1.0, 0.0)
    glRotate(angle, 0.0, 0.0, 1.0)


def axes():
    glBegin(GL_LINES)

    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(-5.0, 0.0, 0.0)
    glVertex3f(5.0, 0.0, 0.0)

    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, -5.0, 0.0)
    glVertex3f(0.0, 5.0, 0.0)

    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0.0, 0.0, -5.0)
    glVertex3f(0.0, 0.0, 5.0)

    glEnd()


def render(time, table):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    spin(time * 180 / 3.1415)
    render_by_triangle_strip(table)
    glLoadIdentity()
    axes()

    glFlush()


def render_sphere(time, table, time2, r2):
    v1 = math.degrees(math.pi)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    #spin(time * 180 / 3.1415)
    if r2[0] - (time - time2[0]) < 2:
        r2[0] = r2[0] + (time - time2[0])
    else:
        r2[0] = r2[0] - (time - time2[0])

    time2[0] = time
    v2 = math.degrees(v1 * math.sqrt(r2[0] / 2))

    spin_sphere(v2)
    render_by_triangle(create_table_sphere(0, 5, 0))
    glLoadIdentity()
    axes()

    glFlush()


def render_by_triangle_strip(table):
    glBegin(GL_TRIANGLE_STRIP)
    for i in range(table.shape[0] - 1):
        for j in range(table.shape[1]):
            glColor3f(table[i][j][3], table[i][j][4], table[i][j][5])
            glVertex3f(table[i][j][0], table[i][j][1], table[i][j][2])
            glColor3f(table[i + 1][j][3], table[i + 1][j][4], table[i + 1][j][5])
            glVertex3f(table[i + 1][j][0], table[i + 1][j][1], table[i + 1][j][2])
    glEnd()


def render_by_triangle(table):
    for i in range(table.shape[0] - 1):

        for j in range(table.shape[1] - 1):

            render_triangle(table[i][j], table[i][j + 1], table[i + 1][j])
            render_triangle(table[i][j + 1], table[i + 1][j + 1], table[i + 1][j])


def render_triangle(firstVertex, secondVertex, thirdVertex):
    glBegin(GL_TRIANGLES)
    glColor3d(firstVertex[3], firstVertex[4], firstVertex[5])
    glVertex3d(firstVertex[0], firstVertex[1], firstVertex[2])

    glColor3d(secondVertex[3], secondVertex[4], secondVertex[5])
    glVertex3d(secondVertex[0], secondVertex[1], secondVertex[2])

    glColor3d(thirdVertex[3], thirdVertex[4], thirdVertex[5])
    glVertex3d(thirdVertex[0], thirdVertex[1], thirdVertex[2])
    glEnd()


def render_by_lines(table):
    glBegin(GL_LINES)
    for i in range(table.shape[0]):
        for j in range(table.shape[1]):
            glVertex3f(table[i][j][0], table[i][j][1], table[i][j][2])
            if i + 1 == table.shape[0]:
                glVertex3f(table[0][j][0], table[0][j][1], table[0][j][2])
            else:
                glVertex3f(table[i + 1][j][0], table[i + 1][j][1], table[i + 1][j][2])

            if j + 1 == table.shape[1]:
                glVertex3f(table[i][0][0], table[i][0][1], table[i][0][2])
            else:
                glVertex3f(table[i][j + 1][0], table[i][j + 1][1], table[i][j + 1][2])
    glEnd()


def render_by_points(table):
    glBegin(GL_POINTS)
    for i in table:
        for j in i:
            glVertex3f(j[0], j[1], j[2])
    glEnd()


def create_table():
    N = 50
    table = numpy.zeros((N, N, 6))
    for i in range(N):
        for j in range(N):
            u = i / (N - 1)
            v = j / (N - 1)

            x = math.cos(math.pi * v) * (-90 * u ** 5 + 225 * u ** 4 - 270 * u ** 3 + 180 * u ** 2 - 45 * u)
            table[i][j][0] = x

            y = 160 * u ** 4 - 320 * u ** 3 + 160 * u ** 2
            table[i][j][1] = y

            z = math.sin(math.pi * v) * (-90 * u ** 5 + 225 * u ** 4 - 270 * u ** 3 + 180 * u ** 2 - 45 * u)
            table[i][j][2] = z

            for k in range(3, 6):
                table[i][j][k] = random.uniform(0.0, 1.0)
    return table


def create_table_sphere(x0, y0, z0):
    N = 50
    r = 2
    table = numpy.zeros((N + 1, N + 1, 6))
    for i in range(N + 1):
        for j in range(N + 1):
            u = (i * 2 * math.pi) / N
            v = (j * math.pi) / N

            x = x0 + r * math.cos(u) * math.sin(v)
            table[i][j][0] = x

            y = y0 + r * math.sin(u) * math.sin(v)
            table[i][j][1] = y

            z = z0 + r * math.cos(v)
            table[i][j][2] = z

            for k in range(3, 6):
                table[i][j][k] = random.uniform(0.0, 1.0)

    return table


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
        glOrtho(-7.5, 7.5, -7.5 / aspect_ratio, 7.5 / aspect_ratio, 7.5, -7.5)
    else:
        glOrtho(-7.5 * aspect_ratio, 7.5 * aspect_ratio, -7.5, 7.5, 7.5, -7.5)

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

    table = create_table()

    startup()
    r2 = numpy.zeros(1)
    r2[0] = 5
    time2 = numpy.zeros(1)
    while not glfwWindowShouldClose(window):
        #render(glfwGetTime(), table)
        render_sphere(glfwGetTime(), table, time2, r2)
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()
