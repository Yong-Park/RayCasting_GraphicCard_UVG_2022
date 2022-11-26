"""
Universidad del Valle de Guatemala
Curso de Graficas por computadora
Lic. Dennis Aldana 
Raycaster
YongBum Park
Carnet 20117
"""

import pygame
from math import *

#Fps to show ingame
CLOCK = pygame.time.Clock()

BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (0,150,0)

SKY = (40,100,200)
GROUND = (200,200,100)

TRANSPARENT = (152,0,136,255)

colors = [
    (0,20,10),
    (4,40,63),
    (0,91,82),
    (219,248,38),
    (2,248,50),
]

walls = {
    '1': pygame.image.load('./sprites/wall1.png'),
    '2': pygame.image.load('./sprites/wall2.png'),
    '3': pygame.image.load('./sprites/wall3.png'),
    '4': pygame.image.load('./sprites/wall4.png'),
    '5': pygame.image.load('./sprites/wall5.png'),
}

sprite1= pygame.image.load('./sprites/sprite1.png')
sprite2= pygame.image.load('./sprites/sprite2.png')
sprite3= pygame.image.load('./sprites/sprite3.png')
sprite4= pygame.image.load('./sprites/sprite4.png')

enemies = [
    {
        'x':100,
        'y':150,
        'sprite': sprite1,
    },
    {
        'x':300,
        'y':180,
        'sprite': sprite2,
    },
    {
        'x':400,
        'y':250,
        'sprite': sprite4,
    },
    {
        'x':320,
        'y':360,
        'sprite': sprite3,
    },
]

#mas huds para mejorar el diseño del juego
hud = pygame.image.load('./sprites/hud.png')
sword = pygame.image.load('./sprites/sword.png')
#tamaño del sprite que se utiliza
sprite_l = 128
#logo del juego 
logo = pygame.image.load('./sprites/logo.png')

class Raycaster(object):
    def __init__(self, screen):
        self.screen = screen
        _, _, self.width, self.heihgt= screen.get_rect()
        self.blocksize = 50
        self.map = []
        self.player = {
            'x': int(self.blocksize + self.blocksize / 2),
            'y': int(self.blocksize + self.blocksize / 2),
            'fov': int(pi/3),
            'a': int(pi/3),
        }
        self.clearZ()

    def clearZ(self):
        self.zbuffer = [9999 for z in range(0,self.width)]

    def point(self, x, y, c=WHITE):
        self.screen.set_at((x,y),c)

    def block(self, x,y, wall):
        for i in range(x,x + self.blocksize):
            for j in range(y,y + self.blocksize):
                tx = int((i - x) * sprite_l / self.blocksize)
                ty = int((j - y) * sprite_l / self.blocksize)
                c = wall.get_at((tx,ty))
                self.point(i,j,c)

    def draw_stake(self,x,h,c,tx):
        start_y = int(self.heihgt/2 - h/2)
        end_y = int(self.heihgt/2 + h/2)
        height = end_y - start_y

        for y in range(start_y,end_y):
            ty = int((y-start_y) * sprite_l/ height)
            color = walls[c].get_at((tx,ty))
            self.point(x,y,color)
            
    def load_map(self, filename):
        with open(filename) as f:
            for line in f.readlines():
                self.map.append(list(line))

    def cast_ray(self, a):
        d = 0
        ox = self.player['x']
        oy = self.player['y']
        
        while True:
            x = int(ox + d * cos(a))
            y = int(oy + d * sin(a))

            i = int(x / self.blocksize)
            j = int(y / self.blocksize)

            if self.map[j][i] != ' ':
                hitx = x -i*self.blocksize
                hity = y -j*self.blocksize

                if 1 < hitx < self.blocksize - 1:
                    maxhit = hitx
                else:
                    maxhit = hity

                tx = int(maxhit * (sprite_l / self.blocksize))
                return d, self.map[j][i], tx

            self.point(x,y,WHITE)
            d += 1
    
    def draw_map(self):
        for x in range(0,500,self.blocksize):
            for y in range(0,500,self.blocksize):
                i = int(x / self.blocksize)
                j = int(y / self.blocksize)
                if self.map[j][i] != ' ':
                    self.block(x,y, walls[self.map[j][i]])
    
    def draw_player(self):
        self.point(self.player['x'],self.player['y'])

    def draw_sprite(self,sprite):
        sprite_a = atan2(sprite['y'] - self.player['y'],sprite['x'] - self.player['x'],)
        
        d = ((self.player['x']-sprite['x'])**2 + (self.player['y'] - sprite['y'])**2)**0.5

        sprite_size = int(500/d * (75))

        sprite_x = int(
            500 + #offset del mapa
            (sprite_a - self.player['a']) * 500/ self.player['fov'] 
            + 250 - sprite_size/2
        )
        sprite_y = int(500/2 - sprite_size/2)
        
        for x in range(sprite_x,sprite_x+sprite_size):
            for y in range(sprite_y,sprite_y+sprite_size):
                if 500 < x < 1000 and self.zbuffer[x-500] >= d:
                    tx = int((x - sprite_x) * sprite_l/sprite_size)
                    ty = int((y-sprite_y) * sprite_l/sprite_size)
                    c = sprite['sprite'].get_at((tx,ty))
                    if c != TRANSPARENT:
                        if x> 500:
                            if self.zbuffer[x-500] >= d:
                                self.point(x,y,c)
                                self.zbuffer[x - 500] = d
                            else:
                                self.point(x,y,c)
                                self.zbuffer[x] = d
    def draw_Hud(self,xi,yi, w = 515, h = 80):
        for x in range(xi, xi + w):
            for y in range(yi, yi + h):
                tx = int((x - xi) * 128/w)
                ty = int((y - yi) * 128/h)
                c = hud.get_at((tx, ty))
                self.point(x,y,c)
    def draw_sword(self, xi, yi, w = 250, h = 250):
        for x in range(xi, xi + w):
            for y in range(yi, yi + h):
                tx = int((x - xi) * 128/w)
                ty = int((y - yi) * 128/h)
                c = sword.get_at((tx, ty))
                if c != TRANSPARENT:
                    self.point(x,y,c)

    def render(self):
        self.draw_map()
        self.draw_player()

        density = 500
        #minimapa
        for i in range(0,density):
            a = self.player['a'] - self.player['fov']/2 + self.player['fov'] * i/density
            d,c, _ = self.cast_ray(a)
        #line
        for i in range(0,500):
            self.point(499,i)
            self.point(500,i)
            self.point(501,i)

        #draw in 3d
        for i in range(0,int(self.width/2)):
            a = self.player['a'] - self.player['fov']/2 + self.player['fov'] * i/(self.width/2)
            self.d,c,tx = self.cast_ray(a)

            x = int(self.width/2) + i
            #con este se controla la profundiadd en la que se pueden llegar a ver las cosas
            if self.d > 0:
                h = self.heihgt/(self.d * cos(a - self.player['a'])) * self.heihgt /10

                if self.zbuffer[i] >= self.d:
                    self.draw_stake(x,h,c,tx)
                    self.zbuffer[i] = self.d

        for enemy in enemies:
            self.point(enemy["x"],enemy["y"],WHITE)
            self.draw_sprite(enemy)
        
        self.draw_sword(800,230)
        self.draw_Hud(500,420)

def text_objects(text, font):
    textSurface = font.render(text, True, BLACK)
    return textSurface, textSurface.get_rect()
            
def main_menu():
    menu_background = pygame.image.load('./sprites/logo.png')
    start = False
    while start == False:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    start = True
        screen.fill(GREEN)
        screen.blit(menu_background, (425,75))
        largeText = pygame.font.Font('freesansbold.ttf', 50)
        smallText = pygame.font.Font('freesansbold.ttf', 30)
        TextSurf, TextRect = text_objects("Enter para comenzar!", largeText) 
        TextRect.center = (500,250)        
        screen.blit(TextSurf,TextRect)
        TextSurf2, TextRect2 = text_objects("Muevete con W,S!", largeText) 
        TextRect2.center = (500,350)        
        screen.blit(TextSurf2,TextRect2)
        TextSurf3, TextRect3 = text_objects("Mueve la camara colocando el mouse. O con A,D", smallText) 
        TextRect3.center = (500,450)        
        screen.blit(TextSurf3,TextRect3)
        pygame.display.update()
        clock = pygame.time.Clock()
        clock.tick(15)
        
def win_screen():
    win_background = pygame.image.load('./sprites/ending.jpg')
    start = False
    while start == False:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    start = True
        screen.fill(GREEN)
        screen.blit(win_background, (0,0))
        largeText = pygame.font.Font('freesansbold.ttf', 50)
        TextSurf, TextRect = text_objects("You did it!", largeText)
        TextRect.center = (500,250)
        screen.blit(TextSurf,TextRect)
        pygame.display.update()
        clock = pygame.time.Clock()
        clock.tick(15)

def show_fps(clock,screen):
    string = "FPS: " + str(int(clock.get_fps()))
    font = pygame.font.SysFont('Arial', 20, True)
    fps = font.render(string,0,WHITE)
    screen.blit(fps, (900,5))


pygame.init()
screen = pygame.display.set_mode((1000,500))
r = Raycaster(screen)
r.load_map('./map.txt')
last_action = ''
camera_movement = 0

#menu
main_menu()
last_x = 0
last_y = 0

running = True
while running:
    d = 10
    camera_movement += 5
    screen.fill(BLACK,(0,0,r.width,r.heihgt))
    screen.fill(SKY,(r.width/2,0,r.width,r.heihgt/2))
    screen.fill(GROUND, (r.width/2,r.heihgt/2,r.width,r.heihgt/2))
    r.render()
    show_fps(CLOCK,screen)
    CLOCK.tick(60)
    r.clearZ()

    pygame.display.flip()
    
    if r.d ==0:
        r.player["x"] = last_x
        r.player["y"] = last_y
    else:
        last_x = r.player["x"]
        last_y = r.player["y"]
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            exit(0)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                r.player['a'] -= pi/10
            if event.key == pygame.K_d:
                r.player['a'] += pi/10
            if event.key == pygame.K_w:
                r.player['x'] += int(d * cos(r.player["a"]))
                r.player['y'] += int(d * sin(r.player["a"]))
            if event.key == pygame.K_s:
                r.player["x"] -= int(d * cos(r.player["a"]))
                r.player["y"] -= int(d * sin(r.player["a"]))
        #movimiento con el mouse
        if event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
            if mouse_pos[0] in list(range(500, 650)):
                r.player["a"] -= pi/10
            elif mouse_pos[0] in list(range(850, 1000)):
                r.player["a"] += pi/10   
    #evento cuando se acerca al tile de la x
    if(385<r.player["x"]<400 and 390<r.player["y"]<427):
        running=False
win_screen()