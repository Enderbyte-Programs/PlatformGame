###Platform Game (c) 2022 Enderbyte Programs LLC
import pygame
import json
import sys
import os
import random
from time import sleep

def preinit():
    if "--stripped" in sys.argv:
        return True
    else:
        return False

STRIPPED = preinit()
X_SIZE = 1280
Y_SIZE = 720

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
    draw_text_middle(win,"Enderbyte Programs",64,(0,0,255))
    draw_text(win,message,24,(0,0,255),0,0)
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
                        lose_menu(win,score)
                        
            self.prevpos.insert(0,(self.gx,self.gy))
            self.prevpos = self.prevpos[0:20]
            
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
    global X_SIZE
    global Y_SIZE
    global score
    lockcamera = False
    DEBUG = False
    paused = False
    gravity = 1
    jumptick = 0
    camera = [35,-180]
    player = DrawableRect(camera[0],camera[1],30,30,(0,0,255),"player",True,False)
    poffset = (0,0)
    pofx = []
    ents.append(DrawableRect(600,600,100,100,(255,0,0),"",False,False))
    tick = 0
    ents = []
    score = 0
    #print(ents)
    while True:
        if not paused:
            tick += 1
        poffset = (camera[0]//1000,camera[1]//1000)
        for opy in range(-2,2):
            for opx in range(-2,2):

                if (poffset[0]+opx,poffset[1]+opy) not in pofx:
                    
                    for i in range(100):
                        nx = DrawableRect(random.randint(-1000+(poffset[0]+opx)*1000,1000+(poffset[0]+opx)*1000),random.randint(-1000+(poffset[1]+opy)*1000,1000+(poffset[1]+opy)*1000),50,50,(0,255,0),"",False,True)
                        assm = (nx.gx//1000,nx.gy//1000)
                        #print(assm)
                        if assm not in pofx and (nx.gx > player.gx + 200 or nx.gx < player.gx - 100) and (nx.gy > player.gy + 200 or nx.gy < player.gy):
                            ents.append(nx)
                pofx.append((poffset[0]+opx,poffset[1]+opy))
        #print(len(ents))
        if tick > 100 and len(ents) > 2000:

            ents = ents[1000:]
        if tick / 10 == tick // 10:
            score += 1
        win.fill((255,255,255))
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = not paused
                elif event.key == pygame.K_F3:
                    DEBUG = not DEBUG
                elif event.key == pygame.K_l:
                    lockcamera = not lockcamera
            elif event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.VIDEORESIZE:
                win = pygame.display.set_mode((event.w, event.h),pygame.RESIZABLE)
                X_SIZE = event.w
                Y_SIZE = event.h
                camera = [player.gx,player.gy]
        k = pygame.key.get_pressed()
        
        for ent in ents:
            ent.draw(win)
            ent.update(k)
    
        player.draw(win)
        if not paused:
            player.update(k)
        if not lockcamera:
            camera = [player.gx,player.gy]
        if not paused:
            player.gy += gravity
        else:
            draw_text(win,"You are paused. Press ESCAPE to resume.",32,(0,0,0),100,100)
        if gravity < 10:
            gravity += 1
        if jumptick > 0:
            player.gy -= jumptick
            jumptick -= 1
        draw_text(win,f"{-camera[0]},{-camera[1]}",24,(0,0,255),0,0)
        if DEBUG:
            draw_text(win,str(round(clock.get_fps()))+" FPS",24,(0,0,255),100,0)
        draw_text(win,f"Score: {score}",24,(0,0,0),0,20)
        pygame.display.update()
        pygame.display.flip()
        clock.tick(60)  

def main_menu(win):
    while True:
        win.fill((0,0,0))
        draw_text_middle(win,"SkiFree",64,(0,0,255))
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

def lose_menu(win,score: int) -> None:
    while True:
        win.fill((0,0,0))
        draw_text_middle(win,f"You lose. Score: {score}",64,(255,0,0))
        draw_text(win,f"Press Enter to play again",28,(255,255,255),0,0)
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

def pause_menu(win) -> None:
    while True:
        win.fill((0,0,0))
        draw_text_middle(win,"You are paused. Press escape to resume",64,(255,0,0))
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
            elif event.type == pygame.QUIT:
                sys.exit()
        pygame.display.update()
        clock.tick(60)

def main():
    global win
    win = pygame.display.set_mode((X_SIZE,Y_SIZE),pygame.RESIZABLE)
    pygame.display.set_caption("SkiFree")
    init(win)
    main_menu(win)
main()