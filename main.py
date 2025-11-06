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
        self.chartimage = pg.image.load('images/playercharacter.png')
        self.originswordimage = pg.image.load('images/sword.png')
        self.originstaminaimage = pg.image.load('images/stamina.png')
        self.originhpimage = pg.image.load('images/playerhp.png')
        
        self.charsprite = self.chartimage.get_rect()
        self.charsprite.center = (width / 2, height / 2)

        self.swordimage = self.originswordimage
        self.swordsprite = self.swordimage.get_rect()
        
        self.hpimage = self.originhpimage
        self.hpsprite = self.hpimage.get_rect()
        self.hpsprite.center = (width / 30, height / 10)
        
        self.staminaimage = self.originstaminaimage
        self.staminasprite = self.staminaimage.get_rect()
        self.staminasprite.center = (width / 30, height / 10 - height / 20)

        self.distance = 30
        self.attacking = False
        self.attack_timer = 0
        self.attack_cooltime = 0
        self.hp = 100
        self.stamina = 100

    def move(self):
        keys = pg.key.get_pressed()
        dx, dy = 0, 0
        if self.charsprite.left > 0 and keys[K_a]:
            dx = -movespeed
        if self.charsprite.right < width and keys[K_d]:
            dx = movespeed
        if self.charsprite.top > 0 and keys[K_w]:
            dy = -movespeed
        if self.charsprite.bottom < height and keys[K_s]:
            dy = movespeed
        if self.charsprite.bottom < height and self.charsprite.top > 0 and self.charsprite.left > 0 and self.charsprite.right < width and keys[K_SPACE] and self.stamina > 20:
            self.stamina -= 8
            dx *= 3
            dy *= 3
        self.stamina += 0.5
        if self.stamina > 100:
            self.stamina = 100
        self.charsprite.move_ip(dx, dy)
        position = self.charsprite.center
        return position
    
    def swordmove(self):
        mx, my = pg.mouse.get_pos()
        cx = self.charsprite.centerx
        cy = self.charsprite.centery
        dx = mx - cx
        dy = my - cy

        length = math.hypot(dx, dy)
        if length == 0:
            length = 1
        
        dir_x = dx / length
        dir_y = dy / length

        sword_x = cx + dir_x * self.distance
        sword_y = cy + dir_y * self.distance
        self.swordsprite.center = (sword_x, sword_y)

        angle_rad = -math.atan2(dx, dy)
        angle_deg = math.degrees(angle_rad) + 180

        self.swordimage = pg.transform.rotate(self.originswordimage, -angle_deg)
        self.swordsprite = self.swordimage.get_rect(center=self.swordsprite.center)
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
    
    def staminagauge(self):
        self.staminaimage = pg.transform.rotate(self.originstaminaimage, -90)
        self.staminaimage = pg.transform.scale_by(self.staminaimage, (self.stamina / 100 * 3, 2))
        pass

    def hpgauge(self):
        self.hpimage = pg.transform.rotate(self.originhpimage, -90)
        self.hpimage = pg.transform.scale_by(self.hpimage, (self.hp / 100 * 3, 2))
        
        pass
    



pg.init()
pg.display.set_caption('zzilerman')
font = pg.font.SysFont(None, 30, False, False)
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
    text = font.render("stamina: " + str(P1.stamina), True, black, None)
    P1.move() 
    P1.swordmove()
    P1.hpgauge()
    P1.staminagauge()
    maindisplay.blit(P1.chartimage, P1.charsprite)
    maindisplay.blit(P1.swordimage, P1.swordsprite)
    maindisplay.blit(P1.hpimage, P1.hpsprite)
    maindisplay.blit(P1.staminaimage, P1.staminasprite)
    
    maindisplay.blit(text, [0, 0])
    pg.display.update()
    clock.tick(fps)
