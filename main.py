import pygame as pg
import math
import sys
import random
from pygame.locals import *

# ----- 기본 설정 -----
width = 1080
height = 720
white = (255, 255, 255)
black = (0, 0, 0)
fps = 30
movespeed = 7
ui_height = 100  # 상단 UI 영역 높이

# ----- 사운드 -----

pg.init()
pg.mixer.init()
pg.mixer.music.load("musics/bgm.mp3")
attack_sound = pg.mixer.Sound("musics/attacking.wav")
before_attack_sound = pg.mixer.Sound("musics/before_attack.wav")
swing_sound = pg.mixer.Sound("musics/sword_swing.wav")
victory_sound = pg.mixer.Sound("musics/victory.mp3")

pg.mixer.music.set_volume(0.1)
attack_sound.set_volume(1.0)
before_attack_sound.set_volume(0.1)
swing_sound.set_volume(1.0)
victory_sound.set_volume(1.0)

# ----- 화면 텍스트 함수 -----
def draw_text(surface, text, size, x, y, color=black):
    font = pg.font.SysFont('arial', size)
    surf = font.render(text, True, color)
    rect = surf.get_rect()
    rect.center = (x, y)
    surface.blit(surf, rect)

# ----- 시작 화면 -----
def show_start_screen():
    pg.mixer.music.play(-1)
    maindisplay.fill(white)
    draw_text(maindisplay, "ZZILER MAN", 72, width // 2, height // 3)
    draw_text(maindisplay, "Press any key to start", 36, width // 2, height // 2)
    pg.display.update()
    waiting = True
    while waiting:
        clock.tick(fps)
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()
            if event.type == KEYDOWN or event.type == MOUSEBUTTONDOWN:
                waiting = False
                return

# ----- 게임오버 화면 -----
def show_gameover_screen(time_survived, boss_hp):
    pg.mixer.music.stop()
    maindisplay.fill(white)
    draw_text(maindisplay, "GAME OVER", 72, width // 2, height // 3)
    draw_text(maindisplay, f"Time Survived: {time_survived:.2f} s", 36, width // 2, height // 2)
    draw_text(maindisplay, f"Boss HP Left: {boss_hp}", 36, width // 2, height // 2 + 50)
    draw_text(maindisplay, "Press any key to restart", 36, width // 2, height // 2 + 120)
    pg.display.update()

    min_wait = 1200  # ms
    start = pg.time.get_ticks()

    waiting = True
    while waiting:
        clock.tick(fps)
        now = pg.time.get_ticks()
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit(); sys.exit()
            if now - start >= min_wait and (event.type == KEYDOWN or event.type == MOUSEBUTTONDOWN):
                pg.mixer.music.play(-1)
                waiting = False
                return  # restart game

# ----- 클리어 화면 -----
def show_clear_screen(time_survived):
    pg.mixer.music.stop()
    victory_sound.play()
    maindisplay.fill(white)
    draw_text(maindisplay, "CLEAR!", 72, width // 2, height // 3)
    draw_text(maindisplay, f"Time Survived: {time_survived:.2f} s", 36, width // 2, height // 2)
    draw_text(maindisplay, "Press any key to exit", 36, width // 2, height // 2 + 80)
    pg.display.update()
    min_wait = 1200
    start = pg.time.get_ticks()
    while True:
        clock.tick(fps)
        now = pg.time.get_ticks()
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()
            if now - start >= min_wait and (event.type == KEYDOWN or event.type == MOUSEBUTTONDOWN):
                pg.quit()
                sys.exit()
            if event.type == KEYDOWN or event.type == MOUSEBUTTONDOWN:
                pg.quit()
                sys.exit()


# ----- 플레이어 클래스 -----
class Player(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.image.load('images/playercharacter.png')
        self.image = pg.transform.scale_by(self.image, (0.5, 0.5))
        self.originswordimage = pg.image.load('images/sword.png')
        self.originswordimage = pg.transform.scale_by(self.originswordimage, (0.5, 0.5))
        self.originhpimage = pg.image.load('images/playerhp.png')
        self.hpimage = self.originhpimage

        self.rect = self.image.get_rect()
        self.rect.center = (width / 2, ui_height + (height - ui_height) / 6 * 5)
        self.swordimage = self.originswordimage
        self.swordsprite = self.swordimage.get_rect()
        self.hpsprite = self.hpimage.get_rect()
        self.hpsprite.center = (width // 30, ui_height // 2)

        self.distance = 20
        self.attacking = False
        self.attack_timer = 0
        self.attack_cooltime = 0
        self.hp = 100

    def move(self):
        keys = pg.key.get_pressed()
        dx, dy = 0, 0
        if self.rect.left > 0 and keys[K_a]:
            dx = -movespeed
        if self.rect.right < width and keys[K_d]:
            dx = movespeed
        if self.rect.top > ui_height and keys[K_w]:
            dy = -movespeed
        if self.rect.bottom < height and keys[K_s]:
            dy = movespeed
        self.rect.move_ip(dx, dy)
        return self.rect.center

    def swordmove(self):
        mx, my = pg.mouse.get_pos()
        cx, cy = self.rect.center
        dx = mx - cx
        dy = my - cy
        length = math.hypot(dx, dy)
        if length == 0: length = 1
        dir_x, dir_y = dx / length, dy / length
        sword_x, sword_y = cx + dir_x * self.distance, cy + dir_y * self.distance
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
            swing_sound.play()

    def hpgauge(self):
        self.hp = max(self.hp, 0)
        self.hpimage = pg.transform.rotate(self.originhpimage, -90)
        self.hpimage = pg.transform.scale_by(self.hpimage, (self.hp / 100 * 3, 2))

# ----- 총알 클래스 -----
class Bullet(pg.sprite.Sprite):
    def __init__(self, x, y, target_pos):
        super().__init__()
        self.image = pg.Surface((10, 10))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(center=(x, y))
        dx, dy = target_pos[0] - x, target_pos[1] - y
        length = math.hypot(dx, dy) or 1
        self.dir_x, self.dir_y = dx / length, dy / length
        self.speed = 8

    def update(self):
        self.rect.x += self.dir_x * self.speed
        self.rect.y += self.dir_y * self.speed
        if (self.rect.right < 0 or self.rect.left > width or
            self.rect.bottom < ui_height or self.rect.top > height):
            self.kill()

# ----- 보스 클래스 -----
class Boss(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.image.load('images/boss.png')
        self.image = pg.transform.scale_by(self.image, (2.0, 2.0))
        self.originhpimage = pg.image.load('images/playerhp.png')
        self.hpimage = self.originhpimage

        self.rect = self.image.get_rect()
        self.rect.center = (width // 2, ui_height + (height-ui_height) // 2)
        self.hpsprite = self.hpimage.get_rect()
        self.hpsprite.center = (width*7 // 15, ui_height // 2)

        self.hp = 300
        self.last_shot = 0
        self.shot_delay = 1500
        self.attack_zone = None
        self.attack_active = False
        self.attack_time = 0
        self.pre_delay = 0

        self.charging = False
        self.charge_dir = (0, 0)
        self.charge_speed = 18
        self.charge_duration = 350
        self.charge_start = 0
        self.charge_preview_time = 500
        self.charge_distance = 400
        self.charge_width = 50

        self.touch_damage_delay = 700
        self.last_touch_damage = 0


    def update(self, player_pos, bullet_group, player):
        now = pg.time.get_ticks()

        # 패턴 발동
        if not self.attack_active and not self.charging and now - self.last_shot >= self.shot_delay:
            pattern = random.choice([1, 2, 3, 4, 5, 6])
            if pattern == 1: 
                self.pattern1(player_pos, bullet_group)
                attack_sound.play()
            if pattern == 2: 
                self.pattern2(player_pos, bullet_group)
                attack_sound.play()
            if pattern == 3: 
                before_attack_sound.play()
                self.pattern3(player_pos)
            if pattern == 4: 
                before_attack_sound.play()
                self.pattern4(player_pos)
            if pattern == 5: 
                before_attack_sound.play()
                self.pattern5(player_pos)
            if pattern == 6: 
                before_attack_sound.play()
                self.pattern6(player_pos)
            self.attack_active = True
            self.attack_time = now

        # 선딜 진행
        if self.attack_active and not self.charging:
            if now - self.attack_time >= self.pre_delay:
                self.resolve_attack(player_pos, player)
                self.attack_active = False
                self.attack_zone = None
                self.last_shot = now

        # 돌진 이동
        if self.charging:
            if now - self.charge_start <= self.charge_duration:
                new_x = self.rect.x + self.charge_dir[0] * self.charge_speed
                new_y = self.rect.y + self.charge_dir[1] * self.charge_speed
                # 전투 영역 경계 체크
                new_x = max(0, min(width - self.rect.width, new_x))
                new_y = max(ui_height, min(height - self.rect.height, new_y))
                self.rect.x = new_x
                self.rect.y = new_y

                # 돌진 범위 내 플레이어 데미지
                px, py = player.rect.center
                cx, cy = self.rect.center
                vx, vy = self.charge_dir
                px_rel, py_rel = px - cx, py - cy
                proj = px_rel * vx + py_rel * vy
                if 0 <= proj <= self.charge_distance:
                    perp = abs(px_rel * vy - py_rel * vx)
                    if perp <= self.charge_width / 2:
                        if now - self.last_touch_damage > self.touch_damage_delay:
                            player.hp -= 20
                            self.last_touch_damage = now
                            attack_sound.play()
            else:
                self.charging = False
                self.attack_active = False
                self.attack_zone = None
                self.last_shot = now


    
    # ----- 패턴 정의 -----
    def pattern1(self, player_pos, bullet_group):
        bullet_group.add(Bullet(*self.rect.center, player_pos))

    def pattern2(self, player_pos, bullet_group):
        cx, cy = self.rect.center
        dx, dy = player_pos[0]-cx, player_pos[1]-cy
        length = math.hypot(dx,dy) or 1
        dir_x, dir_y = dx/length, dy/length
        offset = 25
        for i in range(3):
            bx = cx + dir_x*offset*i
            by = cy + dir_y*offset*i
            bullet_group.add(Bullet(bx, by, player_pos))

    def pattern3(self, player_pos):
        cx, cy = self.rect.center
        dx, dy = player_pos[0]-cx, player_pos[1]-cy
        angle = math.degrees(math.atan2(dy, dx))
        self.attack_zone = ("sector", (cx, cy, 200, angle - 30, angle + 30))
        self.pre_delay = 500

    def pattern4(self, player_pos):
        cx, cy = self.rect.center
        size = max(self.rect.width, self.rect.height)
        self.attack_zone = ("ring", (cx, cy, size * 1.3, size * 3))
        self.pre_delay = 700

    def pattern5(self, player_pos):
        cx, cy = self.rect.center
        dx, dy = player_pos[0]-cx, player_pos[1]-cy
        length = math.hypot(dx, dy) or 1
        dir_x, dir_y = dx/length, dy/length
        self.charge_dir = (dir_x, dir_y)
        self.attack_zone = ("charge", self.charge_dir)
        self.pre_delay = self.charge_preview_time

    def pattern6(self, player_pos):
        px, py = player_pos
        self.attack_zone = ("explosion", (px, py, 70))
        self.pre_delay = 900

    # ----- 공격 판정 -----
    def resolve_attack(self, player_pos, player):
        if not self.attack_zone: return
        kind, data = self.attack_zone
        px, py = player_pos

        if kind == "sector":
            cx, cy, radius, ang_min, ang_max = data
            dx, dy = px-cx, py-cy
            dist = math.hypot(dx, dy)
            ang = math.degrees(math.atan2(dy, dx))
            attack_sound.play()
            if dist <= radius and ang_min <= ang <= ang_max:
                player.hp -= 15
                

        elif kind == "ring":
            cx, cy, safe, danger = data
            dx, dy = px-cx, py-cy
            dist = math.hypot(dx, dy)
            attack_sound.play()
            if safe < dist <= danger:
                player.hp -= 30

        elif kind == "charge":
            self.charging = True
            self.charge_start = pg.time.get_ticks()
            attack_sound.play()

        elif kind == "explosion":
            x, y, r = data
            attack_sound.play()
            if math.hypot(px-x, py-y) <= r:
                player.hp -= 25

    # ----- 공격 범위 그리기 -----
    def draw_attack_zone(self, surface):
        if not self.attack_zone: return
        kind, data = self.attack_zone

        if kind == "sector":
            cx, cy, radius, ang_min, ang_max = data
            points = [(cx, cy)]
            for ang in range(int(ang_min), int(ang_max) + 1, 5):
                rad = math.radians(ang)
                x = cx + radius * math.cos(rad)
                y = cy + radius * math.sin(rad)
                points.append((x, y))
            pg.draw.polygon(surface, (255, 0, 0, 100), points)

        elif kind == "ring":
            cx, cy, safe, danger = data
            pg.draw.circle(surface, (255, 0, 0, 100), (cx, cy), danger)
            pg.draw.circle(surface, (255, 255, 255, 100), (cx, cy), safe)

        elif kind == "charge":
            dir_x, dir_y = data
            length = self.charge_distance
            width = self.charge_width
            surf = pg.Surface((length, width), pg.SRCALPHA)
            surf.fill((255, 0, 0))
            angle = math.degrees(math.atan2(-dir_y, dir_x))
            rotated_surf = pg.transform.rotate(surf, angle)
            cx, cy = self.rect.center
            center_x = cx + dir_x * length / 2
            center_y = cy + dir_y * length / 2
            rect = rotated_surf.get_rect(center=(center_x, center_y))
            surface.blit(rotated_surf, rect.topleft)

        elif kind == "explosion":
            x, y, r = data
            pg.draw.circle(surface, (255,120,0), (int(x), int(y)), r, 3)

    # HP 표시
    def hpgauge(self):
        self.hp = max(self.hp, 0)
        self.hpimage = pg.transform.rotate(self.originhpimage, -90)
        self.hpimage = pg.transform.scale_by(self.hpimage, (self.hp / 300 * 10, 2))

# ----- 메인 실행 -----
pg.display.set_caption('zzilerman')
maindisplay = pg.display.set_mode((width, height), 0, 32)
clock = pg.time.Clock()

show_start_screen()

while True:
    P1 = Player()
    Boss1 = Boss()
    boss_group = pg.sprite.Group(Boss1)
    bullet_group = pg.sprite.Group()

    start_ticks = pg.time.get_ticks()
    running = True
    cleared = False

    while running:
        dt = clock.tick(fps)
        maindisplay.fill(white)

        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                P1.swordattack()

        player_pos = P1.move()
        P1.swordmove()
        P1.hpgauge()
        boss_group.update(player_pos, bullet_group, P1)
        bullet_group.update()

        # --- 충돌 처리 ---
        hits = pg.sprite.spritecollide(P1, bullet_group, True)
        if hits:
            P1.hp -= 10
            P1.hp = max(P1.hp, 0)
            if P1.hp <= 0:
                running = False

        for boss in boss_group:
            if P1.rect.colliderect(boss.rect):
                now = pg.time.get_ticks()
                if now - boss.last_touch_damage > boss.touch_damage_delay:
                    P1.hp -= 5
                    P1.hp = max(P1.hp, 0)
                    boss.last_touch_damage = now
                    if P1.hp <= 0:
                        running = False

        if P1.attacking:
            for boss in boss_group:
                if P1.swordsprite.colliderect(boss.rect):
                    boss.hp -= 5
                    boss.hp = max(boss.hp, 0)
                    if boss.hp <= 0:
                        boss.kill()

        # --- UI 영역 ---
        pg.draw.rect(maindisplay, (220,220,220), (0, 0, width, ui_height))
        maindisplay.blit(P1.hpimage, P1.hpsprite)
        for boss in boss_group:
            boss.hpgauge()
            maindisplay.blit(boss.hpimage, boss.hpsprite)

        # --- 전투 공간 배경 ---
        pg.draw.rect(maindisplay, (255,255,255), (0, ui_height, width, height-ui_height))

        # --- 전투 요소 표시 ---
        for boss in boss_group:
            boss.draw_attack_zone(maindisplay)
        boss_group.draw(maindisplay)
        bullet_group.draw(maindisplay)
        maindisplay.blit(P1.image, P1.rect)
        maindisplay.blit(P1.swordimage, P1.swordsprite)

        pg.display.update()

        if not boss_group:
            running = False
            cleared = True

    end_ticks = pg.time.get_ticks()
    time_survived = (end_ticks - start_ticks) / 1000

    if cleared:
        show_clear_screen(time_survived)
    else:
        show_gameover_screen(time_survived, Boss1.hp)
