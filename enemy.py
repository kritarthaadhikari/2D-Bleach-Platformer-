import pygame
import time
import setup as st

hollows = []

class Enemy:
    def __init__(self,width,height,x,y):
        self.x= x
        self.feet= y
        self.width= width
        self.height= height
        self.vel=2
        self.facing=-1 #direction of movement
        self.walkCount=0 #for walk animation
        self.end= [self.width-80, st.screen_width-230] #boundary
        self.attackCount=0 #attack animation
        self.lastattackTimer= time.time() #attack timer
        self.state="idle" #enemy state
        self.body_hitbox= pygame.Rect(self.x+10, self.feet-100,70, 125 )
        self.attack_hitbox= pygame.Rect(self.x+10, self.feet-100, 50, 60)
        self.hitCount=0
        self.health=500
        self.fallCount= 0
        self.blownCount=0
        self.blown=False
        self.static_x=x
    
    def draw(self,win,other):
        framesPerImg=4
        sprite = None
        
        if self.state=="idle" and not self.blown:
            if self.facing==-1:
                limit= len(st.HwalkLeft)* framesPerImg
                sprite= st.HwalkLeft[self.walkCount//framesPerImg]
            elif self.facing==1:
                limit= len(st.HwalkRight)*framesPerImg
                sprite= st.HwalkRight[self.walkCount//framesPerImg]
            self.walkCount+=1
            if self.walkCount+1>= limit:
                self.walkCount=0 
            if self.facing==1:
                self.body_hitbox= pygame.Rect(self.x+30, self.feet-100,68, 135 )
            elif self.facing==-1:
                self.body_hitbox= pygame.Rect(self.x+12, self.feet-100,68, 135 )
            
            pygame.draw.rect(win,(255,0,0),(self.body_hitbox[0], self.body_hitbox[1]-20,70,10))
            pygame.draw.rect(win,(0,255,0),(self.body_hitbox[0], self.body_hitbox[1]-20,70-7*(500-self.health)/50,10))
        
        elif self.state=="attacking":
            attackFramesPerImg = 3
            if self.facing==1:
                limit = len(st.HattackRight) * attackFramesPerImg
                sprite = st.HattackRight[self.attackCount // attackFramesPerImg]
            elif self.facing==-1:
                limit = len(st.HattackLeft) * attackFramesPerImg
                sprite = st.HattackLeft[self.attackCount // attackFramesPerImg]
            self.attackCount += 1
            if self.attackCount + 1 >= limit:
                self.attackCount = 0 
                if self.body_hitbox.colliderect(other.hitbox):
                    self.state = "hit"
                else:
                    self.state="idle"
            
            if self.facing==1:
                self.body_hitbox= pygame.Rect(self.x+10, self.feet-40,130, 60 )
                self.attack_hitbox= pygame.Rect(self.x+100, self.feet-30,50, 60)
            else:
                self.body_hitbox= pygame.Rect(self.x, self.feet-40,130, 60 )
                self.attack_hitbox= pygame.Rect(self.x, self.feet-30,50, 60)
            
            pygame.draw.rect(win,(255,0,0),(self.body_hitbox[0], self.body_hitbox[1]-20,70,10))
            pygame.draw.rect(win,(0,255,0),(self.body_hitbox[0], self.body_hitbox[1]-20,70-7*(500-self.health)/50,10))
        
        elif self.state=="hit":
            attackFramesPerImg = 3
            if self.facing==1:
                limit= len(st.attackSeenRight)* attackFramesPerImg
                sprite= st.attackSeenRight[self.hitCount//attackFramesPerImg]
            else:
                limit= len(st.attackSeenLeft)* attackFramesPerImg
                sprite= st.attackSeenLeft[self.hitCount//attackFramesPerImg]
            self.hitCount+=1
            if self.hitCount+1 >=limit:
                self.hitCount=0
            
            pygame.draw.rect(win,(255,0,0),(self.body_hitbox[0], self.body_hitbox[1]-20,70,10))
            pygame.draw.rect(win,(0,255,0),(self.body_hitbox[0], self.body_hitbox[1]-20,70-7*(500-self.health)/50,10))
        
        elif self.blown:
            if self.facing==1:
                limit= len(st.blownRight)*framesPerImg
                sprite= st.blownRight[self.blownCount// framesPerImg]
            elif self.facing==-1:
                limit= len(st.blownLeft)*framesPerImg
                sprite= st.blownLeft[self.blownCount// framesPerImg]
            if self.blownCount+1>= limit:
                self.blownCount=0
                self.state="idle"
                self.blown=False
            self.blownCount+=1
        
        elif self.state=="falling":
            if self.facing==1:
                limit= len(st.fallRight)*framesPerImg
                sprite= st.fallRight[self.fallCount// framesPerImg]
            elif self.facing==-1:
                limit= len(st.fallLeft)*framesPerImg
                sprite= st.fallLeft[self.fallCount// framesPerImg]
            if self.fallCount+1>= limit:
                self.fallCount=0
                self.state="dead"
            self.fallCount+=1
        
        elif self.state=="dead":
            if self.facing==1:
                sprite= st.fallRight[3]
            else:
                sprite= st.fallLeft[3]
            self.kill(other)
        if sprite:
            sprite_height= sprite.get_height()
            draw_y= self.feet- sprite_height+50
            win.blit(sprite , (self.x , draw_y))
    
    def move(self, win,other):
        if not self.blown:
        
            if self.state=="idle" and self.health>0:
                if self.x-other.x>20:
                    if self.facing==1:
                        self.facing=-1
                elif other.x-self.x>40:
                    if self.facing==-1:
                        self.facing=1
                self.x+= self.facing* self.vel
        else:
            self.x+= -self.facing*4
            if self.facing==1:
                self.body_hitbox= pygame.Rect(self.x+10, self.feet-40,130, 60 )
                self.attack_hitbox= pygame.Rect(self.x+100, self.feet-30,50, 60)
            else:
                self.body_hitbox= pygame.Rect(self.x, self.feet-40,130, 60 )
                self.attack_hitbox= pygame.Rect(self.x, self.feet-30,50, 60)
        
        if self.health<=0 and self.state!="falling" and self.state!="dead":
            self.state="falling"
        self.draw(win,other)
    
    def gothit(self,other):
        if not other.action=="visored":
            if self.state=="idle":
                self.state="attacking"
                self.attackCount=0
        else:
            self.state="idle"
            self.health-=20*other.incrementalFactor
        self.health-=5*other.incrementalFactor
        if other.ultimateGauge<160:
            st.previousGauge=other.ultimateGauge
            other.ultimateGauge+=1/2
            st.bankaiUltimateReady(other,st.previousGauge)
            other.ultimateGauge=min(other.ultimateGauge, 160)
    
    def kill(self,other):
        if self in hollows:
            hollows.remove(self)
            st.score+=10
            st.killCount+=1
            st.killCountperRound+=1
            if other.ultimateGauge<160:
                st.previousGauge=other.ultimateGauge
                other.ultimateGauge+=10
                st.bankaiUltimateReady(other,st.previousGauge)
                other.ultimateGauge=min(other.ultimateGauge, 160)