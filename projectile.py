import pygame
import setup as st
import player as pl

projectiles = []

class Projectile(pygame.Rect):
    def __init__(self,x,y,width,height,facing):
        super().__init__(x,y,width,height)
        self.vel= 15
        self.count=0
        self.getsugatenshou=False
        self.direction= facing
        self.hitEnemies= []
        self.shot={
            "bankai":{
                "shotRight": st.getsugatenshoProjectileRight,
                "shotLeft": st.getsugatenshoProjectileLeft
            },
            "shikai":{
                "shotRight": st.slashright,
                "shotLeft": st.slashLeft
            }
        } #stores hollows that have been hit and prevents repeated hits
    
    def draw(self,win, scroll=0,player=None):
        framesPerImg=3
        sprite=None
        if self.getsugatenshou :
            limit= 3*len(self.shot[player.mode]["shotRight"])
            if self.direction==1:
                sprite= self.shot[player.mode]["shotRight"][self.count//framesPerImg]
            else:
                sprite= self.shot[player.mode]["shotLeft"][self.count//framesPerImg]
            if self.count+1>=limit:
                self.count=0
                self.getsugatenshou=False
                self.kill()
            self.count+=1 
        win.blit(sprite, (self.x - scroll,self.y))
        #pygame.draw.rect(win, (255,0,0),self,2) for hitbox

    def move(self,player):
        self.x+= self.direction*self.vel*(player.incrementalFactor//2)
        # Note: We pass win from the main loop to this method later
    
    def kill(self):
        if self in projectiles[:]:
            projectiles.remove(self)