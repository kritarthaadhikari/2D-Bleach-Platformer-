import pygame

pygame.init()
pygame.mixer.init()

screen_width = 1280
screen_height = 720
feet_y_initial = 616
win = pygame.display.set_mode((screen_width, screen_height))
surface =pygame.Surface((screen_width,screen_height),pygame.SRCALPHA)
ground= pygame.transform.smoothscale(pygame.image.load('images/setup/ground.png').convert_alpha(), (screen_width, 100))
#“This surface will use RGBA 
# (Red, Green, Blue, Alpha) instead of just RGB."

pygame.mixer.music.load('audio/on the precipice of death.mp3')
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play(-1)

bankaiSound= pygame.mixer.Sound('audio/ichigobankai.wav')
bankaiSound.set_volume(0.5)

getsugatenshoSound= pygame.mixer.Sound('audio/getsugatensho.wav')
getsugatenshoSound.set_volume(0.5)

hollowSound= pygame.mixer.Sound('audio/hollowscream.mp3')
hollowSound.set_volume(1)
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
killCount=1
killCountperRound=0
pause= False
scroll=False
arrow= pygame.transform.flip(pygame.transform.smoothscale(pygame.image.load('images/setup/arrow.png'),(100,100)),True, False)

#Signature Display Parameters
text_duration= 1000 #1s
text_start_time= 0
current_time=0
show_text= False

#Aizen
lastTeleport= pygame.time.get_ticks()
lastCero= pygame.time.get_ticks()

#Bankai Display Parameters
text_duration_bankai= 2000 #2s
text_start_time_bankai= 0
current_time_bankai=0

# --- PROJECTILE ASSETS ---
slash = [pygame.image.load(f'images/shot/fire{i}.png') for i in range(1,5)]
slashright = [pygame.transform.smoothscale(img, (64,64)) for img in slash]
slashLeft = [pygame.transform.flip(img, True, False) for img in slashright]
ceroRight = [pygame.transform.smoothscale(pygame.image.load('images/shot/cero.png').convert_alpha(), (64, 64))]*200
ceroLeft =[pygame.transform.flip(img, True, False) for img in ceroRight]
getsugatenshoProjectileRight = [pygame.transform.smoothscale(pygame.image.load(f'images/shot/getsuga{i}.png'), (64, 64)) for i in range(1,3)]*100
getsugatenshoProjectileLeft = [pygame.transform.flip(img, True, False) for img in getsugatenshoProjectileRight]
gargantaRight= [pygame.transform.smoothscale(pygame.image.load(f'images/menosgrande/garganta1.png'), (36, 190)),
                 pygame.transform.smoothscale(pygame.image.load(f'images/menosgrande/garganta2.png'), (65, 200)),
                 pygame.transform.smoothscale(pygame.image.load(f'images/menosgrande/garganta3.png'), (95,200)),
                 pygame.transform.smoothscale(pygame.image.load(f'images/menosgrande/garganta4.png'), (115, 250)),
                 pygame.transform.smoothscale(pygame.image.load(f'images/menosgrande/garganta5.png'), (95, 230)),
                 pygame.transform.smoothscale(pygame.image.load(f'images/menosgrande/garganta6.png'), (72, 200))]
gargantaLeft= [pygame.transform.flip(img, True, False) for img in gargantaRight]

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
attackRight = [pygame.image.load(f'images/ichigo/attack{i}.png') for i in range (1,6)]
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
standUpAutoRight=[pygame.image.load(f'images/ichigo/stanced{i}.png') for i in range(1,4)]
standUpAutoLeft=[pygame.transform.flip(img, True, False) for img in standUpAutoRight]
getsugatenshoLeft = [pygame.transform.flip(img, True, False) for img in getsugatenshoRight]
attackFollowUpRight=[pygame.image.load(f'images/ichigo/fattack{i}.png') for i in range(1,7)]
attackFollowUpLeft= [pygame.transform.flip(img, True, False) for img in attackFollowUpRight]
shikaiTransformRight= [pygame.image.load(f'images/bankai/shikai{i}.png') for i in range(1,8)]
shikaiTransformLeft= [pygame.transform.flip(img, True, False) for img in shikaiTransformRight]
hitSteadyRight= [pygame.image.load('images/ichigo/hit2.png')]*3
hitSteadyLeft= [pygame.transform.flip(img, True, False) for img in hitSteadyRight]
hitbyAizenRight= [pygame.image.load(f'images/ichigo/hit{i}.png') for i in range(0,3)]+hitSteadyRight
hitbyAizenLeft= [pygame.transform.flip(img, True, False) for img in hitbyAizenRight]+hitSteadyLeft

# --- PLAYER BANKAI ASSETS ---
bankaiWalkRight = [pygame.image.load(f'images/bankai/run{i}.png') for i in range(1, 9)]
bankaiWalkLeft = [pygame.transform.flip(img, True, False) for img in bankaiWalkRight]
bankaiStanceRight = [pygame.image.load(f'images/bankai/stance{i}.png') for i in range(1, 5)]
bankaiStanceLeft = [pygame.transform.flip(img, True, False) for img in bankaiStanceRight]
bankaiJumpRight = [pygame.image.load(f'images/bankai/jump{i}.png') for i in range(1, 10)]
bankaiJumpLeft = [pygame.transform.flip(img, True, False) for img in bankaiJumpRight]
bankaiDashRight = [pygame.image.load(f'images/bankai/dash{i}.png') for i in range(1, 3)]
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
bankaiTransformRight= [pygame.image.load(f'images/bankai/bankai{i}.png') for i in range(1,9)]
bankaiTransformLeft = [pygame.transform.flip(img, True, False) for img in bankaiTransformRight]
getsugatensho= pygame.image.load('images/bankai/getsuga.png')
bankaihitbyAizenRight= [pygame.image.load(f'images/bankai/hit{i}.png') for i in range(1,4)]
bankaihitbyAizenLeft=[pygame.transform.flip(img, True, False) for img in bankaihitbyAizenRight]
bankaihitsteadyRight= [pygame.image.load('images/bankai/hit3.png')]*10
bankaihitsteadyLeft= [pygame.transform.flip(img,True, False) for img in bankaihitsteadyRight]

#Visored
VisoredTransformRight= [pygame.image.load(f'images/visored/transform{i}.png') for i in range(1,4)]
VisoredTransformLeft= [pygame.transform.flip(img, True, False) for img in VisoredTransformRight]
VisoredToBankaiRight = [pygame.image.load(f'images/visored/transformback{i}.png') for i in range(1,5)]
VisoredToBankaiLeft = [pygame.transform.flip(img, True, False) for img in VisoredToBankaiRight]
VisoredWalkRight =[pygame.transform.smoothscale(pygame.image.load(f'images/visored/run{i}.png'),(64,64) )
                   for i in range(1,4)]
VisoredWalkLeft =[pygame.transform.flip(img, True, False) for img in VisoredWalkRight]

#bankai visuals
bankai= pygame.image.load('images/bankai/bankai.png')
tr= pygame.image.load('images/bankai/TR1.png')
tl= pygame.image.load('images/bankai/TL.png')

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

#Aizen ASSETS
AizenattackRight= [pygame.image.load(f'images/Aizen/attack{i}.png') for i in range(1,6)]
AizenattackLeft= [pygame.transform.flip(img, True, False) for img in AizenattackRight]
AizensecondAttackRight =[pygame.image.load('images/Aizen/attack1.png')]+[pygame.image.load(f'images/Aizen/attack2.{i}.png') for i in range(2,5)]
AizensecondAttackLeft= [pygame.transform.flip(img, True, False) for img in AizensecondAttackRight]
AizenStanceRight= [pygame.image.load(f'images/Aizen/stance{i}.png') for i in range(1,4)]
AizenStanceLeft= [pygame.transform.flip(img, True, False) for img in AizenStanceRight]
AizenHitRight= [pygame.image.load(f'images/Aizen/hit1.png')]*10
AizenHitLeft= [pygame.transform.flip(img, True, False) for img in AizenHitRight]
AizenRunRight= [pygame.image.load(f'images/Aizen/run{i}.png') for i in range(1,3)]
AizenRunLeft= [pygame.transform.flip(img, True, False) for img in AizenRunRight]
AizenJumpAttackRight= [pygame.image.load(f'images/Aizen/jumpattack{i}.png') for i in range(1,4)]
AizenJumpAttackLeft= [pygame.transform.flip(img, True, False) for img in AizenJumpAttackRight]
AizenTeleportRight= [pygame.image.load(f'images/Aizen/teleport{i}.png') for i in range(1,14)]
AizenTeleportLeft= [pygame.transform.flip(img, True, False) for img in AizenTeleportRight]
AizenStanceMiddleRight= [pygame.image.load(f'images/Aizen/wait{i}.png') for i in range(1,8)]
AizenStanceMiddleLeft= [pygame.transform.flip(img, True, False) for img in AizenStanceMiddleRight]
AizenCeroRight= [pygame.image.load(f'images/Aizen/cero{i}.png') for i in range(1,6)]
AizenCeroLeft= [pygame.transform.flip(img, True, False) for img in AizenCeroRight]
AizenStanceFinalRight= [pygame.image.load(f'images/Aizen/aurafarm{i}.png') for i in range(1,6)]
AizenStanceFinalLeft= [pygame.transform.flip(img, True, False) for img in AizenStanceFinalRight]
AizenFinalIdleRight= [pygame.image.load('images/Aizen/aurafarm1.png'),
                      pygame.image.load('images/Aizen/aurafarm5.png')]
AizenFinalIdleLeft= [pygame.transform.flip(img,True, False) for img in AizenFinalIdleRight]
AizenTitle= pygame.transform.smoothscale(pygame.image.load('images/setup/aizen_title.png'),(150,30))
AizenHoldAfterCeroRight= [pygame.image.load(f'images/Aizen/cero1.png')]
AizenHoldAfterCeroLeft= [pygame.transform.flip(img, True, False) for img in AizenHoldAfterCeroRight]

# --- UI & BG ---
hud_original = pygame.image.load('images/setup/hudpannel.png').convert_alpha()
hud_pannel = pygame.transform.smoothscale(hud_original, (450, 246))
bg = pygame.transform.scale(pygame.image.load("images/setup/background.png"), (screen_width, screen_height))
mute= pygame.transform.smoothscale(pygame.image.load('images/setup/volume-mute.png'),(64,64))

def pause_music():
    if Mpause:
        pygame.mixer.music.pause()
    else:
        pygame.mixer.music.unpause()

# gargantaCount=0
# gargantaH=[]
# def drawgarganta(enemy):
#     global gargantaCount
#     framesPerImg= 8
#     limit=len(gargantaRight)*framesPerImg
#     if enemy.facing==1:
#         sprite= gargantaRight[gargantaCount//framesPerImg]
#     else:
#         sprite= gargantaLeft[gargantaCount//framesPerImg]
#     if gargantaCount+1>= limit:
#         gargantaCount=0
#         gargantaH.append(enemy)
#     gargantaCount+=1
#     win.blit(sprite, (enemy.static_x-enemy.facing*20, enemy.feet-160))

NON_INTERRUPT_KEYS= {pygame.K_SPACE,
                     pygame.K_LSHIFT,
                     pygame.K_z,
                     pygame.K_LEFT,
                     pygame.K_RIGHT, 
                     pygame.K_a,
                    pygame.K_d,
                    pygame.K_ESCAPE,
                    pygame.K_m
                    ,pygame.K_UP,
                    pygame.K_w
                     }

EXISTING_KEYS={pygame.K_SPACE,
               pygame.K_LSHIFT,
               pygame.K_z,
               pygame.K_LEFT,
               pygame.K_RIGHT
               ,pygame.K_a,
               pygame.K_d,
               pygame.K_ESCAPE,
               pygame.K_m,
               pygame.K_UP,
               pygame.K_w,
               pygame.K_b,
               }