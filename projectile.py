import pygame
import aizen
import setup as st
import player as pl

projectiles = []
cero= []
class Projectile(pygame.Rect):
    def __init__(self,x,y,width,height,facing):
        super().__init__(x,y,width,height)
        self.vel= 15
        self.count=0
        self.getsugatenshou=False
        self.direction= facing
        self.hitEnemies= [] #stores hollows that have been hit and prevents repeated hits
        self.shot={
            "bankai":{
                "shotRight": st.getsugatenshoProjectileRight,
                "shotLeft": st.getsugatenshoProjectileLeft
            },
            "shikai":{
                "shotRight": st.slashright,
                "shotLeft": st.slashLeft
            }
        }
    
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
        if self.shot!="bankai" and self.getsugatenshou:
            self.x+=self.direction*5
        win.blit(sprite, (self.x - scroll,self.y))
        #pygame.draw.rect(win, (255,0,0),self,2) for hitbox

    def move(self,player):
        if player.mode=="bankai":
            self.x+= self.direction*self.vel*2
        else:
            self.x+= self.direction*self.vel
        # Note: We pass win from the main loop to this method later
    
    def kill(self):
        if self in projectiles[:]:
            projectiles.remove(self)
    
class Cero(Projectile):
    def __init__(self, x, y, width, height, facing):
        super().__init__(x, y, width, height, facing)
        self.vel=30
        self.start_x=x
        self.max_distance=650
    
    def draw(self,win,aizen):
        framesPerImg=3
        sprite=None
        if aizen.cero_started:
            if not st.ceroRight:
                return
            limit=len(st.ceroRight)*framesPerImg
            frame = min(self.count // framesPerImg, len(st.ceroRight)-1)
            if self.direction==1:
                sprite=st.ceroRight[frame]
            else:
                sprite=st.ceroLeft[frame]
            if self.count+1>=limit:
                self.count=0
                aizen.cero_started=False
                self.kill()
            else:
                self.count+=1
        if sprite:
            win.blit(sprite,(self.x,self.y))

    def move(self,aizen):
        if aizen.cero_started:
            self.x += self.direction * self.vel
            if abs(self.x - self.start_x) >= self.max_distance:
                self.kill()

    def kill(self):
        if self in cero[:]:
            cero.remove(self)

    
