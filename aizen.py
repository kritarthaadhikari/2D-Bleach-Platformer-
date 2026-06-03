import setup as st
import pygame
import projectile as pj
import levels as lv
import time 
class HealthBar:
    def __init__(self, x, y, width, height, max_hp):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.max_hp = max_hp
        self.current_hp = max_hp

        # Aizen-themed colors
        self.bg_color = (20, 20, 25)
        self.fill_color = (0, 210, 190)      # reiatsu cyan
        self.border_color = (190, 190, 255)

    def update(self, hp):
        self.current_hp = max(0, min(hp, self.max_hp))

    def draw(self, win):
        pygame.draw.rect(win, self.bg_color,
                         (self.x, self.y, self.width, self.height))

        ratio = self.current_hp / self.max_hp
        pygame.draw.rect(win, self.fill_color,
                         (self.x,self.y, int(self.width * ratio), self.height))

        pygame.draw.rect(win, self.border_color,
                         (self.x, self.y, self.width, self.height), 2)


class Aizen:
    def _frame_index(self, count, frames_per_img, frames):
        if not frames:
            return 0
        return min(count // frames_per_img, len(frames) - 1)

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hitbox = pygame.Rect(self.x+10, self.y-4, 10, st.AizenTitle.get_height()+20)
        self.hitbox_x=self.x+10
        self.max_health = 800
        self.health = 800
        self.dx = 0
        self.vel = 7
        self.walkCount = 0
        self.facing = 1
        self.idleCount = 0
        self.action = "idle"
        self.attackCount = 0
        self.hitCount = 0
        self.status = "alive"
        self.teleportCount = 0
        self.cero_queued=False
        self.attack_cooldown = 0
        self.cero_started = False
        self.attack_damage = 15
        self.health_bar = HealthBar(
            x=st.screen_width//2 - 200,
            y=st.AizenTitle.get_height()+20,
            width=400,
            height=14,
            max_hp=self.max_health
        )

    def draw(self, win,other):
        framesPerImg = 3
        if self.action == "idle":
            animation = st.AizenStanceLeft if self.facing == -1 else st.AizenStanceRight
            limit = len(animation) * framesPerImg
            sprite = animation[self._frame_index(self.idleCount, framesPerImg, animation)]
            self.hitbox = pygame.Rect(self.x-50, self.y, 25, 52)
            if self.idleCount + 1 >= limit:
                self.idleCount = 0
                self.action = "sec_idle"
            else:
                self.idleCount += 1
        elif self.action == "sec_idle":
            animation = st.AizenStanceMiddleLeft if self.facing == -1 else st.AizenStanceMiddleRight
            limit = len(animation) * framesPerImg
            sprite = animation[self._frame_index(self.idleCount, framesPerImg, animation)]
            if self.idleCount + 1 >= limit:
                self.idleCount = 0
                self.action = "third_idle"
            else:
                self.idleCount += 1
        elif self.action == "third_idle":
            animation = st.AizenStanceFinalLeft if self.facing == -1 else st.AizenStanceFinalRight
            limit = len(animation) * framesPerImg
            sprite = animation[self._frame_index(self.idleCount, framesPerImg, animation)]
            if self.idleCount + 1 >= limit:
                self.idleCount = 0
                self.action = "final_idle"
            else:
                self.idleCount += 1
        elif self.action == "cero":
            animation = st.AizenCeroRight if self.facing == 1 else st.AizenCeroLeft
            limit = len(animation) * framesPerImg
            if not self.cero_started:
                direction = 1 if self.facing == 1 else -1
                spawn_x = self.x + (90 if direction == 1 else -10)
                spawn_y = self.y - 20
                pj.projectiles.append(pj.Cero(spawn_x, spawn_y, 80, 80, direction))
                self.cero_started = True
            sprite = animation[self._frame_index(self.attackCount, framesPerImg, animation)]
            if self.attackCount + 1 >= limit:
                self.attackCount = 0
                self.cero_started = False
                self.action = "idle"
            else:
                self.attackCount += 1
        elif self.action == "attack":
            animation = st.AizenattackRight if self.facing == 1 else st.AizenattackLeft
            limit = len(animation) * framesPerImg
            sprite = animation[self._frame_index(self.attackCount, framesPerImg, animation)]
            if self.attackCount + 1 >= limit:
                self.attackCount = 0
                self.action = "jump_attack"
            else:
                self.attackCount += 1
        elif self.action == "jump_attack":
            animation = st.AizenJumpAttackRight if self.facing == 1 else st.AizenJumpAttackLeft
            limit = len(animation) * framesPerImg
            self.x += self.facing * 5
            if self.attackCount < limit // 2:
                self.y -= 10
            else:
                self.y += 10
            sprite = animation[self._frame_index(self.attackCount, framesPerImg, animation)]
            if self.attackCount + 1 >= limit:
                self.attackCount = 0
                self.y = 616
                self.action = "combo_attack"
            else:
                self.attackCount += 1
        elif self.action == "combo_attack":
            if other.x-self.x>0:
                self.facing==1
            animation = st.AizensecondAttackRight if self.facing == 1 else st.AizensecondAttackLeft
            limit = len(animation) * framesPerImg
            self.x += self.facing * 5
            if self.attackCount < limit // 2:
                self.y -= 10
            else:
                self.y += 10
            sprite = animation[self._frame_index(self.attackCount, framesPerImg, animation)]
            if self.attackCount + 1 >= limit:
                self.attackCount = 0
                self.action = "idle"
                self.y=616
            else:
                self.attackCount += 1
        elif self.action == "teleport":
            animation = st.AizenTeleportRight if self.facing == 1 else st.AizenTeleportLeft
            limit = len(animation) * framesPerImg
            sprite = animation[self._frame_index(self.teleportCount, framesPerImg, animation)]
            if self.teleportCount + 1 >= limit:
                self.teleportCount = 0
                self.action = "idle"
            else:
                self.teleportCount += 1
        elif self.action == "walk":
            animation = st.AizenRunRight if self.facing == 1 else st.AizenRunLeft
            limit = len(animation) * framesPerImg
            sprite = animation[self._frame_index(self.walkCount, framesPerImg, animation)]
            self.hitbox = pygame.Rect(self.x-60, self.y, 45, 30)
            if self.walkCount + 1 >= limit:
                self.walkCount = 0
            else:
                self.walkCount += 1
        elif self.action == "hit":
            animation = st.AizenHitRight if self.facing == 1 else st.AizenHitLeft
            limit = len(animation) * framesPerImg
            sprite = animation[self._frame_index(self.hitCount, framesPerImg, animation)]
            self.hitbox = pygame.Rect(self.x-50, self.y, 25, 52)
            if self.hitCount + 1 >= limit:
                self.hitCount = 0
            else:
                self.hitCount += 1
        else:
            animation = st.AizenFinalIdleLeft if self.facing == -1 else st.AizenFinalIdleRight
            limit = len(animation) * framesPerImg
            sprite = animation[self._frame_index(self.idleCount, framesPerImg, animation)]
            if self.idleCount + 1 >= limit:
                self.idleCount = 0
                self.action = "final_idle"
        draw_x = self.x - sprite.get_width() // 2 - 40
        draw_y = self.hitbox.bottom - sprite.get_height() + 5

        win.blit(st.AizenTitle,
                 (st.screen_width//2 - st.AizenTitle.get_width() + 50, 10))
        win.blit(sprite, (draw_x, draw_y))
        pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)
        self.health_bar.update(self.health)
        self.health_bar.draw(win)

    def move(self, other):
        if self.status != "alive":
            return
        # self.action="walk"
        # print(self.x)
        # if self.x>=st.screen_width-self.vel:
        #     self.facing=-1
        # elif self.x<=52+self.vel:
        #     self.facing=1
        # self.hitbox = pygame.Rect(self.x + 10, self.y, 25, 52)
        # if self.attack_cooldown > 0:
        #     self.attack_cooldown -= 1
        self.dx = other.x - self.x
        if abs(self.dx) > 40 and other.hit_state == "normal" and not self.action=="teleport":
            if self.action != "walk":
                self.interrupt()
                self.action = "walk"
            self.facing = 1 if self.dx > 0 else -1
        if self.action=="walk":
            self.x += self.facing * self.vel
            
        if self.action in ["walk"]:
            self.y = 635
        else:
            self.y = 616
        if pygame.time.get_ticks()-st.lastTeleport>=10 and abs(self.dx)>100:
            self.action="teleport"
            st.lastTeleport=pygame.time.get_ticks()
        if self.teleportCount>=36 and self.action=="teleport" and not self.cero_queued:
            self.x=other.x-10
        
        if pygame.time.get_ticks()-st.lastCero>=1000 and self.action not in ["cero", "teleport"]:
            self.cero_queued=True
            self.cero()
        if self.cero_queued and not self.cero_started:
            if self.teleportCount>=36:
                self.x=other.x-self.dx
            self.cero()
        # else:
        #     if self.action not in [
        #         "idle", "sec_idle", "third_idle", "final_idle",
        #         "attack", "jump_attack", "combo_attack",
        #         "cero", "teleport", "dash", "hit"
        #     ]:
        #         self.action = "idle"
        #         self.idleCount = 0
        # if self.hitbox.colliderect(other.hitbox) and self.attack_cooldown <= 0:
        #     self.interrupt()
        #     self.action = "attack"
        #     self.attack_cooldown = 30

        self.draw(st.win,other)

    def cero(self):
        if self.status != "alive":
            return
        if self.action not in ["cero"]:
            if abs(self.dx)<200 and not self.cero_started:
                self.action="teleport"
                self.cero_queued=True
                self.cero_started=False
            else:
                self.interrupt()
                self.action = "cero"
                st.lastCero = pygame.time.get_ticks()
                self.cero_queued=False
                self.cero_started=True

    def interrupt(self):
        self.attackCount = 0
        self.idleCount = 0
        self.walkCount = 0
        self.teleportCount = 0
        self.dashCount = 0
        self.cero_started = False
        self.y = 616

    def hit(self, amount=20):
        self.health -= amount
        self.health = max(0, self.health)
        self.health_bar.update(self.health)
        self.action = "hit"
        self.interrupt()