###Platform Game (c) 2022 Enderbyte Programs LLC
import pygame
import json
import sys
import os
from time import sleep

def preinit():
    if "--stripped" in sys.argv:
        return True
    else:
        return False

STRIPPED = preinit()
X_SIZE = 1280
Y_SIZE = 720
GAMESIZEX = 1000
GAMESIZEY = 1000

pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()

def draw_text_middle(surface, text, size, color):
    font = pygame.font.SysFont("Consolas", size, bold=True)
    label = font.render(text, 1, color)
    surface.blit(label, (X_SIZE//2-(label.get_width()//2),Y_SIZE//2-(label.get_height()//2)))

def draw_text(surface,text,size,color,x,y):
    font = pygame.font.SysFont("Colsolas",size)
    label = font.render(text,False,color)
    surface.blit(label,(x,y))

def drawbtext(win,message):
    win.fill ((0,0,0))
    draw_text_middle(win,"Enderbyte Programs",64,(255,255,255))
    draw_text(win,message,24,(255,255,255),0,0)
    pygame.display.update()

def init(win):
    drawbtext(win,"Loading...")

class DrawableRect():
    def __init__(self,gx: int,gy: int,sx: int,sy: int,colour,callsign="__ENTITY__"):
        self.gx = gx
        self.gy = gy
        self.sx = sx
        self.sy = sy
        self.colour = colour
        self.callsign = callsign
    def draw(self,win):
        self.surf = pygame.Surface((self.sx,self.sy))
        self.surf.fill(self.colour)
        self.rect = pygame.Rect(self.sx+(camera[0]-GAMESIZEX//2),self.sy+(camera[1]-GAMESIZEY//2),self.sx,self.sy)
        win.blit(self.surf,self.rect)
    def __repr__(self) -> str:
        return str(self.callsign)

def findbycallsign(ents: list,calls: str):
    try:
        vents = [e.callsign for e in ents]
        return ents[vents.index(calls)]
    except ValueError:
        return None

def game(win):
    global camera
    camera = [GAMESIZEX//2+X_SIZE//2,GAMESIZEY//2+Y_SIZE//2]
    ents = []
    player = DrawableRect(500,500,30,30,(255,255,255),callsign="__pl")
    ents.append(player)
    print(ents)
    while True:
        win.fill((0,0,0))
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
                elif event.key == pygame.K_RETURN:
                    game(win)
            elif event.type == pygame.QUIT:
                sys.exit()
        for ent in ents:
            ent.draw(win)
        k = pygame.key.get_pressed()
        if k[pygame.K_UP]:
            camera[1] -= 5
            findbycallsign(ents,"__pl").gy -= 5
        if k[pygame.K_DOWN]:
            camera[1] += 5
            findbycallsign(ents,"__pl").gy += 5
        if k[pygame.K_LEFT]:
            camera[0] -= 5
            findbycallsign(ents,"__pl").gx -= 5
        if k[pygame.K_RIGHT]:
            camera[0] += 5
            findbycallsign(ents,"__pl").gx += 5
        draw_text(win,str(camera),24,(255,255,255),0,0)
        pygame.display.update()
        clock.tick(60)  

def main_menu(win):
    sleep(1)
    while True:
        win.fill((0,0,0))
        draw_text_middle(win,"Platform game",64,(255,255,255))
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
                elif event.key == pygame.K_RETURN:
                    game(win)
            elif event.type == pygame.QUIT:
                sys.exit()
        pygame.display.update()
        clock.tick(60)    

def main():
    win = pygame.display.set_mode((X_SIZE,Y_SIZE))
    pygame.display.set_caption("Platform Game")
    init(win)
    main_menu(win)
main()