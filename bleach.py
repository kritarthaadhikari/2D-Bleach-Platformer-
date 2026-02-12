import pygame
import setup as st
import projectile as pj
import enemy as en
import player as pl
import time

clock = pygame.time.Clock()
player = pl.Player(64, 64, 10, 500)
enemy = en.Enemy(110, 149, 1200, 500)
en.hollows.append(enemy)
font= pygame.font.SysFont('Comic Sans',30, True, False)

def hudPannel():
    pygame.draw.rect(st.win,(255,0,0),(212,59,212,23))
    pygame.draw.rect(st.win,(0,255,0),(212,59,212- 53*(120-player.health)/30,22 ))
    pygame.draw.rect(st.win,(255,255,0),(175,89,188-(100-player.staminaGauge)*1.88,14))
    pygame.draw.rect(st.win,"cyan",(237,116,st.score*2.37,18))
    
    st.win.blit(st.hud_pannel, (10,10))

def redrawwindow():
    st.win.blit(st.bg, (0, 0))
    hudPannel()
    for e in en.hollows:
        e.move(st.win)
    player.draw(st.win)
    text= font.render(f"Score: {st.score}",1,(255,255,255))
    st.win.blit(text,(st.screen_width-text.get_width()-20, 0))
    if player.signatureCount>=21:
        for p in pj.projectiles[:]:
           p.move()
           p.draw(st.win)
    pygame.display.update()   

last_enemy_spawn = time.time()

def createEnemies():
    global last_enemy_spawn
    if time.time() - last_enemy_spawn >= 10:
        new_enemy = en.Enemy(110, 149, 1200, 500)
        en.hollows.append(new_enemy)
        last_enemy_spawn = time.time()

def main():
    run = True
    while run:
        clock.tick(24)
        createEnemies()
        
        if player.staminaGauge<100:
            player.staminaGauge+=1
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
         
            if event.type == pygame.KEYDOWN:
                if event.key== pygame.K_SPACE:
                    player.standing= False
                    player.attacking= True
                    player.signature=False
                    player.stancephase=0
                
                elif event.key== pygame.K_LSHIFT:
                   if player.vel < player.x < st.screen_width - player.width - player.vel and player.staminaGauge>=20:
                        player.x+= player.facing*40
                        player.standing= False
                        player.dashing= True
                        player.dashCount=0
                        player.staminaGauge-=20
           
                elif event.key== pygame.K_z and player.staminaGauge>=80:
                    player.standing= False
                    player.signature= True
                    player.attacking= True
                    player.signatureCount=0
                    player.staminaGauge-=80
                    new_slash= pj.Projectile(player.x, player.feet_y-20,64,64,player.facing)   
                    new_slash.getsugatenshou=True
                    pj.projectiles.append(new_slash)
                    
        keys = pygame.key.get_pressed()
        if not player.attacking:
            if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and player.x > player.vel:
                player.x -= player.vel
                player.left = True
                player.right = False
                player.standing = False
                player.facing= -1
            elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and player.x+ player.width+ player.vel < st.screen_width:
                player.x += player.vel
                player.left = False
                player.right = True
                player.standing = False
                player.facing= 1
            else:
                if not player.dashing:      
                    player.standing = True
                    player.dashCount=0
                player.walkCount = 0

        # Jump logic
        if not player.isJump:
            if keys[pygame.K_UP] or keys[pygame.K_w] :
                player.isJump = True
                player.standing = False
        else:
            if player.jumpCount >= -11:
                neg = 1
                if player.jumpCount < 0: neg = -1
                player.feet_y -= (player.jumpCount ** 2) * 0.5 * neg
                player.x+=player.facing*2
                player.jumpCount -= 1
            else:
                player.jumpCount = 11
                player.isJump = False
                player.feet_y=500

        # Collisions
        for p in pj.projectiles[:]:
            for h in en.hollows:
                if p.colliderect(h.body_hitbox) and player.signatureCount>=21:
                    h.health-=100
                    h.damage=True
                    p.kill()
               

        for h in en.hollows[:]:
            if player.hitbox.colliderect(h.body_hitbox):
                if h.attacking and player.hitbox.colliderect(h.attack_hitbox):
                    if 21 <=h.attackCount <24:
                        player.hit()
                        if not player.down:
                            h.hit= True
                            player.hit()
                elif not player.signature and player.attacking:
                    if player.attackCount==0:
                        h.gothit()
                else:
                    h.hit= False
                    player.stationaryPhase= False
                    player.gotHit=False
            else:
                h.hit= False
                player.stationaryPhase= False
                player.gotHit=False

        redrawwindow()
    pygame.quit()
main()