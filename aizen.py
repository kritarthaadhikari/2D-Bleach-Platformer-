import pygame
import time
pygame.init()

screen_width= 1200
screen_height= 500
win=pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('Aizen')
#Aizen ASSETS
walk=  [pygame.image.load(f'images\enemy\Aizen\walk{i}.png').convert_alpha() for i in range(1,9)]
walkRight= [pygame.transform.smoothscale(img,(40,80) )for img in walk]
walkLeft= [pygame.transform.flip(img, True, False) for img in walkRight]
teleportRight= [pygame.image.load(f'images\enemy\Aizen\Teleport.png')]
teleportLeft= [pygame.transform.flip(img, True, False) for img in teleportRight]

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
    
    def draw(self,win):
        framesPerimg=3
        if not self.dash:
            limit= len(walkRight)*framesPerimg
            if self.facing==1:
                sprite= walkRight[self.walkCount//framesPerimg]
            else:
                sprite= walkLeft[self.walkCount//framesPerimg]
            if self.walkCount+1>=limit:
                self.walkCount=0
            self.walkCount+=1
           
        else:
            if self.facing==1:
                sprite=teleportRight[self.walkCount//framesPerimg]
            else:
                sprite=teleportLeft[self.walkCount//framesPerimg]
            if self.walkCount+1>=3:
                self.walkCount=0
                self.dash=False
            self.walkCount+=1
        win.blit(sprite,(self.x,self.feet_y))

    def move(self):
        if self.x- self.vel< self.end[0]:
            self.facing=1
        elif self.x+self.vel > self.end[1]:
            self.facing=-1
        self.x+=self.facing*self.vel
        if time.time()-self.start>3:
            self.flashstep()
            self.walkCount=0
            self.dash=True
            self.start=time.time()
        self.draw(win)
     
    def flashstep(self):
        self.x+=self.facing*100

aizen= Antagonist(30, 320,64,64)
clock= pygame.time.Clock()
def main():
    run=True
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type== pygame.QUIT:
                run=False
        win.fill((50, 50, 50))
        aizen.move()
        pygame.display.update()
    pygame.quit()
main()