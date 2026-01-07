import pygame
import time

pygame.init()
# Screen setup
screen_width = 1200
screen_height = 600
win = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Bleach')

# Background
bg = pygame.transform.scale(pygame.image.load("bleach.jpeg"), (screen_width, screen_height))

# Music
pygame.mixer.music.load('on the precipice of death.mp3')
pygame.mixer.music.play(-1)
#0 for once, 1 for twice 2 for thrice,etc

# Sprites
#Player
walkRight = [pygame.image.load(f'run{i}.png') for i in range(1, 9)]
walkLeft = [pygame.transform.flip(img, True, False) for img in walkRight]
stanceRight = [pygame.image.load(f'stanced{i}.png') for i in range(4, 20)]
stanceLeft = [pygame.transform.flip(img, True, False) for img in stanceRight]
stanceFinalRight = [pygame.image.load(f'stanced1{i}.png') for i in range(7,10)]
stanceFinalLeft= [pygame.transform.flip(img, True, False) for img in stanceFinalRight]
jumpRight= [pygame.image.load(f'jump{i}.png') for i in range(0,10)]
jumpLeft= [pygame.transform.flip(img, True, False) for img in jumpRight]
dashRight= pygame.image.load('dash2.png')
dashLeft= pygame.transform.flip(dashRight, True, False)
attackRight= [pygame.image.load(f'attack{i}.png') for i in range(1,7)]
attackLeft= [pygame.transform.flip(img, True, False) for img in attackRight]

#Enemy
HwalkRight=[pygame.image.load(f'walk{i}.png') for i in range(2,10)]
HwalkLeft= [pygame.transform.flip(img, True, False) for img in HwalkRight]
HattackRight= [pygame.image.load(f'hattack{i}.png') for i in range(0,10)]
HattackLeft= [pygame.transform.flip(img, True, False) for img in HattackRight]
kickRight= [pygame.image.load(f'kick{i}.png') for i in range(0,3)]
kickLeft= [pygame.transform.flip(img, True, False) for img in kickRight]

# Player class
class Player:
    def __init__(self, width, height, x, y):
        self.width = width
        self.height = height
        self.x = x
        self.feet_y = y  # y-coordinate of the character's feet
        self.vel = 5
        self.walkCount = 0
        self.stanceCount = 0
        self.stanceFinal=0
        self.stancephase=0
        self.jumpCount = 10
        self.spjumpCount=0
        self.isJump = False
        self.right = False
        self.left = False
        self.standing = True
        self.dashing= False
        self.dashCount= 0
        self.facing= 1
        self.dashTimer= 10
        self.attacking= False
        self.attackCount= 0
        self.hitbox= pygame.Rect(self.x+10, self.feet_y-4,50, 52 )

    def draw(self, win):
        # Select current sprite
        framesPerImg = 3
        sprite = jumpLeft[0]

        if not self.standing and not self.isJump and not self.attacking:
            self.stancephase=0
            if self.dashing:
                if self.facing==1:
                    # limit = len(dashRight) 
                    # sprite = dashRight[self.dashCount // framesPerImg]
                    sprite= dashRight
                
                else:
                    # limit = len(dashLeft) 
                    # sprite = dashLeft[self.dashCount // framesPerImg]
                    sprite= dashLeft
                # self.dashCount += 1
                # if self.dashCount +1>= limit:
                #     self.dashCount = 0
                
                # self.dashTimer-=1
                # if self.dashTimer<=0:
                #     self.dashing= False
                #     self.dashCount=0
                
            if self.left:
                limit = len(walkLeft) * framesPerImg
                sprite = walkLeft[self.walkCount // framesPerImg]

            elif self.right:
                limit = len(walkRight) * framesPerImg
                sprite = walkRight[self.walkCount // framesPerImg]
            if self.walkCount +1>= limit:
                self.walkCount = 0
            self.walkCount += 1
        
        elif self.attacking:
            framesPerImg=4
            if self.facing==1:
                limit= len(attackRight)*framesPerImg
                sprite= attackRight[self.attackCount// framesPerImg]
            else:
                limit= len(attackLeft)*framesPerImg
                sprite= attackLeft[self.attackCount// framesPerImg]
            self.attackCount+=1
            if self.attackCount+1 >= limit:
                self.attackCount=0
                self.attacking=False

        elif self.isJump:
            if self.facing==1:
                limit = len(jumpRight)* framesPerImg
                sprite= jumpRight[self.spjumpCount//framesPerImg]
            else:
                limit = len(jumpLeft)* framesPerImg
                sprite= jumpLeft[self.spjumpCount//framesPerImg]
            if self.spjumpCount +1>= limit:
                self.spjumpCount=0
            self.spjumpCount += 1

        else:
            if self.stancephase==0: 
                if self.facing==-1:
                    limit = len(stanceLeft) * framesPerImg
                    sprite = stanceLeft[self.stanceCount // framesPerImg]

                elif self.facing==1:
                    limit = len(stanceRight) * framesPerImg
                    sprite = stanceRight[self.stanceCount // framesPerImg]
                self.stanceCount += 1
                if self.stanceCount +1>= limit:
                    self.stanceCount=0
                    self.stancephase=1

            else:
                if self.facing==-1:
                    limit = len(stanceFinalLeft)* framesPerImg
                    sprite = stanceFinalLeft[self.stanceFinal // framesPerImg]
                else:
                    limit = len(stanceFinalRight)* framesPerImg
                    sprite = stanceFinalRight[self.stanceFinal // framesPerImg]
                self.stanceFinal+=1
                if self.stanceFinal+1>= limit:
                    self.stanceFinal=0
                    self.stanceCount=0
        # Draw sprite using feet position
        pygame.draw.rect(win, (255,0,0), (self.x+10, self.feet_y-4,50, 52 ))
        sprite_height = sprite.get_height()
        draw_y = self.feet_y - sprite_height+50
        win.blit(sprite, (self.x, draw_y))

    def hit(self):
        self.x=0
        

#Enemy Class
class Enemy:
    def __init__(self,width,height,x,y):#dunder - double underscore
        self.x= x
        self.feet= y
        self.width= width
        self.height= height
        self.vel=2
        self.facing=-1
        self.walkCount=0
        self.end= [self.x,self.width-30]
        self.attackCount=0
        self.lastattackTimer= time.time()
        self.attacking= False
        self.hitbox= pygame.Rect(self.x+10, self.feet-100,85, 150 )
    
    def draw(self,win):
        framesPerImg=4
        current= time.time()
        if current- self.lastattackTimer > 3.0:
            self.attacking= True
            if self.facing==1:
                limit= len(HattackRight)*framesPerImg
                sprite= HattackRight[self.attackCount//framesPerImg]
            elif self.facing==-1:
                limit= len(HattackLeft)*framesPerImg
                sprite= HattackLeft[self.attackCount//framesPerImg]
            self.attackCount+=1
            if self.attackCount+1>=limit:
                self.attackCount=0 
                self.attacking= False
                self.lastattackTimer= time.time()

        elif self.facing==-1:
            limit= len(HwalkLeft)* framesPerImg
            sprite= HwalkLeft[self.walkCount//framesPerImg]
        elif self.facing==1:
            limit= len(HwalkRight)*framesPerImg
            sprite= HwalkRight[self.walkCount//framesPerImg]
        self.walkCount+=1
        if self.walkCount+1>= limit:
            self.walkCount=0
        pygame.draw.rect(win, (255,0,0), (self.x+10, self.feet-100,85, 150 ))
        sprite_height= sprite.get_height()
        draw_y= self.feet- sprite_height+50
        win.blit(sprite , (self.x, draw_y))
    
    def move(self):
        if not self.attacking:
            if self.x==self.end[0]:
                self.facing=-1
            elif self.x==self.end[1]:
                self.facing=1
            self.x+= self.facing* self.vel
        self.draw(win)

# Redraw function
def redrawwindow():
    win.blit(bg, (0, 0))
    player.draw(win)
    enemy.move()
    pygame.display.update()

def hit():
    pass

# Clock and player initialization
clock = pygame.time.Clock()
player = Player(64, 64, 10, 410)
enemy = Enemy(110, 149, 560, 410)

# Main game loop
def main():
    run = True
    while run:
        clock.tick(24)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
         
            if event.type == pygame.KEYDOWN:
                if event.key== pygame.K_SPACE:
                    player.standing= False
                    player.attacking= True
                    player.stancephase=0
                
                elif event.key== pygame.K_LSHIFT:
                   if player.vel < player.x < screen_width - player.width - player.vel:
                        player.x+= player.facing*70
                        player.standing= False
                        player.dashing= True
            
        keys = pygame.key.get_pressed()
        # Left/right movement
        if not player.attacking:

            if keys[pygame.K_LEFT] and player.x > player.vel:
                player.x -= player.vel
                player.left = True
                player.right = False
                player.standing = False
                player.dashing= False
                player.facing= -1

            elif keys[pygame.K_RIGHT] and player.x+ player.width+ player.vel < screen_width:
                player.x += player.vel
                player.left = False
                player.right = True
                player.standing = False
                player.dashing= False
                player.facing= 1

            else:
                player.standing = True
                player.dashing= False
                player.walkCount = 0
                player.dashCount=0

        # Jump logic
        if not player.isJump:
            if keys[pygame.K_UP]:
                player.isJump = True
                player.right = False
                player.left = False
                player.standing = False
        else:
            if player.jumpCount >= -10:
                neg = 1
                if player.jumpCount < 0:
                    neg = -1
                # Update feet_y instead of y
                player.feet_y -= (player.jumpCount ** 2) * 0.5 * neg
                player.x+=player.facing*2
                player.jumpCount -= 1
            else:
                player.jumpCount = 10
                player.isJump = False
        
        if player.hitbox.colliderect(enemy.hitbox):
                player.hit()

        redrawwindow()

    pygame.quit()


main()
