import pygame as pg
import math
import sys
from pygame.locals import *

width = 1080
height = 720
white = (255, 255, 255)
black = (0, 0, 0)
fps = 30
movespeed = 7


class player(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.image.load('images/playercharacter.png')
        self.rect = self.image.get_rect()
        self.originsword = pg.image.load('images/sword.png')
        self.sword = self.originsword
        self.swordrect = self.sword.get_rect()
        self.rect.center = (width / 2, height / 2)
        self.distance = 30
        self.attacking = False
        self.attack_timer = 0
        self.attack_cooltime = 0

    def move(self):
        keys = pg.key.get_pressed()
        dx, dy = 0, 0
        if self.rect.left > 0 and keys[K_a]:
             dx = -movespeed
        if self.rect.right < width and keys[K_d]:
             dx = movespeed
        if self.rect.top > 0 and keys[K_w]:
             dy = -movespeed
        if self.rect.bottom < height and keys[K_s]:
             dy = movespeed
        self.rect.move_ip(dx, dy)
        position = self.rect.center
        return position
    
    def swordmove(self):
        mx, my = pg.mouse.get_pos()
        cx = self.rect.centerx
        cy = self.rect.centery
        dx = mx - cx
        dy = my - cy

        length = math.hypot(dx, dy)
        if length == 0:
            length = 1
        
        dir_x = dx / length
        dir_y = dy / length

        sword_x = cx + dir_x * self.distance
        sword_y = cy + dir_y * self.distance
        self.swordrect.center = (sword_x, sword_y)

        angle_rad = -math.atan2(dx, dy)
        angle_deg = math.degrees(angle_rad) + 180

        self.sword = pg.transform.rotate(self.originsword, -angle_deg)
        self.swordrect = self.sword.get_rect(center=self.swordrect.center)
        if self.attacking and pg.time.get_ticks() - self.attack_timer > 50:
            print("attack!")
            self.distance = 30
            self.attacking = False
            self.attack_cooltime = pg.time.get_ticks()
    
    def swordattack(self):
        if self.attack_cooltime - pg.time.get_ticks() < -700:
            self.distance = 50
            self.attacking = True
            self.attack_timer = pg.time.get_ticks()




pg.init()
pg.display.set_caption('zzilerman')
maindisplay = pg.display.set_mode((width, height), 0, 32)
maindisplay.fill(white)
clock = pg.time.Clock()

P1 = player()

while True:
    maindisplay.fill(white)
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            sys.exit()
        if event.type == pg.MOUSEBUTTONDOWN:
            P1.swordattack()
    P1.move() 
    P1.swordmove()
    maindisplay.blit(P1.image, P1.rect)
    maindisplay.blit(P1.sword, P1.swordrect)
    pg.display.update()
    clock.tick(fps)
