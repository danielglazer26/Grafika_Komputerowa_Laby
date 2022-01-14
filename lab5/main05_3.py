import math
import sys

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

viewer = [0.0, 0.0, 10.0]

pix2angle = 1.0

R = 10

delta_x = 0
delta_y = 0

thetaX = 0.0
thetaY = 0.0

left_mouse_button_pressed = 0
right_mouse_button_pressed = 0

thetaX_2 = 0.0
thetaY_2 = 0.0

mouse_x_pos_old = 0
mouse_y_pos_old = 0

mat_ambient = [1.0, 1.0, 1.0, 1.0]
mat_diffuse = [1.0, 1.0, 1.0, 1.0]
mat_specular = [1.0, 1.0, 1.0, 1.0]
mat_shininess = 20.0

light_ambient = [0.0, 1.0, 0.0, 1.0]
light_diffuse = [0.5, 0.5, 0.0, 1.0]
light_specular = [1.0, 1.0, 1.0, 1.0]
light_position = [-20.0, 0.0, 0.0, 1.0]

light_ambient_2 = [0.5, 0.5, 0.5, 1.0]
light_diffuse_2 = [0.5, 0.5, 0.0, 1.0]
light_specular_2 = [1.0, 1.0, 1.0, 1.0]
light_position_2 = [20.0, 0.0, 0.0, 1.0]

att_constant = 1.0
att_linear = 0.05
att_quadratic = 0.001


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)

    glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
    glMaterialf(GL_FRONT, GL_SHININESS, mat_shininess)

    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)

    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, att_constant)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, att_linear)
    glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, att_quadratic)

    glLightfv(GL_LIGHT1, GL_AMBIENT, light_ambient_2)
    glLightfv(GL_LIGHT1, GL_DIFFUSE, light_diffuse_2)
    glLightfv(GL_LIGHT1, GL_SPECULAR, light_specular_2)
    glLightfv(GL_LIGHT1, GL_POSITION, light_position_2)

    glLightf(GL_LIGHT1, GL_CONSTANT_ATTENUATION, att_constant)
    glLightf(GL_LIGHT1, GL_LINEAR_ATTENUATION, att_linear)
    glLightf(GL_LIGHT1, GL_QUADRATIC_ATTENUATION, att_quadratic)

    glEnable(GL_LIGHT1)

    glShadeModel(GL_SMOOTH)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)


def shutdown():
    pass


def spin(angle):
    glRotatef(angle, 0.1, 0.0, 0.0)
    glRotatef(angle, 0.0, 0.1, 0.0)
    glRotatef(angle, 0.0, 0.0, 0.1)


def camera_coordinates():
    Xeye = R * math.cos(thetaX * math.pi / 180) * math.cos(thetaY * math.pi / 180)
    Yeye = R * math.sin(thetaY * math.pi / 180)
    Zeye = R * math.sin(thetaX * math.pi / 180) * math.cos(thetaY * math.pi / 180)
    return Xeye, Yeye, Zeye


def camera_coordinates_2():
    Xeye = R * math.cos(thetaX_2 * math.pi / 180) * math.cos(thetaY_2 * math.pi / 180) * (-1)
    Yeye = R * math.sin(thetaY_2 * math.pi / 180) * (-1)
    Zeye = R * math.sin(thetaX_2 * math.pi / 180) * math.cos(thetaY_2 * math.pi / 180) * (-1)
    return Xeye, Yeye, Zeye


def render(time):
    global thetaX, thetaY, delta_x, delta_y, light_position, light_position_2
    global thetaX_2, thetaY_2

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    gluLookAt(viewer[0], viewer[1], viewer[2],
              0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    if left_mouse_button_pressed:
        thetaX += delta_x * pix2angle
        thetaY += delta_y * pix2angle
    if right_mouse_button_pressed:
        thetaX_2 += delta_x * pix2angle
        thetaY_2 += delta_y * pix2angle

    light_position = camera_coordinates()
    light_position_2 = camera_coordinates_2()

    glTranslatef(light_position[0], light_position[1], light_position[2])

    quadric_first_light = gluNewQuadric()
    gluQuadricDrawStyle(quadric_first_light, GLU_LINE)
    gluSphere(quadric_first_light, 0.5, 6, 15)
    gluDeleteQuadric(quadric_first_light)

    glTranslatef(-light_position[0], -light_position[1], -light_position[2])

    glTranslatef(light_position_2[0], light_position_2[1], light_position_2[2])

    quadric_second_light = gluNewQuadric()
    gluQuadricDrawStyle(quadric_second_light, GLU_LINE)
    gluSphere(quadric_second_light, 0.5, 6, 5)
    gluDeleteQuadric(quadric_second_light)

    glTranslatef(-light_position_2[0], -light_position_2[1], -light_position_2[2])

    glLightfv(GL_LIGHT0, GL_POSITION, light_position)
    glLightfv(GL_LIGHT1, GL_POSITION, light_position_2)

    spin(time * 180 / math.pi)

    quadric = gluNewQuadric()
    gluQuadricDrawStyle(quadric, GLU_FILL)
    gluSphere(quadric, 3.0, 10, 10)
    gluDeleteQuadric(quadric)

    quadric2 = gluNewQuadric()
    gluQuadricDrawStyle(quadric2, GLU_LINE)
    gluSphere(quadric2, 5.5, 10, 10)
    gluDeleteQuadric(quadric2)

    glFlush()


def update_viewport(window, width, height):
    global pix2angle
    pix2angle = 360.0 / width

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluPerspective(100, 1.0, 0.1, 500.0)

    if width <= height:
        glViewport(0, int((height - width) / 2), width, width)
    else:
        glViewport(int((width - height) / 2), 0, height, height)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def keyboard_key_callback(window, key, scancode, action, mods):
    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)


def mouse_motion_callback(window, x_pos, y_pos):
    global delta_x, delta_y
    global mouse_x_pos_old, mouse_y_pos_old

    delta_x = x_pos - mouse_x_pos_old
    mouse_x_pos_old = x_pos

    delta_y = y_pos - mouse_y_pos_old
    mouse_y_pos_old = y_pos


def mouse_button_callback(window, button, action, mods):
    global left_mouse_button_pressed, right_mouse_button_pressed

    if button == GLFW_MOUSE_BUTTON_LEFT and action == GLFW_PRESS:
        left_mouse_button_pressed = 1
    else:
        left_mouse_button_pressed = 0

    if button == GLFW_MOUSE_BUTTON_RIGHT and action == GLFW_PRESS:
        right_mouse_button_pressed = 1
    else:
        right_mouse_button_pressed = 0


def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSetKeyCallback(window, keyboard_key_callback)
    glfwSetCursorPosCallback(window, mouse_motion_callback)
    glfwSetMouseButtonCallback(window, mouse_button_callback)
    glfwSwapInterval(1)

    startup()
    while not glfwWindowShouldClose(window):
        render(glfwGetTime())
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()
