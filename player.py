import pygame
import setup as st

class Player:
    def __init__(self, width, height, x, y):
        self.width = width
        self.height = height
        self.x = x
        self.feet_y = y  
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

    def draw(self, win):
        framesPerImg = 3
        limit=0
        sprite = st.jumpLeft[0]
    
        if not self.standing and not self.isJump and not self.attacking:
            self.stancephase=0
            if self.dashing: #dashing animation
                if self.facing==1:
                    limit= len(st.dashRight)*framesPerImg
                    sprite=st.dashRight[self.dashCount// framesPerImg]
                else:
                    limit = len(st.dashLeft) *framesPerImg
                    sprite = st.dashLeft[self.dashCount//framesPerImg]
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
                    limit = len(st.walkLeft) * framesPerImg
                    sprite = st.walkLeft[self.walkCount // framesPerImg]
                elif self.right:
                    limit = len(st.walkRight) * framesPerImg
                    sprite = st.walkRight[self.walkCount // framesPerImg]
                self.walkCount += 1
                if self.walkCount +1 >= limit:
                    self.walkCount = 0
            else: #Standing back up animation
                self.stationaryPhase= False
                if self.facing==1:
                    limit= len(st.standUpRight)* framesPerImg
                    sprite= st.standUpRight[self.downCount// framesPerImg]
                else:
                    limit= len(st.standUpLeft)* framesPerImg
                    sprite= st.standUpLeft[self.downCount// framesPerImg]
                if self.downCount+1 >=limit:
                    self.downCount=0
                    self.down= False
                self.downCount+=1

        elif self.stationaryPhase:  #continuously getting hit animation
            if self.facing==-1:
                limit= len(st.hitLeft)*framesPerImg
                sprite= st.hitLeft[self.stationaryPhaseCount// framesPerImg]
            else:
                limit= len(st.hitRight)*framesPerImg
                sprite= st.hitRight[self.stationaryPhaseCount// framesPerImg]
            if self.stationaryPhaseCount+1>= limit:
                self.stationaryPhaseCount=0
                self.down= True
            self.stationaryPhaseCount+=1
            
        elif self.gotHit: #falling and getting hit animation
            if self.facing==1:
                limit= len(st.getHitRight)*framesPerImg
                sprite= st.getHitRight[self.getHitCount//framesPerImg]
            else:
                limit= len(st.getHitLeft)*framesPerImg
                sprite= st.getHitLeft[self.getHitCount//framesPerImg]
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
                limit= len(st.attackRight)*framesPerImg
                if self.facing==1:
                    sprite= st.attackRight[self.attackCount// framesPerImg]
                else:
                    sprite= st.attackLeft[self.attackCount// framesPerImg]
                self.attackCount+=1
                if self.attackCount+1 >= limit:
                    self.attackCount=0
                    self.attacking=False
            else: #getsugatensho launch animation
                limit= len(st.getsugatenshoRight)*framesPerImg
                if self.facing==1:
                    sprite= st.getsugatenshoRight[self.signatureCount// framesPerImg]
                else:
                    limit= len(st.getsugatenshoLeft)*framesPerImg
                    sprite= st.getsugatenshoLeft[self.signatureCount// framesPerImg]
                self.signatureCount+=1
                if self.signatureCount+1>=limit:
                    self.signatureCount=0
                    self.attacking= False
        elif self.isJump: #jump animation
            if self.facing==1:
                limit = len(st.jumpRight)* framesPerImg
                sprite= st.jumpRight[self.spjumpCount//framesPerImg]
            else:
                limit = len(st.jumpLeft)* framesPerImg
                sprite= st.jumpLeft[self.spjumpCount//framesPerImg]
            if self.spjumpCount +1>= limit:
                self.spjumpCount=0
            self.spjumpCount += 1
        else:
            if self.stancephase==0: #stance during no input
                if self.facing==-1:
                    limit = len(st.stanceLeft) * framesPerImg
                    sprite = st.stanceLeft[self.stanceCount // framesPerImg]
                elif self.facing==1:
                    limit = len(st.stanceRight) * framesPerImg
                    sprite = st.stanceRight[self.stanceCount // framesPerImg]
                self.stanceCount += 1
                if self.stanceCount +1>= limit:
                    self.stanceCount=0
                    self.stancephase=1
            else: #continued stance when idle
                if self.facing==-1:
                    limit = len(st.stanceFinalLeft)* framesPerImg
                    sprite = st.stanceFinalLeft[self.stanceFinal // framesPerImg]
                else:
                    limit = len(st.stanceFinalRight)* framesPerImg
                    sprite = st.stanceFinalRight[self.stanceFinal // framesPerImg]
                self.stanceFinal+=1
                if self.stanceFinal+1>= limit:
                    self.stanceFinal=0
                    self.stanceCount=0

        self.hitbox= pygame.Rect(self.x+10, self.feet_y-4,50, 52 )
        if self.signature and self.facing==-1:
            draw_x= self.x -sprite.get_width()+50
        else:
            draw_x= self.x
        sprite_height = sprite.get_height()
        draw_y = self.feet_y - sprite_height+50
        win.blit(sprite, (draw_x, draw_y))

    def hit(self):
        if self.gotHit or self.stationaryPhase or self.down:
            return
        if not self.stationaryPhase:
            self.health-=1
            self.gotHit=True
            self.attacking= False
            self.stationaryPhase= False