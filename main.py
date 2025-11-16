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


class Player(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # 이미지 로드
        self.image = pg.image.load('images/playercharacter.png')
        self.image = pg.transform.scale_by(self.image, (0.5, 0.5))
        self.originswordimage = pg.image.load('images/sword.png')
        self.originswordimage = pg.transform.scale_by(self.originswordimage, (0.5, 0.5))
        self.originhpimage = pg.image.load('images/playerhp.png')
        self.originstaminaimage = pg.image.load('images/stamina.png')
        self.staminaimage = self.originstaminaimage
        self.hpimage = self.originhpimage

        # 이미지 처리
        self.rect = self.image.get_rect()
        self.rect.center = (width / 2, height / 2)
        self.swordimage = self.originswordimage
        self.swordsprite = self.swordimage.get_rect()
        self.hpsprite = self.hpimage.get_rect()
        self.hpsprite.center = (width / 30, height / 10)
        self.staminasprite = self.staminaimage.get_rect()
        self.staminasprite.center = (width / 30, height / 10 - height / 20)

        # 변수들
        self.distance = 20
        self.attacking = False
        self.attack_timer = 0
        self.attack_cooltime = 0
        self.hp = 100
        self.stamina = 100

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
        if keys[K_SPACE] and self.stamina > 20:
            self.stamina -= 8
            dx *= 3
            dy *= 3

        self.stamina += 0.5
        if self.stamina > 100:
            self.stamina = 100

        self.rect.move_ip(dx, dy)
        return self.rect.center
    
    def swordmove(self):
        mx, my = pg.mouse.get_pos()
        cx, cy = self.rect.center
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
            self.distance = 20
            self.attacking = False
            self.attack_cooltime = pg.time.get_ticks()
    
    def swordattack(self):
        if self.attack_cooltime - pg.time.get_ticks() < -700:
            self.distance = 40
            self.attacking = True
            self.attack_timer = pg.time.get_ticks()
    
    def staminagauge(self):
        self.staminaimage = pg.transform.rotate(self.originstaminaimage, -90)
        self.staminaimage = pg.transform.scale_by(self.staminaimage, (self.stamina / 100 * 3, 2))

    def hpgauge(self):
        self.hpimage = pg.transform.rotate(self.originhpimage, -90)
        self.hpimage = pg.transform.scale_by(self.hpimage, (self.hp / 100 * 3, 2))


class Bullet(pg.sprite.Sprite):
    def __init__(self, x, y, target_pos):
        super().__init__()
        self.image = pg.Surface((10, 10))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(center=(x, y))

        dx = target_pos[0] - x
        dy = target_pos[1] - y
        length = math.hypot(dx, dy)
        if length == 0:
            length = 1
        self.dir_x = dx / length
        self.dir_y = dy / length
        self.speed = 8

    def update(self):
        self.rect.x += self.dir_x * self.speed
        self.rect.y += self.dir_y * self.speed
        if (self.rect.right < 0 or self.rect.left > width or
            self.rect.bottom < 0 or self.rect.top > height):
            self.kill()


class Boss(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        #이미지 로드
        self.image = pg.image.load('images/boss.png')
        self.image = pg.transform.scale_by(self.image, (0.7, 0.7))
        self.originhpimage = pg.image.load('images/playerhp.png')
        self.hpimage = self.originhpimage

        #이미지 처리
        self.rect = self.image.get_rect()
        self.rect.center = (width // 2, height // 5)
        self.hpsprite = self.hpimage.get_rect()
        self.hpsprite.center = (width // 2, height // 20)

        #변수
        self.hp = 300
        self.last_shot = 0
        self.shot_delay = 1000


    def update(self, player_pos, bullet_group):
        now = pg.time.get_ticks()
        if now - self.last_shot > self.shot_delay:
            bullet = Bullet(self.rect.centerx, self.rect.centery, player_pos)
            bullet_group.add(bullet)
            self.last_shot = now

    def hpgauge(self):
        self.hpimage = pg.transform.rotate(self.originhpimage, -90)
        self.hpimage = pg.transform.scale_by(self.hpimage, (self.hp / 300 * 5, 2))


# 메인 실행
pg.init()
pg.display.set_caption('zzilerman')
maindisplay = pg.display.set_mode((width, height), 0, 32)
clock = pg.time.Clock()

P1 = Player()
Boss1 = Boss()

boss_group = pg.sprite.Group()
bullet_group = pg.sprite.Group()
boss_group.add(Boss1)

while True:
    maindisplay.fill(white)
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            sys.exit()
        if event.type == pg.MOUSEBUTTONDOWN:
            P1.swordattack()

    # 업데이트
    player_pos = P1.move()
    P1.swordmove()
    P1.hpgauge()
    P1.staminagauge()
    boss_group.update(player_pos, bullet_group)
    bullet_group.update()

    # 충돌 처리
    hits = pg.sprite.spritecollide(P1, bullet_group, True, pg.sprite.collide_rect)
    if hits:
        P1.hp -= 10
        if P1.hp <= 0:
            print("플레이어 사망!")
            pg.quit()
            sys.exit()

    if P1.attacking:
        for boss in boss_group:
            if P1.swordsprite.colliderect(boss.rect):
                boss.hp -= 20
                print("보스 피격! HP:", boss.hp)
                if boss.hp <= 0:
                    print("보스 처치!")
                    boss.kill()

    # 그리기
    maindisplay.blit(P1.image, P1.rect)
    maindisplay.blit(P1.swordimage, P1.swordsprite)
    maindisplay.blit(P1.hpimage, P1.hpsprite)
    maindisplay.blit(P1.staminaimage, P1.staminasprite)

    boss_group.draw(maindisplay)
    bullet_group.draw(maindisplay)
    for boss in boss_group:
        boss.hpgauge()
        maindisplay.blit(boss.hpimage, boss.hpsprite)

    pg.display.update()
    clock.tick(fps)