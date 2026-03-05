import pygame
pygame.init()

screen_width= 1200
screen_height= 500
win=pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('Ulquiorra')
#ULQUIORRA ASSETS
walkRight= [pygame.image.load(f'images\enemy\ulquiorra\walk{i}.png') for i in range(1,8)]
walkLeft= [pygame.transform.flip(img, True, False) for img in walkRight]

class Espada:
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
    
    def draw(self,win):
        framesPerimg=3
        limit= len(walkRight)*framesPerimg
        if self.facing==1:
            sprite= walkRight[self.walkCount//framesPerimg]
        else:
            sprite= walkLeft[self.walkCount//framesPerimg]
        if self.walkCount+1>=limit:
            self.walkCount=0
        self.walkCount+=1
        win.blit(sprite,(self.x,self.feet_y))
    
    def move(self,win):
        if self.x- self.vel< self.end[0]:
            self.facing=1
        elif self.x+self.vel > self.end[1]:
            self.facing=-1
        self.x+=self.facing*self.vel
        self.draw(win)

ulquiorra= Espada(30, 430,64,64)
clock= pygame.time.Clock()
def main():
    run=True
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type== pygame.QUIT:
                run=False
        win.fill((50, 50, 50))
        ulquiorra.move(win)
        pygame.display.update()
    pygame.quit()
main()