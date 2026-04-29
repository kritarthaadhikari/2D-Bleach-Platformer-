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
HitRight = [pygame.image.load(f'images/ichigo/hit{i}.png') for i in range(0,10)]
HitLeft = [pygame.transform.flip(img, True, False) for img in HitRight]
IdleHitRight = [pygame.image.load(f'images/ichigo/hit{i}.png') for i in range(5,10)]
IdleHitLeft = [pygame.transform.flip(img, True, False) for img in IdleHitRight]
standUpRight = [pygame.image.load('images/ichigo/stanced1.png'), pygame.image.load('images/ichigo/stanced2.png'),
                pygame.image.load('images/ichigo/jump1.png'), pygame.image.load('images/ichigo/jump2.png'),
                pygame.image.load('images/ichigo/jump7.png'), pygame.image.load('images/ichigo/jump8.png'),
                pygame.image.load('images/ichigo/jump9.png')]
standUpLeft = [pygame.transform.flip(img, True, False) for img in standUpRight]
getsugatenshoRight = [pygame.image.load(f'images/ichigo/getsugatensho{i}.png') for i in range(1,15)]
getsugatenshoLeft = [pygame.transform.flip(img, True, False) for img in getsugatenshoRight]
attackFollowUpRight=[pygame.transform.smoothscale(pygame.image.load(f'images/ichigo/niattack1.png'), (64,64)),
                    pygame.transform.smoothscale(pygame.image.load(f'images/ichigo/niattack2.png'), (69,64)),
                    pygame.transform.smoothscale(pygame.image.load(f'images/ichigo/niattack3.png'), (64,64)),
                    pygame.transform.smoothscale(pygame.image.load(f'images/ichigo/niattack4.png'), (72,64)),
                    pygame.transform.smoothscale(pygame.image.load(f'images/ichigo/niattack5.png'), (47,67)),
                    pygame.transform.smoothscale(pygame.image.load(f'images/ichigo/niattack6.png'), (58,58))]
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
bankaiAttackRight = [pygame.image.load(f'images/bankai/attack{i}.png') for i in range(0, 6)]
bankaiAttackLeft = [pygame.transform.flip(img, True, False) for img in bankaiAttackRight]
bankaiIdleHitRight= [pygame.image.load(f'images/bankai/hit{i}.png') for i in range(5,10)]
bankaiIdleHitLeft = [pygame.transform.flip(img, True, False) for img in bankaiIdleHitRight]
bankaistandUpRight = [pygame.image.load('images/bankai/stanced1.png'), pygame.image.load('images/bankai/stanced2.png'),
                       pygame.image.load('images/bankai/jump2.png'),pygame.image.load('images/bankai/jump3.png'), 
                       pygame.image.load('images/bankai/jump7.png'),pygame.image.load('images/bankai/jump8.png'), 
                       pygame.image.load('images/bankai/jump9.png')]
bankaistandUpLeft = [pygame.transform.flip(img, True, False) for img in bankaistandUpRight]
bankaiGetsugatenshoRight = [pygame.image.load(f'images/bankai/getsugatensho{i}.png') for i in range(0,11)]
bankaiGetsugatenshoLeft = [pygame.transform.flip(img, True, False) for img in bankaiGetsugatenshoRight]
bankaiFollowUpRight=[pygame.image.load(f'images/bankai/fattack{i}.png') for i in range(1,7)]
bankaiFollowUpLeft = [pygame.transform.flip(img, True, False) for img in bankaiFollowUpRight]




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