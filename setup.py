import pygame

pygame.init()
pygame.mixer.init()

screen_width = 1200
screen_height = 600
win = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Bleach')

#Audio
pygame.mixer.music.load('audio/on the precipice of death.mp3')
pygame.mixer.music.play(-1)

score=0
killCount=0
pressed=False #for availability of signature

# --- PROJECTILE ASSETS ---
slash = [pygame.image.load(f'images/fire{i}.png') for i in range(1,7)]
slashLeft = [pygame.transform.smoothscale(img, (64,64)) for img in slash]
slashright = [pygame.transform.flip(img, True, False) for img in slashLeft]
blastLeft = slashLeft[5]
blastRight = slashright[5]

# --- PLAYER ASSETS ---
walkRight = [pygame.image.load(f'images/run{i}.png') for i in range(1, 9)]
walkLeft = [pygame.transform.flip(img, True, False) for img in walkRight]
stanceRight = [pygame.image.load(f'images/stanced{i}.png') for i in range(4, 20)]
stanceLeft = [pygame.transform.flip(img, True, False) for img in stanceRight]
stanceFinalRight = [pygame.image.load(f'images/stanced1{i}.png') for i in range(7,10)]
stanceFinalLeft = [pygame.transform.flip(img, True, False) for img in stanceFinalRight]
jumpRight = [pygame.image.load(f'images/jump{i}.png') for i in range(0,10)]
jumpLeft = [pygame.transform.flip(img, True, False) for img in jumpRight]
dashRight = [pygame.image.load(f'images/dash{i}.png') for i in range(1,4)]
dashLeft = [pygame.transform.flip(img, True, False) for img in dashRight]
attackRight = [pygame.image.load(f'images/nattack{i}.png') for i in range (0,6)]
attackLeft = [pygame.transform.flip(img, True, False) for img in attackRight]
getHitRight = [pygame.image.load(f'images/hit{i}.png') for i in range(0,10)]
getHitLeft = [pygame.transform.flip(img, True, False) for img in getHitRight]
hitRight = [pygame.image.load(f'images/hit{i}.png') for i in range(5,10)]
hitLeft = [pygame.transform.flip(img, True, False) for img in hitRight]
standUpRight = [pygame.image.load('images/stanced1.png'), pygame.image.load('images/stanced2.png'),
                pygame.image.load('images/jump1.png'), pygame.image.load('images/jump2.png'),
                pygame.image.load('images/jump7.png'), pygame.image.load('images/jump8.png'),
                pygame.image.load('images/jump9.png')]
standUpLeft = [pygame.transform.flip(img, True, False) for img in standUpRight]
getsugatenshoRight = [pygame.image.load(f'images/getsugatensho{i}.png') for i in range(1,15)]
getsugatenshoLeft = [pygame.transform.flip(img, True, False) for img in getsugatenshoRight]
attackFollowUpRight= [pygame.image.load(f'images/ichigoattack2.{i}.png') for i in range(3,8)]+[
    pygame.image.load('images/ichigoattack2.16.png')]
attackFollowUpLeft= [pygame.transform.flip(img, True, False) for img in attackFollowUpRight]

# --- ENEMY ASSETS ---
HwalkRight = [pygame.image.load(f'images/walk{i}.png') for i in range(2,10)]
HwalkLeft = [pygame.transform.flip(img, True, False) for img in HwalkRight]
HattackRight = [pygame.image.load(f'images/hattack{i}.png') for i in range(0,10)]
HattackLeft = [pygame.transform.flip(img, True, False) for img in HattackRight]
attackSeenRight = [pygame.image.load(f'images/hattack{i}.png') for i in range(7,10)]
attackSeenLeft = [pygame.transform.flip(img, True, False) for img in attackSeenRight]
fallRight = [pygame.image.load(f'images/fall{i}.png') for i in range(1,5)]
fallLeft = [pygame.transform.flip(img, True, False) for img in fallRight]

# --- UI & BG ---
hud_original = pygame.image.load('images/unnamed1.png').convert_alpha()
hud_pannel = pygame.transform.smoothscale(hud_original, (430, 150))
bg = pygame.transform.scale(pygame.image.load("images/bleach.jpeg"), (screen_width, screen_height))