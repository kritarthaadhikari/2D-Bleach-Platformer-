import pygame
import time
pygame.init()

screen_width= 1200
screen_height= 500
win=pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('Aizen')
#Aizen ASSETS
walk=  [pygame.image.load(f'images\enemy\Aizen\walk{i}.png').convert_alpha() for i in range(1,9)]
walkRight= [pygame.transform.smoothscale(img,(img.get_width(),90) )for img in walk]
walkLeft= [pygame.transform.flip(img, True, False) for img in walkRight]
teleportRight= [pygame.image.load(f'images\enemy\Aizen\Teleport.png')]
teleportLeft= [pygame.transform.flip(img, True, False) for img in teleportRight]
attack= [pygame.image.load(f'images/enemy/Aizen/attack{i}.png') for i in range(1,7)]
attackRight= [pygame.transform.smoothscale(img,(img.get_width(),90)) for img in attack]
attackLeft= [pygame.transform.flip(img, True, False) for img in attackRight]
airattack =[pygame.image.load(f'images/enemy/Aizen/airattack{i}.png') for i in range(1,6)]
airattackRight= [pygame.transform.smoothscale(img,(img.get_width(),90) ) for img in airattack]
airattackLeft= [pygame.transform.flip(img,True, False) for img in airattackRight]

class Antagonist:
    def __init__(self,x,y,width,height):
        self.x=  x
        self.feet_y= y
        self.width= width
        self.height= height 
        self.vel= 3
        self.walkCount=0
        self.walk= True 
        self.facing=1
        self.end= [self.width-50, screen_width-100]
        self.start=time.time()
        self.dash=False
        self.hitbox=pygame.Rect(self.x,self.feet_y,30,70)
        self.attackhitbox=pygame.Rect(self.x+20,self.feet_y-self.height//2,30,30)
        self.test= pygame.Rect(200,self.feet_y, 50,100)
        self.attackCount=0
        self.attacking=True
        self.attack_state=1 #type of attack
        self.jump= False
        self.jumpCount=5
        
    
    def draw(self,win):
        framesPerimg=3
        if not self.dash and not self.attacking:
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
                    self.attack_state=1
                    self.jump=False
                self.attackCount+=1

        self.hitbox=pygame.Rect(self.x+self.facing*5,self.feet_y,40,70)
        self.test= pygame.Rect(250,self.feet_y, 50,100)
        if self.facing==1:
            self.attackhitbox=pygame.Rect(self.x+50,self.feet_y,75,60)
        else:
            self.attackhitbox= pygame.Rect(self.x-sprite.get_width()-30, self.feet_y,75,60)
        pygame.draw.rect(win,(0,255,0),self.attackhitbox,2)
        pygame.draw.rect(win,(255,0,0),self.test,2)
        pygame.draw.rect(win,(255,0,0),self.hitbox,2)
        win.blit(sprite,(self.x,self.feet_y))

    def move(self):
        if self.x- self.vel< self.end[0]:
            self.facing=1
        elif self.x+self.vel > self.end[1]:
            self.facing=-1
        if not self.attacking and not self.jump:
            self.x+=self.facing*self.vel

            # if time.time()-self.start>3:
            #     self.flashstep()
            #     self.walkCount=0
            #     self.dash=True
            #     self.start=time.time()
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
                self.feet_y=320
        self.draw(win)
    
    def attack(self):
        self.attacking=True
       
    def flashstep(self):
        self.x+=self.facing*100

aizen= Antagonist(1000, 320,64,64)
clock= pygame.time.Clock()
def main():
    run=True
    while run:
        clock.tick(20)
        for event in pygame.event.get():
            if event.type== pygame.QUIT:
                run=False
        win.fill((50, 50, 50))
        aizen.move()
        if aizen.test.colliderect(aizen.hitbox):
            aizen.attack()
        else:
            aizen.attacking=False
        pygame.display.update()
    pygame.quit()
main()