import pygame
import setup as st

projectiles = []

class Projectile(pygame.Rect):
    def __init__(self,x,y,width,height,facing):
        super().__init__(x,y,width,height)
        self.vel= 10
        self.count=0
        self.getsugatenshou=False
        self.direction= facing
        self.hit= True
    
    def draw(self,win):
        if self.hit:
            limit=3
            if self.direction==1:
                sprite= st.blastRight
            else:
                sprite= st.blastLeft
            if self.count+1>=limit:
                self.count=0
                self.hit= False
            self.count+=1

        elif self.getsugatenshou :
            limit= 3*len(st.slashLeft)
            if self.direction==1:
                sprite= st.slashright[self.count//3]
            else:
                sprite= st.slashLeft[self.count//3]
            if self.count+1>=limit:
                self.count=0
                self.getsugatenshou=False
                self.kill()
            self.count+=1 
        
        if self.hit:
            win.blit(st.blastLeft,(self.x,self.y))
        win.blit(sprite, (self.x,self.y))
        #pygame.draw.rect(win, (255,0,0),self,2) for hitbox

    def move(self):
        self.x+= self.direction*self.vel
        # Note: We pass win from the main loop to this method later
    
    def kill(self):
        if self in projectiles[:]:
            projectiles.remove(self)