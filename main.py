import pygame
from OpenGL.GL import *

pygame.init()

screen = pygame.display.set_mode(
    (800,600),
    pygame.OPENGL | pygame.DOUBLEBUF
)

x = 10
y = 10
x1 = 600
y1 = 500

def pixel(x,y,color):
    glEnable(GL_SCISSOR_TEST)
    glScissor(x,y,100,100)
    glClearColor(color[0],color[1],color[2],1.0)
    glClear(GL_COLOR_BUFFER_BIT)
    glDisable(GL_SCISSOR_TEST)

speedx = 1
speedy = 1
speedx1 = 1
speedy1 = 1
running = True
while running:
    #clean
    glClearColor(0.1,0.1,0.1,1.0)
    glClear(GL_COLOR_BUFFER_BIT)

    #paint
    pixel(x,y,(1.0,0.0,0.0))
    x += speedx
    y += speedy

    if x == 800:
        speedx = -1
    if x == 0:
        speedx = 1
    if y == 600:
        speedy = -1
    if y == 0:
        speedy = 1

    pixel(x1,y1,(1.0,1.0,0.0))
    x1 += speedx1
    y1 += speedy1

    if x1 == 800:
        speedx1 = -1
    if x1 == 0:
        speedx1 = 1
    if y1 == 600:
        speedy1 = -1
    if y1 == 0:
        speedy1 = 1

    if x == x1:
        if x > 400:
            speedx = -1
            speedx1 = 1
        else:
            speedx = 1
            speedx1 = -1

    if y == y1:
        if y > 300:
            speedy = -1
            speedy1 = 1
        else:
            speedy = 1
            speedy1 = -1

    #flip 
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running= False