import pygame

from OpenGL.GL import *

pygame.init()

screen = pygame.display.set_mode(
    (800,600),
    pygame.OPENGL | pygame.DOUBLEBUF
)

x = 10
y = 10

glClearColor(0.0,1.0,0.0,1.0)

running = True
while running:
    #clean
    glClear(GL_COLOR_BUFFER_BIT)

    #paint
    # screen.set_at((x,y),(255,255,255))
    # x += 1
    # y += 1

    #flip 
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running= False
