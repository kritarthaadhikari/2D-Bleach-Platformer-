import pygame
import time
import setup as st
# pygame.init()

#Aizen ASSETS
walk=  [pygame.image.load(f'images\enemy\Aizen\walk{i}.png').convert_alpha() for i in range(1,9)]
walkRight= [pygame.transform.smoothscale(img,(img.get_width(),90) )for img in walk]
walkLeft= [pygame.transform.flip(img, True, False) for img in walkRight]
teleportRight= [pygame.image.load(f'images\enemy\Aizen\Teleport.png')]
teleportLeft= [pygame.transform.flip(img, True, False) for img in teleportRight]
attack= [pygame.image.load(f'images/enemy/Aizen/attack{i}.png') for i in range(1,6)]
attackRight= [pygame.transform.smoothscale(img,(img.get_width(),90)) for img in attack]
attackLeft= [pygame.transform.flip(img, True, False) for img in attackRight]
airattack =[pygame.image.load(f'images/enemy/Aizen/airattack{i}.png') for i in range(1,6)]
airattackRight= [pygame.transform.smoothscale(img,(img.get_width(),90) ) for img in airattack]
airattackLeft= [pygame.transform.flip(img,True, False) for img in airattackRight]
strongAttack= [pygame.image.load(f'images/enemy/Aizen/strongattack{i}.png') for i in range(1,8)]
strongAttackRight = [pygame.transform.smoothscale(img, (img.get_width(),90) )for img in strongAttack]
strongAttackLeft= [pygame.transform.flip(img, True, False) for img in strongAttackRight]
stance= [pygame.image.load(f'images/enemy/Aizen/taunt{i}.png') for i in range(1,6)]
stanceRight= [pygame.transform.smoothscale(img,(img.get_width(),90))for img in stance]
stanceLeft= [pygame.transform.flip(img, True, False) for img in stanceRight]
damage= [pygame.image.load(f'images/enemy/Aizen/damage{i}.png') for i in range(1,5)]
damageRight= [pygame.transform.smoothscale(img,(img.get_width(),90) ) for img in damage]
damageLeft= [pygame.transform.flip(img, True, False) for img in damageRight]

class Antagonist:
    def __init__(self,x,y,width,height):
        self.x=  x
        self.feet_y= y
        self.width= width
        self.height= height 
        self.vel= 2
        self.walkCount=0
        self.walk= False 
        self.facing=1
        self.end= [self.width-50, st.screen_width-100]
        self.start=time.time()
        self.dash=False
        self.hitbox=pygame.Rect(self.x,self.feet_y,30,70)
        self.attackhitbox=pygame.Rect(self.x+20,self.feet_y-self.height//2,30,30)
        self.attackCount=0
        self.attacking=True
        self.attack_state=1 #type of attack
        self.jump= False
        self.jumpCount=5
        self.stationary=False
        self.stationaryCount=0
        self.gotHit= False
        self.gotHitcount=0
        self.health =500
        
    def draw(self,win):
        framesPerimg=4
        if not self.dash and not self.attacking and not self.stationary and not self.gotHit:
            limit= len(walkRight)*framesPerimg
            if self.facing==1:
                sprite= walkRight[self.walkCount//framesPerimg]
            else:
                sprite= walkLeft[self.walkCount//framesPerimg]
            if self.walkCount+1>=limit:
                self.walkCount=0
            self.walkCount+=1
        elif self.dash:
            if self.facing==1:
                sprite=teleportRight[self.walkCount//framesPerimg]
            else:
                sprite=teleportLeft[self.walkCount//framesPerimg]
            if self.walkCount+1>=3:
                self.walkCount=0
                self.dash=False
            self.walkCount+=1
        elif self.gotHit:
            limit= len(damageLeft)*framesPerimg
            if self.facing==1:
                sprite= damageRight[self.gotHitcount//framesPerimg]
            else:
                sprite= damageLeft[self.gotHitcount//framesPerimg]
            if self.gotHitcount+1>=limit:
                self.gotHitcount=0
            self.gotHitcount+=1
        elif self.stationary:
            limit=len(stance*framesPerimg)
            if self.facing==1:
                sprite= stanceRight[self.stationaryCount//framesPerimg]
            else:
                sprite=stanceLeft[self.stationaryCount//framesPerimg]
            if self.stationaryCount+1>=limit:
                self.stationary=False
                self.stationaryCount=0
            self.stationaryCount+=1
            
        elif self.attacking:
            if self.attack_state==1:
                limit= len(attackLeft)*framesPerimg
                if self.facing==1:
                    sprite=attackRight[self.attackCount//framesPerimg]
                else:
                    sprite= attackLeft[self.attackCount//framesPerimg]
                if self.attackCount+1>=limit:
                    self.attacking=False
                    self.attackCount=0
                    self.attack_state+=1
                self.attackCount+=1 
            elif self.attack_state==2:
                self.jump=True
                limit= len(airattackRight)*framesPerimg
                if self.facing==1:
                    sprite= airattackRight[self.attackCount//framesPerimg]
                else:
                    sprite= airattackLeft[self.attackCount//framesPerimg]
                if self.attackCount+1>=limit:
                    self.attacking=False
                    self.attackCount=0
                    self.attack_state+=1
                    self.jump=False
                self.attackCount+=1
            elif self.attack_state==3:
                limit= len(strongAttack)*framesPerimg
                if self.facing==1:
                    sprite= strongAttackRight[self.attackCount//framesPerimg]
                else:
                    sprite= strongAttackLeft[self.attackCount//framesPerimg]
                if self.attackCount+1>=limit:
                    self.attacking=False
                    self.attackCount=0
                    self.attack_state=1
                self.attackCount+=1
        else:
            if self.facing==-1:
                sprite=stanceLeft
            else:
                sprite=stanceRight
            self.stationary=False
            

        self.hitbox=pygame.Rect(self.x+self.facing*5,self.feet_y,40,70)
        # self.test= pygame.Rect(250,self.feet_y, 50,100)
        if self.attacking:
            if self.facing==1:
                self.attackhitbox=pygame.Rect(self.x+30,self.feet_y,75,60)
            else:
                self.attackhitbox= pygame.Rect(self.x-30, self.feet_y,75,60)
        # pygame.draw.rect(st.win,(0,255,0),self.attackhitbox,2)
        # pygame.draw.rect(win,(255,0,0),self.test,2)
        # pygame.draw.rect(st.win,(255,0,0),self.hitbox,2)
        pygame.draw.rect(st.win, (255,0,0),(self.hitbox[0],self.hitbox[1]-30, 70,10))
        pygame.draw.rect(st.win, (0,255,0),(self.hitbox[0],self.hitbox[1]-30, 70-(500-self.health)*7/50,10))
        st.win.blit(sprite,(self.x,self.feet_y))

    def move(self,other):
        if not self.stationary and not other.down:
            if self.x- other.x-100>0:
                self.facing=-1
            elif self.x-other.x+100<0:
                self.facing=1
            if not self.attacking and not self.jump:
                self.x+=self.facing*self.vel
                if time.time()-self.start>3 and not self.attacking:
                    self.flashstep()
                    self.walkCount=0
                    self.dash=True
                    self.start=time.time()
            if self.jump:
                if self.jumpCount>=-5:
                    neg=1
                    if self.jumpCount<0: neg=-1
                    self.x+=self.facing*15
                    self.feet_y-=(self.jumpCount**2)*neg*0.5
                    self.jumpCount-=1
                else:
                    self.jumpCount=5
                    neg=1
                    self.attack_state=1
                    self.jump=False
                    self.feet_y=470
        else:
            self.stationary=True
        self.draw(st.win)
       
    def flashstep(self):
        self.x+=self.facing*100
    
    def working(self):
        pass
