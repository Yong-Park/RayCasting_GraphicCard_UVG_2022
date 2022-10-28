import pygame
from numpy import *
from OpenGL.GL import *
import time

color_bg = (0.04,0.04,0.04)
color_grid = (0.16,0.16,0.16)
color_alive_next = (1,1,1)

def update(cells,size,moving=False):
    update_cells = zeros((cells.shape[0], cells.shape[1]))

    for row, col in ndindex(cells.shape):
        alive = sum(cells[row-1:row+2, col-1:col+2]) - cells[row,col]
        color = color_bg if cells[row,col] == 0 else color_alive_next

        if cells[row,col] == 1:
            if alive < 2 or alive > 3:
                if moving:
                    color = color_bg
            elif 2 <= alive <= 3:
                update_cells[row,col] = 1
                if moving:
                    color = color_alive_next
        else:
            if alive == 3:
                update_cells[row,col] = 1
                if moving:
                    color = color_alive_next
        pixel((col*size),(row*size),(size-1),(size-1),color)

    return update_cells

def pixel(x,y,w,h,color):
    glEnable(GL_SCISSOR_TEST)
    glScissor(x,y,w,h)
    glClearColor(color[0],color[1],color[2],1.0)
    glClear(GL_COLOR_BUFFER_BIT)
    glDisable(GL_SCISSOR_TEST)

#en rango de 10 en 10
points= [
    [50,100],[60,100],[70,100], #blinker
    [80,180],[90,180],[100,180],[90,190],[100,190],[110,190], #toad
    [180,150],[190,150],[200,150],[200,160],[190,170], #glider
    [200,50],[210,50],[220,60],[210,70],[200,70],[190,60], #bee-hive
    [100,300],[110,300],[100,310],[110,310],[120,320],[130,320],[120,330],[130,330], #beacon
    [500,350],[510,350],[520,350],[530,350],[490,360],[500,360],[510,360],[520,360],[530,360],[540,360],[490,370],[500,370],[510,370],[520,370],[540,370],[550,370],[530,380],[540,380], #heavy weight spaceship
    ]

def main():
    pygame.init()
    pygame.display.set_mode(
    (800,800),
    pygame.OPENGL | pygame.DOUBLEBUF,
    )
    #asignarle un color para el fondo
    glClearColor(color_grid[0],color_grid[1],color_grid[2],1.0)
    glClear(GL_COLOR_BUFFER_BIT)
    #obtener el tamaño del window creado
    screen_size = pygame.display.get_window_size()
    #crear celdas para asignar cada valor en su respectiva posicion
    cells = zeros((round(screen_size[0]/10),round(screen_size[1]/10)))
    #crear cuadros con valores de cero
    update(cells,10)
    #flip
    pygame.display.flip()
    #pintar los puntos en las celdas creadas
    for point in points:
        cells[point[1] // 10,point[0] // 10] = 1
        update(cells,10)
        pygame.display.flip()

    running = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            
            #comenzar a moverse
            running = True
            update(cells,10)
                
        glClearColor(color_grid[0],color_grid[1],color_grid[2],1.0)
        glClear(GL_COLOR_BUFFER_BIT)
        #efecto de movimiento
        if running:
            cells = update(cells, 10, moving=True)
            pygame.display.flip()
        #tiempo de espera para que no sea muy rapido
        time.sleep(0.1)

if __name__ == '__main__':
    main()