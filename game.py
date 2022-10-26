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
ents = []
class DrawableRect():
    def __init__(self,gx: int,gy: int,sx: int,sy: int,colour,callsign="__ENTITY__",allowmovement=False,collide=False):
        self.gx = gx
        self.gy = gy
        self.sx = sx
        self.sy = sy
        self.colour = colour
        self.callsign = callsign
        self.speed = 10
        self.am = allowmovement
        self.surf = pygame.Surface((self.sx,self.sy))
        self.surf.fill(self.colour)
        self.collide = collide
        self.prevpos = []
    def draw(self,win):
        
        self.rect = pygame.Rect(self.gx-(camera[0]-X_SIZE//2),self.gy-(camera[1]-Y_SIZE//2),self.sx,self.sy)
        win.blit(self.surf,self.rect)
    def update(self,pressed_keys):
        global gravity
        global jumptick
        if self.am:
            if pressed_keys[pygame.K_UP]:
                if jumptick == 0:
                    jumptick = 30
            if pressed_keys[pygame.K_DOWN]:
                self.gy += self.speed
            if pressed_keys[pygame.K_RIGHT]:
                self.gx += self.speed
            if pressed_keys[pygame.K_LEFT]:
                self.gx -= self.speed
            for e in ents:
                if e is not self:
                    if self.rect.colliderect(e.rect):
                        print("Collision detected")
                        self.gx, self.gy = self.prevpos[0]
                        jumptick = 0
                        if e.gy > self.gy:
                            self.gy -= 1
                            gravity = 0
                        
            self.prevpos.insert(0,(self.gx,self.gy))
            self.prevpos = self.prevpos[0:4]
            
    def __repr__(self) -> str:
        return str(self.callsign)

def findbycallsign(ents: list,calls: str):
    try:
        vents = [e.callsign for e in ents]
        return ents[vents.index(calls)]
    except ValueError:
        return None

def game2local(x,y):
    return (camera[0] + x,camera[1] + y)

def local2game(x,y):
    return (camera[0] - x, camera[1] - y)

def game(win):
    global camera
    global ents
    global gravity
    global jumptick
    lockcamera = False
    gravity = 1
    jumptick = 0
    camera = [35,-180]
    player = DrawableRect(camera[0],camera[1],30,30,(255,255,255),"player",True,False)
    
    ents.append(DrawableRect(600,600,100,100,(255,0,0),"",False,False))
    ents.append(DrawableRect(0,0,1000,50,(0,255,0),allowmovement=False,collide=True))
    ents.append(DrawableRect(900,-100,500,50,(0,0,255),allowmovement=False,collide=True))
    print(ents)
    while True:
        win.fill((0,0,0))
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
                elif event.key == pygame.K_RETURN:
                    game(win)
                elif event.key == pygame.K_l:
                    lockcamera = not lockcamera
            elif event.type == pygame.QUIT:
                sys.exit()
        k = pygame.key.get_pressed()
        for ent in ents:
            ent.draw(win)
            ent.update(k)
    
        player.draw(win)
        player.update(k)
        if not lockcamera:
            camera = [player.gx,player.gy]
        player.gy += gravity
        if gravity < 30:
            gravity += 1
        if jumptick > 0:
            player.gy -= jumptick
            jumptick -= 1
        draw_text(win,f"{-camera[0]},{-camera[1]}",24,(255,255,255),0,0)
        draw_text(win,str(round(clock.get_fps()))+" FPS",24,(255,255,255),100,0)
        pygame.display.update()
        pygame.display.flip()
        clock.tick(60)  

def main_menu(win):
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