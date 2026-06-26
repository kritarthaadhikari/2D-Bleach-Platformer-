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

    def move(self,player):
        if player.mode=="bankai":
            self.x+= self.direction*self.vel*2
        else:
            self.x+= self.direction*self.vel
    
    def kill(self):
        if self in projectiles[:]:
            projectiles.remove(self)
    
class Cero(Projectile):
    def __init__(self, x, y, width, height, facing):
        super().__init__(x, y, width, height, facing)
        self.vel=30
        self.start_x=x
        self.max_distance=650
        self.active=False
    
    def draw(self,win,aizen):
        framesPerImg=3
        sprite=None
        if not self.active:
            return
        frames = st.ceroRight if self.direction == 1 else st.ceroLeft
        if not frames:
            return
        limit=len(frames)*framesPerImg
        frame = min(self.count // framesPerImg, len(frames)-1)
        sprite=frames[frame]
        if self.count+1>=limit:
            self.count=0
            self.kill()
        else:
            self.count+=1
        if sprite:
            win.blit(sprite,(self.x,self.y))

    def move(self,aizen):
        if not self.active:
            return
        self.x += self.direction * self.vel
        if abs(self.x - self.start_x) >= self.max_distance:
            self.kill()
        if self.x > st.screen_width + 200 or  self.x < 0:
            self.kill()

    def kill(self):
        self.active=False
        if self in cero[:]:
            cero.remove(self)

    
