import setup as st
import pygame
class Aizen:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hitbox= pygame.Rect(self.x+10, self.y-4, 74, 74)
        self.health=800
        self.vel=6
        self.walkCount=0
        self.facing=-1
        self.idleCount=0
        self.action="idle" #idle, sec_idle, walk, attack, hit, death

    def draw(self, win):
        self.hitbox= pygame.Rect(self.x+10, self.y-4, 74, 74)
        pygame.draw.rect(win, (255,0,0), self.hitbox,2)
        framesPerImg=3
        if self.action=="idle":
            limit=len(st.AizenStanceRight)*framesPerImg
            if self.facing==-1:
                sprite=st.AizenStanceLeft[self.idleCount//framesPerImg] 
            else:
                sprite=st.AizenStanceRight[self.idleCount//framesPerImg]
            if self.idleCount+1>=limit: 
                self.idleCount=0
                self.action="sec_idle"
            else:
                self.idleCount+=1    
        elif self.action=="sec_idle":
            limit=len(st.AizenStanceMiddleLeft)*framesPerImg
            if self.facing==-1:
                sprite=st.AizenStanceMiddleLeft[self.idleCount//framesPerImg] 
            else:
                sprite=st.AizenStanceMiddleRight[self.idleCount//framesPerImg]
            if self.idleCount+1>=limit: 
                self.idleCount=0
                self.action="third_idle"
            else:
                self.idleCount+=1
        elif self.action=="third_idle": 
            limit=len(st.AizenStanceFinalLeft)*framesPerImg
            if self.facing==-1:
                sprite=st.AizenStanceFinalLeft[self.idleCount//framesPerImg] 
            else:
                sprite=st.AizenStanceFinalRight[self.idleCount//framesPerImg]
            if self.idleCount+1>=limit: 
                self.idleCount=0
                self.action="idle"
            else:
                self.idleCount+=1
        st.win.blit(sprite, (self.x, self.y))
        


