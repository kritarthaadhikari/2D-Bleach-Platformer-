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
        self.stancephase = 0 #T/F for stance
        self.jumpCount = 11 #jump parameter
        self.spjumpCount = 0 #jump 
        self.isJump = False
        self.right = False
        self.left = False
        self.standing = True
        self.dashing = False
        self.dashCount = 0 #dash
        self.facing = 1 #direction
        self.dashTimer = 10 #dash duration
        self.attacking = False
        self.attackCount = 0 #attack
        self.hitbox = pygame.Rect(self.x+10, self.feet_y-4,50, 52 )
        self.gotHit = False #getting hit T/F
        self.getHitCount = 0 #getting hit
        self.stationaryPhase = False #getting hit continuation T/F
        self.stationaryPhaseCount = 0 #getting hit continuation
        self.down = False #knocked out check 
        self.downCount = 0 #knocked out 
        self.health = 120
        self.signature = False 
        self.signatureCount = 0
        self.staminaGauge = 100
        self.ultimateGauge = 0
        self.comboIndex=0 #for combo attacks
        self.comboTimer=5 #Time allowed for followup attack
        self.combo= False
        self.hollowattack=[]
        self.comboQueued= False
        self.state= "shikai"
        self.damage=200
        self.incrementalFactor= 1 #bankai impact increase factor
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
                "attackFollowUpLeft": st.attackFollowUpLeft   
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
                "attackFollowUpLeft": st.bankaiFollowUpLeft
            }
        }

    def activateBankai(self):
        self.state= "bankai"
        self.vel=7
        self.damage=500
        self.stanceCount=0
        self.stanceFinal=0
        self.incrementalFactor=3
        self.dashCount=0
        self.attackCount=0
        self.signatureCount=0
        
    def draw(self, win):
        framesPerImg = 3
        limit=0
        sprite = st.jumpLeft[0]

        if not self.standing and not self.isJump and not self.attacking and not self.combo:
            self.stancephase=0
            if self.dashing: #dashing animation
                if self.facing==1:
                    limit= len(self.animations[self.state]["dashRight"])*framesPerImg
                    sprite = self.animations[self.state]["dashRight"][self.dashCount//framesPerImg]
                else:
                    limit = len(self.animations[self.state]["dashLeft"]) *framesPerImg
                    sprite = self.animations[self.state]["dashLeft"][self.dashCount//framesPerImg]
                self.dashCount += 1
                if self.dashCount +1>= limit:
                    self.dashCount = 0
                self.dashTimer-=1
                if self.dashTimer<=0:
                    self.dashing= False
                    self.dashCount=0
                    self.dashTimer=10

            elif not self.down: #movement animation
                if self.left:
                    limit = len(self.animations[self.state]["walkLeft"]) * framesPerImg
                    sprite = self.animations[self.state]["walkLeft"][self.walkCount // framesPerImg]
                elif self.right:
                    limit = len(self.animations[self.state]["walkRight"]) * framesPerImg
                    sprite = self.animations[self.state]["walkRight"][self.walkCount // framesPerImg]
                self.walkCount += 1
                if self.walkCount +1 >= limit:
                    self.walkCount = 0
            else: #Standing back up animation
                self.stationaryPhase= False
                if self.facing==1:
                    limit= len(self.animations[self.state]["standUpRight"])* framesPerImg
                    sprite= self.animations[self.state]["standUpRight"][self.downCount// framesPerImg]
                else:
                    limit= len(self.animations[self.state]["standUpLeft"])* framesPerImg
                    sprite= self.animations[self.state]["standUpLeft"][self.downCount// framesPerImg]
                if self.downCount+1 >=limit:
                    self.downCount=0
                    self.down= False
                    if not self.gotHit:
                        self.stationaryPhase=False
                    
                self.downCount+=1
        elif self.isJump: #jump animation
            if self.facing==1:
                limit = len(self.animations[self.state]["jumpRight"])* framesPerImg
                sprite= self.animations[self.state]["jumpRight"][self.spjumpCount//framesPerImg]
            else:
                limit = len(self.animations[self.state]["jumpLeft"])* framesPerImg
                sprite= self.animations[self.state]["jumpLeft"][self.spjumpCount//framesPerImg]
            if self.spjumpCount +1>= limit:
                self.spjumpCount=0
            self.spjumpCount += 1
        elif self.stationaryPhase:  #continuously getting hit animation
            if self.facing==-1:
                limit= len(self.animations[self.state]["IdleHitLeft"])*framesPerImg
                sprite= self.animations[self.state]["IdleHitLeft"][self.stationaryPhaseCount// framesPerImg]
            else:
                limit= len(self.animations[self.state]["IdleHitRight"])*framesPerImg
                sprite= self.animations[self.state]["IdleHitRight"][self.stationaryPhaseCount// framesPerImg]
            if self.stationaryPhaseCount+1>= limit:
                self.stationaryPhaseCount=0
                self.down= True
            self.stationaryPhaseCount+=1
            
        elif self.gotHit: #falling and getting hit animation
            if self.facing==1:
                limit= len(self.animations[self.state]["HitRight"])*framesPerImg
                sprite= self.animations[self.state]["HitRight"][self.getHitCount//framesPerImg]
            else:
                limit= len(self.animations[self.state]["HitLeft"])*framesPerImg
                sprite= self.animations[self.state]["HitLeft"][self.getHitCount//framesPerImg]
            if self.getHitCount+1>=limit:
                self.getHitCount=0
                self.gotHit= False
                self.stationaryPhase= True
                self.down= True
                self.stationaryPhaseCount=0
            self.getHitCount+=1
        elif self.attacking:
            if not self.signature: #attack animation
                self.x+= self.facing//2
                limit= len(self.animations[self.state]["attackRight"])*framesPerImg
                if self.facing==1:
                    sprite= self.animations[self.state]["attackRight"][self.attackCount// framesPerImg]
                else:
                    sprite= self.animations[self.state]["attackLeft"][self.attackCount// framesPerImg]
                self.attackCount+=1

                if self.attackCount+1 >= limit:
                    self.attackCount=0
                    self.attacking=False
                    if self.comboQueued:
                        self.comboQueued = False
                        self.combo = True
                        self.attackCount = 0

            else: #getsugatensho launch animation
                limit= len(self.animations[self.state]["getsugatenshoRight"])*framesPerImg
                if self.facing==1:
                    sprite= self.animations[self.state]["getsugatenshoRight"][self.signatureCount// framesPerImg]
                else:
                    sprite= self.animations[self.state]["getsugatenshoLeft"][self.signatureCount// framesPerImg]
                self.signatureCount+=1
                if self.signatureCount+1>=limit:
                    self.signatureCount=0
                    self.attacking= False
        elif self.combo:
                self.x+= self.facing
                self.y_offset-=1
                limit= len(self.animations[self.state]["attackFollowUpRight"])*framesPerImg
                if self.facing==1:
                    sprite= self.animations[self.state]["attackFollowUpRight"][self.attackCount//framesPerImg]
                else:
                    sprite= self.animations[self.state]["attackFollowUpLeft"][self.attackCount//framesPerImg]
                self.attackCount+=1
                if self.attackCount+1 >=limit:
                    self.attackCount=0
                    self.comboIndex=0   
                    self.comboTimer=5
                    self.y_offset=0
                    self.attacking = False
                    self.combo=False
        
        else:
            if self.stancephase==0: #stance during no input
                if self.facing==-1:
                    limit = len(self.animations[self.state]["stanceLeft"]) * framesPerImg
                    sprite = self.animations[self.state]["stanceLeft"][self.stanceCount // framesPerImg]
                elif self.facing==1:
                    limit = len(self.animations[self.state]["stanceRight"]) * framesPerImg
                    sprite = self.animations[self.state]["stanceRight"][self.stanceCount // framesPerImg]
                if self.stanceCount +1>= limit:
                    self.stanceCount=0
                    self.stancephase=1
                self.stanceCount += 1
            else: #continued stance when idle
                if self.facing==-1:
                    limit = len(self.animations[self.state]["stanceFinalLeft"]) * framesPerImg
                    sprite = self.animations[self.state]["stanceFinalLeft"][self.stanceFinal // framesPerImg]
                else:
                    limit = len(self.animations[self.state]["stanceFinalRight"]) * framesPerImg
                    sprite = self.animations[self.state]["stanceFinalRight"][self.stanceFinal // framesPerImg]
                self.stanceFinal+=1
                if self.stanceFinal+1>= limit:
                    self.stanceFinal=0
                    self.stanceCount=0

        self.hitbox= pygame.Rect(self.x+10, self.feet_y-4,50, 52 )
        
        draw_x= self.x
        if not self.state=="bankai" or  ((self.animations['bankai']['stanceRight'][0] and self.facing==1)and (not self.attacking and not self.combo)
                                        or((self.state=="bankai" and (self.attacking or self.combo) and self.facing==-1))):
            if self.signature and self.facing==-1 or self.state=="bankai":
                draw_x= self.x -sprite.get_width()+50
        
        sprite_height = sprite.get_height()
        draw_y = self.feet_y - sprite_height+self.y_offset+50
        win.blit(sprite, (draw_x, draw_y))

    def hit(self):
        self.health-=1
        if not self.stationaryPhase:
            self.interrupt()
            self.gotHit=True
            self.stationaryPhase= False

    def interrupt(self):
        self.attacking = False
        self.attackCount = 0
        self.combo=False
        self.comboQueued=False
        self.comboTimer=5
        self.comboIndex=0
        self.y_offset = 0
        pr.projectiles.clear()   # only reset animation, not physics
        self.signature= False
        self.signatureCount=0