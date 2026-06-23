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
        self.max_health = 20
        self.health = 20
        self.dx = 0
        self.vel = 6
        self.walkCount = 0
        self.facing = 1
        self.idleCount = 0
        self.action = "idle"
        self.attackCount = 0
        self.hitCount = 0
        self.status = "alive"
        self.gothit=False
        self.teleportCount = 0
        self.cero_queued=False
        self.cero_projectile = None
        self.attack_cooldown = 0
        self.cero_started = False
        self.attack_damage = 15
        self.attack_facing = None
        self.health_bar = HealthBar(
            x=st.screen_width//2 - 200,
            y=st.AizenTitle.get_height()+20,
            width=400,
            height=14,
            max_hp=self.max_health
        )

    def draw(self, win,other):
        framesPerImg = 3
        if self.status=="dead":
            return
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
        elif self.action == "final_idle":
            animation = st.AizenFinalIdleLeft if self.facing == -1 else st.AizenFinalIdleRight
            limit = len(animation) * framesPerImg
            sprite = animation[self._frame_index(self.idleCount, framesPerImg, animation)]
            if self.idleCount + 1 >= limit:
                self.idleCount = 0
            else:
                self.idleCount += 1
        elif self.action=="hold_after_cero":
            if self.facing==1:
                animation = st.AizenHoldAfterCeroRight
            else:
                animation = st.AizenHoldAfterCeroLeft
            sprite = animation[0]
            self.idleCount += 1
            if self.idleCount >= 30:  # Hold for 30 frames then return to idle
                self.idleCount = 0
                self.action = "idle"
        elif self.action == "cero":
            animation = st.AizenCeroRight if self.facing == 1 else st.AizenCeroLeft
            limit = len(animation) * 5
            if not self.cero_queued:
                direction = 1 if self.facing == 1 else -1
                spawn_x = self.x + (90 if direction == 1 else -100)
                spawn_y = self.y - 20
                self.cero_projectile = pj.Cero(spawn_x, spawn_y, 80, 80, direction)
                pj.cero.append(self.cero_projectile)
                self.cero_queued = True
            sprite = animation[self._frame_index(self.attackCount, 5, animation)]
            if self.attackCount + 1 >= limit:
                self.attackCount = 0
                self.cero_queued = False
                if self.cero_projectile is not None:
                    self.cero_projectile.active = True
                self.cero_started = True
                self.action = "hold_after_cero"
            else:
                self.attackCount += 1
        elif self.action == "attack":
            self.facing = self.attack_facing if self.attack_facing is not None else self.facing
            animation = st.AizenattackRight if self.facing == 1 else st.AizenattackLeft
            limit = len(animation) * framesPerImg
            sprite = animation[self._frame_index(self.attackCount, framesPerImg, animation)]
            if self.attackCount + 1 >= limit:
                self.attackCount = 0
                self.action = "jump_attack"
            else:
                self.attackCount += 1
        elif self.action == "jump_attack":
            self.facing = self.attack_facing if self.attack_facing is not None else self.facing
            animation = st.AizenJumpAttackRight if self.facing == 1 else st.AizenJumpAttackLeft
            limit = len(animation) * framesPerImg
            self.x += self.facing * 1
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
            self.facing = self.attack_facing if self.attack_facing is not None else self.facing
            animation = st.AizensecondAttackRight if self.facing == 1 else st.AizensecondAttackLeft
            limit = len(animation) * framesPerImg
            self.x += self.facing * 1
            if self.attackCount < limit // 2:
                self.y -= 10
            else:
                self.y += 10
            sprite = animation[self._frame_index(self.attackCount, framesPerImg, animation)]
            if self.attackCount + 1 >= limit:
                self.attackCount = 0
                self.action = "idle"
                self.y=616
                self.attack_facing = None
            else:
                self.attackCount += 1
        elif self.action == "teleport":
            animation = st.AizenTeleportRight if self.facing == 1 else st.AizenTeleportLeft
            limit = len(animation) * framesPerImg
            sprite = animation[self._frame_index(self.teleportCount, framesPerImg, animation)]
            self.hitbox = pygame.Rect(self.x-50, self.y, 25, 52)
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
            else:
                self.idleCount += 1
        draw_x = self.x - sprite.get_width() // 2 - 40
        draw_y = self.hitbox.bottom - sprite.get_height() + 5

        win.blit(st.AizenTitle,
                 (st.screen_width//2 - st.AizenTitle.get_width() + 50, 10))
        win.blit(sprite, (draw_x, draw_y))
        self.health_bar.update(self.health)
        self.health_bar.draw(win)

    def move(self, other):
        if self.status != "alive":
            return
        if other.transform_state!="activating":
            attack_chain = self.action in ["attack", "jump_attack", "combo_attack"]
            if attack_chain and self.attack_facing is not None:
                self.facing = self.attack_facing
            if self.x>=st.screen_width-self.vel:
                self.facing=-1
            elif self.x<=52+self.vel:
                self.facing=1
            self.dx = other.x - self.x
            # Hysteresis deadzone: only change facing when other is clearly left or right
            if not attack_chain and self.dx > 20:
                self.facing = 1
            elif not attack_chain and self.dx < -40:
                self.facing = -1          
            if other.hit_state=="normal":
                if 250>abs(self.dx) and not self.hitbox.colliderect(other.hitbox) and not self.gothit:
                    if self.action!= "walk":
                        self.interrupt()
                        self.action = "walk"
                elif abs(self.dx)>=250 or self.gothit:
                    if self.action!="teleport" and pygame.time.get_ticks() - st.lastCero >= 5000 and not self.gothit:
                        self.interrupt()
                        self.action ="cero"
                        st.lastCero = pygame.time.get_ticks()
                    elif (pygame.time.get_ticks() - st.lastTeleport >= 1000 ) and self.action not in ["teleport","cero","hold_after_cero"]:
                        self.interrupt()
                        self.action = "teleport"
                        st.lastTeleport = pygame.time.get_ticks()
                elif self.hitbox.colliderect(other.hitbox) and not self.gothit and self.action not in ["attack","jump_attack","combo_attack"]:
                    self.action = "attack"
                    self.attack_facing = self.facing
                    self.attack_cooldown = 30
                elif self.action not in ["idle", "sec_idle", "third_idle", "final_idle"
                                        ,"attack","jump_attack","combo_attack","cero","teleport","hit"]:
                    self.action = "idle"
            elif self.hitbox.colliderect(other.hitbox) and self.action!="hit" and self.action not in ["attack","jump_attack","combo_attack"]:
                    self.action = "attack"
                    self.attack_facing = self.facing
            else:
                self.action = "idle"
        
            if self.action=="walk":
                self.x += self.facing * self.vel
                self.y=635
            elif self.action == "teleport":
                self.y=616
                if self.teleportCount==36:  # Adjust timing as needed
                    if not self.gothit:
                        self.x= other.x +10 if self.facing==-1 else other.x+40
                    else:
                        self.x=1000 if st.screen_width//2- other.x>0 else 100
                        self.gothit=False
            else:
                self.y=616
                self.gothit=False

            if self.action == "walk":
                self.hitbox = pygame.Rect(self.x-60, self.y, 45, 30)
            elif self.action in ["idle", "sec_idle", "third_idle", "final_idle", "hold_after_cero", "cero", "attack", "jump_attack", "combo_attack", "teleport", "hit"]:
                self.hitbox = pygame.Rect(self.x-50, self.y, 25, 52)
            else:
                if self.action not in [
                    "idle", "sec_idle", "third_idle", "final_idle",
                    "attack", "jump_attack", "combo_attack",
                    "cero", "teleport", "dash", "hit"
                ]:
                    self.action = "idle"
                    self.idleCount = 0
        else:
            self.action="idle"
            self.y=616
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
        self.teleportCount=0
        self.walkCount = 0
        self.dashCount = 0
        self.attack_facing = None
        if self.cero_projectile is not None and not self.cero_projectile.active:
            self.cero_projectile.kill()
        self.cero_projectile = None
        self.cero_started = False
        self.y = 616

    def hit(self, amount=10):
        self.health -= amount
        self.health = max(0, self.health)
        self.health_bar.update(self.health)
        self.gothit=True
        if self.action not in ["cero","teleport"]:
            self.action = "hit"
            self.interrupt()
