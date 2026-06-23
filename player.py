import pygame
import setup as st
import projectile as pr
class Player:
    def __init__(self, width, height, x, y):
        self.width = width
        self.height = height
        self.x = x
        self.feet_y = y  
        self.y_offset= 0
        self.vel = 5
        self.walkCount = 0 #movement
        self.stanceCount = 0 #stance init
        self.stanceFinal = 0 #stance continuation
        self.stance_state = "initial" # stance animation phase
        self.jumpCount = 11 #jump parameter
        self.spjumpCount = 0 #jump  count for animation
        self.facing = 1 #direction
        self.dashTimer = 10 #dash duration
        self.air_dash = False
        self.hitbox = pygame.Rect(self.x+10, self.feet_y-4,50, 52 )
        self.attackhitbox= pygame.Rect(self.x,self.feet_y,20,30)
        self.getHitCount = 0 #getting hit
        self.hitCount=0 #hit by aizen
        self.hit_state = "normal" # normal, got_hit, stationary
        self.stationaryPhaseCount = 0 #getting hit continuation
        self.downCount = 0 #knocked out 
        self.down_state = "normal" # normal or down
        self.health = 200
        self.signatureCount = 0
        self.steadyCount=0 #steadyhit
        self.staminaGauge = 100
        self.ultimateGauge = 160
        self.comboTimer=0 #Time allowed for followup attack window
        self.combo_state= "none" 
        self.mode= "shikai" #shikai or bankai mode
        self.action="idle" #current action state -idle, walking, jumping, dashing, attacking, hit, knockeddown, combo, signature
        self.incrementalFactor= 1 #bankai impact increase factor
        self.transform_state="inactive" #inactive, activating
        self.bankaiCount=0
        self.attackCount = 0 #attack
        self.dashCount = 0 #dash
        self.movement_state = "idle" #left, right, or idle
        self.hollowattack=[] 
        self.ceroHit=False
        self.damage=200
        self.jump=False
        self.fixed_x=self.x
        self.visoredCount=0
        self.animations= {
            "shikai":{
                "walkRight": st.walkRight,
                "walkLeft": st.walkLeft,
                "stanceRight": st.stanceRight,
                "stanceLeft": st.stanceLeft,
                "stanceFinalRight": st.stanceFinalRight,
                "stanceFinalLeft": st.stanceFinalLeft,
                "jumpRight": st.jumpRight,
                "jumpLeft": st.jumpLeft,
                "dashRight": st.dashRight,
                "dashLeft": st.dashLeft,
                "attackRight": st.attackRight,
                "attackLeft": st.attackLeft,
                "IdleHitRight": st.IdleHitRight,
                "IdleHitLeft": st.IdleHitLeft,
                "HitRight": st.HitRight,
                "HitLeft": st.HitLeft,
                "standUpRight": st.standUpRight,
                "standUpLeft": st.standUpLeft,
                "getsugatenshoRight": st.getsugatenshoRight,
                "getsugatenshoLeft": st.getsugatenshoLeft,
                "attackFollowUpRight": st.attackFollowUpRight,
                "attackFollowUpLeft": st.attackFollowUpLeft,
                "transformRight": st.shikaiTransformRight,
                "transformLeft": st.shikaiTransformLeft,
                "standUpAutoRight": st.standUpAutoRight,
                "standUpAutoLeft": st.standUpAutoLeft,
                "hitbyAizenRight": st.hitbyAizenRight,
                "hitbyAizenLeft" : st.hitbyAizenLeft,
                "steadyhitRight": st.hitSteadyRight,
                "steadyhitLeft": st.hitSteadyLeft
            },
            "bankai":{
                "walkRight": st.bankaiWalkRight,
                "walkLeft": st.bankaiWalkLeft,
                "stanceRight": st.bankaiStanceRight,
                "stanceLeft": st.bankaiStanceLeft,
                "stanceFinalRight": st.bankaiStanceRight,
                "stanceFinalLeft": st.bankaiStanceLeft,
                "jumpRight": st.bankaiJumpRight,
                "jumpLeft": st.bankaiJumpLeft,
                "dashRight": st.bankaiDashRight,
                "dashLeft": st.bankaiDashLeft,
                "HitRight": st.bankaiHitRight,
                "HitLeft": st.bankaiHitLeft,
                "attackRight": st.bankaiAttackRight,
                "attackLeft": st.bankaiAttackLeft,
                "IdleHitRight": st.bankaiIdleHitRight,
                "IdleHitLeft": st.bankaiIdleHitLeft,
                "standUpRight": st.bankaistandUpRight,
                "standUpLeft": st.bankaistandUpLeft,
                "getsugatenshoRight": st.bankaiGetsugatenshoRight,
                "getsugatenshoLeft": st.bankaiGetsugatenshoLeft,
                "attackFollowUpRight": st.bankaiFollowUpRight,
                "attackFollowUpLeft": st.bankaiFollowUpLeft,
                "transformRight": st.bankaiTransformRight,
                "transformLeft": st.bankaiTransformLeft ,
                "hitbyAizenRight": st.bankaihitbyAizenRight,
                "hitbyAizenLeft" : st.bankaihitbyAizenLeft,
                "steadyhitRight" :st.bankaihitsteadyRight,
                "steadyhitLeft" :st.bankaihitsteadyLeft
            }
        }

    def activateDeactivateBankai(self):
        if self.mode=="shikai":
            self.mode= "bankai"
            self.vel=7
            self.damage=500
            self.incrementalFactor=2
            self.transform_state="activating"
            self.ultimateGauge-=80
            st.bankaiSound.play(0)
        # elif self.mode=="bankai":
        #     self.mode= "visored"
        #     self.vel=11
        #     self.damage=750
        #     self.incrementalFactor=4
        #     self.transform_state="activating"
        #     self.ultimateGauge=0
        elif self.mode=="bankai":
            self.mode= "shikai"
            self.vel=5
            self.damage=200
            self.stanceCount=0
            self.stanceFinal=0
            self.incrementalFactor=1
            self.transform_state="activating"
        self.dashCount=0
        self.attackCount=0
        self.signatureCount=0
        self.jumpCount=11
        self.spjumpCount=0
        self.stanceCount=0
        self.stanceFinal=0
        self.action="idle"
        self.draw(st.win)
        
    def draw(self, win, scroll=0):
        framesPerImg = 3
        limit=0
        sprite = self.animations[self.mode]["stanceRight"][0]
        if self.transform_state == "activating":
            framesPerImg=4
            limit=len(self.animations[self.mode]["transformRight"])*framesPerImg
            if self.facing==1:
                sprite= self.animations[self.mode]["transformRight"][self.bankaiCount//framesPerImg]
            else:
                sprite= self.animations[self.mode]["transformLeft"][self.bankaiCount//framesPerImg]
            if self.mode=="bankai":
                if 16<=self.bankaiCount<=24:
                    st.win.blit(st.bankai, (self.x-self.facing*(70+scroll), self.feet_y- st.bankai.get_height()+50))
                if 24<=self.bankaiCount<=32:
                    st.win.blit(st.tl,(self.x-self.facing*(50 + scroll), self.feet_y- st.tl.get_height()+40))
                    st.win.blit(st.tr,(self.x+self.facing*(50 - scroll), self.feet_y-st.tr.get_height()+40))
                    # st.win.blit(st.br,(self.x+self.facing*70,self.feet_y+st.br.get_height()-60))
                    # st.win.blit(st.bl,(self.x-self.facing*70,self.feet_y+st.bl.get_height()-60))
                    # st.win.blit(st.br2, (self.x+self.facing*70,self.feet_y+st.br2.get_height()))
            
            if self.bankaiCount+1>= limit:
                self.bankaiCount=0
                self.transform_state="inactive"
                self.action="idle"
            self.bankaiCount+=1
        else:
            if self.action=="visored":
                framesPerImg=4
                limit=len(st.VisoredRight)*framesPerImg
                if self.facing==1:
                    sprite= st.VisoredRight[self.visoredCount//framesPerImg]
                else:
                    sprite=st.VisoredLeft[self.visoredCount//framesPerImg]
                self.health-=1/15
                if self.visoredCount==28:
                    self.x=self.fixed_x
                if self.visoredCount>=20 and self.visoredCount<28:
                    self.x+=self.facing*15
                    self.feet_y-=4
                elif self.visoredCount>=28 and self.visoredCount<36:
                    self.x+=self.facing*15
                    self.feet_y+=4
                elif self.visoredCount>=12 and self.visoredCount<20:
                    self.feet_y-=2
                else:
                    self.feet_y=st.feet_y_initial
                self.hitbox= pygame.Rect(self.x+10, self.feet_y-4,60, 52 )
                if self.visoredCount+1>=limit:
                    self.visoredCount=0
                    self.action="idle"
                else:
                    self.visoredCount+=1
            elif self.action in ["idle", "dashing","knockeddown"] and not self.jump: #idle and dash animation
                if self.stance_state=="stand": #Auto standing after hit
                    limit=len(self.animations[self.mode]["standUpAutoRight"])*framesPerImg
                    if self.facing==1:
                        sprite= self.animations[self.mode]["standUpAutoRight"][self.stanceCount//framesPerImg]
                    else:
                        sprite= self.animations[self.mode]["standUpAutoLeft"][self.stanceCount//framesPerImg]
                    if self.stanceCount+1>= limit:
                        self.stanceCount=0
                        self.stance_state="initial"
                    else:
                        self.stanceCount+=1
                elif self.stance_state=="initial": #stance during no input
                    limit = len(self.animations[self.mode]["stanceRight"]) * framesPerImg
                    if self.facing==-1:
                        sprite = self.animations[self.mode]["stanceLeft"][self.stanceCount // framesPerImg]
                    elif self.facing==1:
                        sprite = self.animations[self.mode]["stanceRight"][self.stanceCount // framesPerImg]
                    if self.stanceCount +1>= limit:
                        self.stanceCount=0
                        self.stance_state="final"
                    else:
                        self.stanceCount += 1
                elif self.stance_state=="final": #continued stance when idle
                    limit = len(self.animations[self.mode]["stanceFinalLeft"]) * framesPerImg
                    if self.facing==-1:
                        sprite = self.animations[self.mode]["stanceFinalLeft"][self.stanceFinal // framesPerImg]
                    else:
                        sprite = self.animations[self.mode]["stanceFinalRight"][self.stanceFinal // framesPerImg]
                    if self.stanceFinal+1>= limit:
                        self.stanceFinal=0
                        self.stanceCount=0
                    else:
                        self.stanceFinal+=1

                if self.action=="dashing": #dashing animation
                    limit= len(self.animations[self.mode]["dashRight"])*framesPerImg
                    if self.facing==1:
                        sprite = self.animations[self.mode]["dashRight"][self.dashCount//framesPerImg]
                    else:
                        sprite = self.animations[self.mode]["dashLeft"][self.dashCount//framesPerImg]
                    if self.dashCount +1>= limit:
                        self.dashCount = 0
                    self.dashTimer-=1
                    if self.dashTimer<=0:
                        self.action="idle"
                        self.stance_state="initial"
                        self.dashCount=0
                        self.dashTimer=10
                    else:
                        self.dashCount += 1
                elif self.action=="knockeddown": #Standing back up animation
                    self.hit_state= "normal"
                    limit= len(self.animations[self.mode]["standUpLeft"])* framesPerImg
                    if self.facing==1:
                        sprite= self.animations[self.mode]["standUpRight"][self.downCount// framesPerImg]
                    else: 
                        sprite= self.animations[self.mode]["standUpLeft"][self.downCount// framesPerImg]
                    if self.downCount+1 >=limit:
                        self.downCount=0
                        self.down_state= "normal"
                        self.action = "idle"
                        self.hit_state= "normal"
                    else:
                        self.downCount+=1
                else:
                    if self.movement_state == "left":
                        limit = len(self.animations[self.mode]["walkLeft"]) * framesPerImg
                        sprite = self.animations[self.mode]["walkLeft"][self.walkCount // framesPerImg]
                    elif self.movement_state == "right":
                        limit = len(self.animations[self.mode]["walkRight"]) * framesPerImg
                        sprite = self.animations[self.mode]["walkRight"][self.walkCount // framesPerImg]
                    if self.walkCount +1 >= limit:
                        self.walkCount = 0
                    else:
                        self.walkCount += 1
            elif (self.action in ["hitbyAizen" ,"hitbyCero"])and self.movement_state=="idle":
                framesPerImg=3
                frame = min(self.hitCount // framesPerImg,len(self.animations[self.mode]["hitbyAizenRight"]) - 1)
                limit=len(self.animations[self.mode]["hitbyAizenRight"])*framesPerImg
                if self.facing==1:
                    sprite= self.animations[self.mode]["hitbyAizenRight"][frame]
                elif self.facing==-1:
                    sprite= self.animations[self.mode]["hitbyAizenLeft"][frame]
                
                if self.hitCount+1>=limit:
                    if self.action=="hitbyCero":
                        self.action="idle"
                        self.ceroHit=False
                    self.hitCount=0
                else:
                    self.hitCount+=1
            elif self.jump: #jump animation
                if self.air_dash:
                    if self.facing==1:
                        limit = len(self.animations[self.mode]["dashRight"])*framesPerImg
                        sprite = self.animations[self.mode]["dashRight"][self.dashCount//framesPerImg]
                    else:
                        limit = len(self.animations[self.mode]["dashLeft"])*framesPerImg
                        sprite = self.animations[self.mode]["dashLeft"][self.dashCount//framesPerImg]
                    if self.dashCount + 1 >= limit:
                        self.dashCount = 0
                    self.dashTimer -= 1
                    if self.dashTimer <= 0:
                        self.air_dash = False
                        self.dashTimer = 10
                    else:
                        self.dashCount += 1
                else:
                    if self.facing==1:
                        limit = len(self.animations[self.mode]["jumpRight"])* framesPerImg
                        sprite= self.animations[self.mode]["jumpRight"][self.spjumpCount//framesPerImg]
                    else:
                        limit = len(self.animations[self.mode]["jumpLeft"])* framesPerImg
                        sprite= self.animations[self.mode]["jumpLeft"][self.spjumpCount//framesPerImg]
                    if self.spjumpCount +1>= limit:
                        self.spjumpCount=0
                    else:
                        self.spjumpCount += 1
            elif self.action=="hit" and self.movement_state=="idle":
                if self.hit_state=="stationary":  #continuously getting hit animation
                    if self.facing==-1:
                        limit= len(self.animations[self.mode]["IdleHitLeft"])*framesPerImg
                        sprite= self.animations[self.mode]["IdleHitLeft"][self.stationaryPhaseCount// framesPerImg]
                    else:
                        limit= len(self.animations[self.mode]["IdleHitRight"])*framesPerImg
                        sprite= self.animations[self.mode]["IdleHitRight"][self.stationaryPhaseCount// framesPerImg]
                    if self.stationaryPhaseCount+1>= limit:
                        self.stationaryPhaseCount=0
                        self.down_state= "down"
                    else:
                        self.stationaryPhaseCount+=1
                    
                elif self.hit_state=="got_hit": #falling and getting hit animation
                    if self.facing==1:
                        limit= len(self.animations[self.mode]["HitRight"])*framesPerImg
                        sprite= self.animations[self.mode]["HitRight"][self.getHitCount//framesPerImg]
                    else:
                        limit= len(self.animations[self.mode]["HitLeft"])*framesPerImg
                        sprite= self.animations[self.mode]["HitLeft"][self.getHitCount//framesPerImg]
                    if self.getHitCount+1>=limit:
                        self.getHitCount=0
                        self.hit_state= "stationary"
                        self.down_state= "down"
                        self.stationaryPhaseCount=0
                        self.action = "hit"
                    else:
                        self.getHitCount+=1

            elif self.action=="attacking" or self.action=="signature":
                if self.action=="signature": #getsugatensho launch animation
                    limit= len(self.animations[self.mode]["getsugatenshoRight"])*framesPerImg
                    if self.facing==1:
                        sprite= self.animations[self.mode]["getsugatenshoRight"][self.signatureCount// framesPerImg]
                    else:
                        sprite= self.animations[self.mode]["getsugatenshoLeft"][self.signatureCount// framesPerImg]
                    if 32>=self.signatureCount>=12:
                        st.win.blit(st.getsugatensho, (self.x-self.facing*(50 + scroll), self.feet_y- st.getsugatensho.get_height()+40))
                    if self.signatureCount+1>=limit:
                        self.signatureCount=0
                        self.action="idle"
                    else:
                        self.signatureCount+=1

                else: #normal attack animation
                    self.x += self.facing * 1
                    limit= len(self.animations[self.mode]["attackRight"])*framesPerImg
                    if self.facing==1:
                        sprite= self.animations[self.mode]["attackRight"][self.attackCount// framesPerImg]
                    else:
                        sprite= self.animations[self.mode]["attackLeft"][self.attackCount// framesPerImg]
                    self.attackhitbox=pygame.Rect(self.x+self.facing*40,self.feet_y,55,30)
                    if self.attackCount+1 >= limit:
                        self.attackCount=0
                        self.action="idle"
                        if self.combo_state == "queued":
                            self.combo_state = "none"
                            self.action="combo"
                            self.attackCount = 0
                    else:
                        self.attackCount+=1

            elif self.action=="combo":
                    self.x+= self.facing
                    self.y_offset-=1
                    limit= len(self.animations[self.mode]["attackFollowUpRight"])*framesPerImg
                    if self.facing==1:
                        sprite= self.animations[self.mode]["attackFollowUpRight"][self.attackCount//framesPerImg]
                    else:
                        sprite= self.animations[self.mode]["attackFollowUpLeft"][self.attackCount//framesPerImg]
                    
                    self.attackhitbox=pygame.Rect(self.x+self.facing*30,self.feet_y,45,30)
                    if self.attackCount+1 >=limit:
                        self.attackCount=0
                        self.comboTimer=0
                        self.y_offset=0
                        self.action="idle"
                    else:
                        self.attackCount+=1
            else:
                if self.movement_state == "left":
                    limit = len(self.animations[self.mode]["walkLeft"]) * framesPerImg
                    sprite = self.animations[self.mode]["walkLeft"][self.walkCount // framesPerImg]
                elif self.movement_state == "right":
                    limit = len(self.animations[self.mode]["walkRight"]) * framesPerImg
                    sprite = self.animations[self.mode]["walkRight"][self.walkCount // framesPerImg]
                self.walkCount += 1
                if self.walkCount +1 >= limit:
                    self.walkCount = 0

        self.hitbox= pygame.Rect(self.x+10, self.feet_y-4,35, 52 )
        draw_x = self.x
        if not self.mode == "bankai" or (((self.animations['bankai']['stanceRight'][0] and self.facing == 1) and (self.action not in ["attacking", "combo"]))
                                           or ((self.mode == "bankai" and (self.action in ["attacking", "combo"]) and self.facing == -1))):
            if (self.facing == -1) or (self.mode == "bankai"):
                draw_x = self.x-sprite.get_width() + 50
        sprite_height = sprite.get_height()
        draw_y = self.feet_y - sprite_height+self.y_offset+50
        win.blit(sprite, (draw_x-scroll , draw_y))

    def hit(self):
        self.health-=1
        if self.hit_state != "stationary":
            self.hit_state = "got_hit"
        self.interrupt()

    def interrupt(self):
        self.action="hit"
        self.attackCount = 0
        self.comboTimer=5
        self.comboIndex=0
        self.y_offset = 0
        pr.projectiles.clear()   # only reset animation, not physics
        self.signatureCount=0
        if not self.jump:
            st.getsugatenshoSound.stop()

    def aizen_hit(self):
        if not self.action=="hitbyCero":
            self.health-=3
            self.action="hitbyAizen"
        else:
            self.health-=100
            self.ceroHit=True
            self.movement_state="idle"
            self.x-=self.facing*20
    
    def visoredAttack(self):
        self.interrupt()
        self.action="visored"
        self.fixed_x=self.x
        self.draw(st.win)
        