import pygame

pygame.init()
pygame.mixer.init()

screen_width = 1200
screen_height = 600
win = pygame.display.set_mode((screen_width, screen_height))
surface =pygame.Surface((screen_width,screen_height),pygame.SRCALPHA)
#“This surface will use RGBA 
# (Red, Green, Blue, Alpha) instead of just RGB.”

pygame.mixer.music.load('audio/on the precipice of death.mp3')
pygame.mixer.music.play(-1)
#Alpha = transparency value:
# 0 → fully transparent
# 255 → fully opaque
# 128 → 50% transparent

Mpause= False

game_state= "mainmenu"
pygame.display.set_caption('Bleach')
font= pygame.font.SysFont('Comic Sans',30, True, False)
fontmm= pygame.font.SysFont('Arial Black',70, True, False)
#Audio
pygame.mixer.music.load('audio/on the precipice of death.mp3')
pygame.mixer.music.play(-1)

score=0
killCount=0
pressed=False #for availability of signature
pause= False

# --- PROJECTILE ASSETS ---
slash = [pygame.image.load(f'images/shot/fire{i}.png') for i in range(1,5)]
slashright = [pygame.transform.smoothscale(img, (64,64)) for img in slash]
slashLeft = [pygame.transform.flip(img, True, False) for img in slashright]

# --- PLAYER ASSETS ---
walkRight = [pygame.image.load(f'images/ichigo/run{i}.png') for i in range(1, 9)]
walkLeft = [pygame.transform.flip(img, True, False) for img in walkRight]
stanceRight = [pygame.image.load(f'images/ichigo/stanced{i}.png') for i in range(4, 20)]
stanceLeft = [pygame.transform.flip(img, True, False) for img in stanceRight]
stanceFinalRight = [pygame.image.load(f'images/ichigo/stanced1{i}.png') for i in range(7,10)]
stanceFinalLeft = [pygame.transform.flip(img, True, False) for img in stanceFinalRight]
jumpRight = [pygame.image.load(f'images/ichigo/jump{i}.png') for i in range(0,10)]
jumpLeft = [pygame.transform.flip(img, True, False) for img in jumpRight]
dashRight = [pygame.image.load(f'images/ichigo/dash{i}.png') for i in range(1,4)]
dashLeft = [pygame.transform.flip(img, True, False) for img in dashRight]
attackRight = [pygame.image.load(f'images/ichigo/nattack{i}.png') for i in range (0,6)]
attackLeft = [pygame.transform.flip(img, True, False) for img in attackRight]
getHitRight = [pygame.image.load(f'images/ichigo/hit{i}.png') for i in range(0,10)]
getHitLeft = [pygame.transform.flip(img, True, False) for img in getHitRight]
hitRight = [pygame.image.load(f'images/ichigo/hit{i}.png') for i in range(5,10)]
hitLeft = [pygame.transform.flip(img, True, False) for img in hitRight]
standUpRight = [pygame.image.load('images/ichigo/stanced1.png'), pygame.image.load('images/ichigo/stanced2.png'),
                pygame.image.load('images/ichigo/jump1.png'), pygame.image.load('images/ichigo/jump2.png'),
                pygame.image.load('images/ichigo/jump7.png'), pygame.image.load('images/ichigo/jump8.png'),
                pygame.image.load('images/ichigo/jump9.png')]
standUpLeft = [pygame.transform.flip(img, True, False) for img in standUpRight]
getsugatenshoRight = [pygame.image.load(f'images/ichigo/getsugatensho{i}.png') for i in range(1,15)]
getsugatenshoLeft = [pygame.transform.flip(img, True, False) for img in getsugatenshoRight]
attackFollowUpRight= [pygame.image.load(f'images/ichigo/ichigoattack2.{i}.png') for i in range(3,8)]+[
    pygame.image.load('images/ichigo/ichigoattack2.16.png')]
attackFollowUpLeft= [pygame.transform.flip(img, True, False) for img in attackFollowUpRight]

# --- PLAYER BANKAI ASSETS ---
bankaiWalkRight = [pygame.image.load(f'images/bankai/run{i}.png') for i in range(1, 9)]
bankaiWalkLeft = [pygame.transform.flip(img, True, False) for img in bankaiWalkRight]
bankaiStanceRight = [pygame.image.load(f'images/bankai/stance{i}.png') for i in range(1, 5)]
bankaiStanceLeft = [pygame.transform.flip(img, True, False) for img in bankaiStanceRight]
bankaiJumpRight = [pygame.image.load(f'images/bankai/jump{i}.png') for i in range(1, 10)]
bankaiJumpLeft = [pygame.transform.flip(img, True, False) for img in bankaiJumpRight]
bankaiDashRight = [pygame.image.load(f'images/bankai/dash{i}.png') for i in range(1, 4)]
bankaiDashLeft = [pygame.transform.flip(img, True, False) for img in bankaiDashRight]
bankaiHitRight = [pygame.image.load(f'images/bankai/hit{i}.png') for i in range(1, 11)]
bankaiHitLeft = [pygame.transform.flip(img, True, False) for img in bankaiHitRight]


# --- ENEMY ASSETS ---
HwalkRight = [pygame.image.load(f'images/menosgrande/walk{i}.png') for i in range(2,10)]
HwalkLeft = [pygame.transform.flip(img, True, False) for img in HwalkRight]
HattackRight = [pygame.image.load(f'images/menosgrande/hattack{i}.png') for i in range(0,10)]
HattackLeft = [pygame.transform.flip(img, True, False) for img in HattackRight]
attackSeenRight = [pygame.image.load(f'images/menosgrande/hattack{i}.png') for i in range(7,10)]
attackSeenLeft = [pygame.transform.flip(img, True, False) for img in attackSeenRight]
fallRight = [pygame.image.load(f'images/menosgrande/fall{i}.png') for i in range(1,5)]
fallLeft = [pygame.transform.flip(img, True, False) for img in fallRight]
blownRight=[pygame.image.load(f'images/menosgrande/blown{i}.png')for i in range(1,4)] 
blownLeft= [pygame.transform.flip(img, True, False) for img in blownRight]

# --- UI & BG ---
hud_original = pygame.image.load('images/setup/unnamed1.png').convert_alpha()
hud_pannel = pygame.transform.smoothscale(hud_original, (430, 150))
bg = pygame.transform.scale(pygame.image.load("images/setup/bleach.jpeg"), (screen_width, screen_height))
mute= pygame.transform.smoothscale(pygame.image.load('images/setup/volume-mute.png'),(64,64))

def pause_music():
    if Mpause:
        pygame.mixer.music.pause()
    else:
        pygame.mixer.music.unpause()


NON_INTERRUPT_KEYS= {pygame.K_SPACE,
                     pygame.K_LSHIFT,
                     pygame.K_z,
                     pygame.K_LEFT,
                     pygame.K_RIGHT, 
                     pygame.K_a,
                    pygame.K_d,
                    pygame.K_ESCAPE,
                    pygame.K_m
                     }