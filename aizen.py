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
        self.test= pygame.Rect(200,self.feet_y, 50,100)
        self.attackCount=0
        self.attacking=True
    
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
            limit= len(attackLeft)*framesPerimg
            if self.facing==1:
                sprite=attackRight[self.attackCount//framesPerimg]
            else:
                sprite= attackLeft[self.attackCount//framesPerimg]
            if self.attackCount+1>=limit:
                self.attacking=False
                self.attackCount=0
            self.attackCount+=1

        self.hitbox=pygame.Rect(self.x,self.feet_y,40,70)
        self.test= pygame.Rect(250,self.feet_y, 50,100)
        pygame.draw.rect(win,(255,0,0),self.test,2)
        pygame.draw.rect(win,(255,0,0),self.hitbox,2)
        win.blit(sprite,(self.x,self.feet_y))

    def move(self):
        if self.x- self.vel< self.end[0]:
            self.facing=1
        elif self.x+self.vel > self.end[1]:
            self.facing=-1
        self.x+=self.facing*self.vel
        # if time.time()-self.start>3:
        #     self.flashstep()
        #     self.walkCount=0
        #     self.dash=True
        #     self.start=time.time()
        self.draw(win)
    
    def attack(self):
        self.attacking=True
       
    def flashstep(self):
        self.x+=self.facing*100

aizen= Antagonist(30, 320,64,64)
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