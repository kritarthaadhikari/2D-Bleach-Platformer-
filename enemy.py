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
        self.attacking= False 
        self.body_hitbox= pygame.Rect(self.x+10, self.feet-100,70, 125 )
        self.attack_hitbox= pygame.Rect(self.x+10, self.feet-100, 50, 60)
        self.hit= False 
        self.hitCount=0
        self.health=500
        self.fallCount= 0
        self.fall= False #detects ground fall
    
    def draw(self,win):
        framesPerImg=4
        current= time.time()
        if not self.fall:
            if current- self.lastattackTimer > 3.0 or self.attacking:
                self.attacking= True
                if not self.hit:
                    if self.facing==1:
                        limit= len(st.HattackRight)*framesPerImg
                        sprite= st.HattackRight[self.attackCount//framesPerImg]
                    elif self.facing==-1:
                        limit= len(st.HattackLeft)*framesPerImg
                        sprite= st.HattackLeft[self.attackCount//framesPerImg]
                    self.attackCount+=1
                    if self.attackCount+1>=limit:
                        self.attackCount=0 
                        self.attacking= False
                        self.lastattackTimer= time.time()
            else:       
                if self.facing==-1:
                    limit= len(st.HwalkLeft)* framesPerImg
                    sprite= st.HwalkLeft[self.walkCount//framesPerImg]
                elif self.facing==1:
                    limit= len(st.HwalkRight)*framesPerImg
                    sprite= st.HwalkRight[self.walkCount//framesPerImg]
                self.walkCount+=1
                if self.walkCount+1>= limit:
                    self.walkCount=0

            if not self.attacking:
                if self.facing==1:
                    self.body_hitbox= pygame.Rect(self.x+30, self.feet-100,68, 135 )
                elif self.facing==-1:
                    self.body_hitbox= pygame.Rect(self.x+12, self.feet-100,68, 135 )
            else:
                if self.facing==1:
                    self.body_hitbox= pygame.Rect(self.x+10, self.feet-40,130, 60 )
                    self.attack_hitbox= pygame.Rect(self.x+100, self.feet-30,50, 60)
                else:
                    self.body_hitbox= pygame.Rect(self.x, self.feet-40,130, 60 )
                    self.attack_hitbox= pygame.Rect(self.x, self.feet-30,50, 60)

            if self.hit:
                if self.facing==1:
                    limit= len(st.attackSeenRight)* framesPerImg
                    sprite= st.attackSeenRight[self.hitCount//framesPerImg]
                else:
                    limit= len(st.attackSeenLeft)* framesPerImg
                    sprite= st.attackSeenLeft[self.hitCount//framesPerImg]
                self.hitCount+=1
                if self.hitCount+1 >=limit:
                    self.hitCount=0
            
            pygame.draw.rect(win,(255,0,0),(self.body_hitbox[0], self.body_hitbox[1]-20,70,10))
            pygame.draw.rect(win,(0,255,0),(self.body_hitbox[0], self.body_hitbox[1]-20,70-7*(500-self.health)/50,10))
                
        if self.health<=0 and not self.fall:
                if self.facing==1:
                    limit= len(st.fallRight)*framesPerImg
                    sprite= st.fallRight[self.fallCount// framesPerImg]
                elif self.facing==-1:
                    limit= len(st.fallLeft)*framesPerImg
                    sprite= st.fallLeft[self.fallCount// framesPerImg]
                if self.fallCount+1>= limit:
                    self.fallCount=0
                    self.fall= True
                self.fallCount+=1
        elif self.fall:
                if self.facing==1:
                    sprite= st.fallRight[3]
                else:
                    sprite= st.fallLeft[3]
                self.kill()

        # pygame.draw.rect(win, (255,0,0), self.body_hitbox,2)
        sprite_height= sprite.get_height()
        draw_y= self.feet- sprite_height+50
        win.blit(sprite , (self.x, draw_y))
    
    def move(self, win):
        if not self.attacking and not self.health<=0:
            if self.x==self.end[1]:
                self.facing=-1
            elif self.x==self.end[0]:
                self.facing=1
            self.x+= self.facing* self.vel
        self.draw(win)
    
    def gothit(self):
        self.health-=20
        self.x= self.x
    
    def kill(self):
        if self in hollows:
            hollows.remove(self)
            st.score+=10
            st.killCount+=1