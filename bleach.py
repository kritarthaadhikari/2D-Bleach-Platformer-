import pygame
import setup as st
import projectile as pj
import enemy as en
import player as pl
import time
import mainmenu as mm

clock = pygame.time.Clock()
player = pl.Player(64, 64, 10, 500)
enemy = en.Enemy(110, 149, 1200, 500)
en.hollows.append(enemy)


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
        if e.health==0:
            if player.health<=80:
                player.health+=40
    player.draw(st.win)
    text= st.font.render(f"Score: {st.score}",1,(255,255,255))
    st.win.blit(text,(st.screen_width-text.get_width()-20, 0))
    if player.signatureCount>=21:
        for p in pj.projectiles[:]:
           p.move()
           p.draw(st.win)
    if st.killCount==0 and st.pressed:
        text= st.font.render("Locked! Get a kill",1,(255,255,255))
        st.win.blit(text,(st.screen_width//2-text.get_width()//2, st.screen_height//2-text.get_height()//2))
    pygame.display.update()   

last_enemy_spawn = time.time()

def createEnemies():
    global last_enemy_spawn
    if time.time() - last_enemy_spawn >= 30:
        new_enemy = en.Enemy(110, 149, 1200, 500)
        en.hollows.append(new_enemy)
        last_enemy_spawn = time.time()

def draw_pause():
    pygame.draw.rect(st.surface,(128,128,128,150),[0,0, st.screen_width,st.screen_height])
    pygame.draw.rect(st.surface,'dark gray',[st.screen_width//2-210,160,440,50],0,12)
    reset= pygame.draw.rect(st.surface,'white',[st.screen_width//2-210,220, 210,50],0,12) 
    save= pygame.draw.rect(st.surface,'white',[st.screen_width//2+20,220, 210,50],0,12) 
    st.surface.blit(st.font.render("Game Paused: Esc to Resume",True,'black'),(st.screen_width//2-200,160))
    st.surface.blit(st.font.render('Restart',True, 'black'),[st.screen_width//2-150,220, 210,50])
    st.surface.blit(st.font.render('Main Menu',True, 'black'),[st.screen_width//2+50,220, 210,50])
    st.win.blit(st.surface,(0,0))
    pygame.display.update()
    return reset, save

def reset():
    global player,enemy, last_enemy_spawn
    # Reset player
    player = pl.Player(64, 64, 10, 500)

    # Reset enemies
    en.hollows.clear()
    enemy = en.Enemy(110, 149, 1200, 500)
    en.hollows.append(enemy)

    # Reset projectiles
    pj.projectiles.clear()

    # Reset stats
    st.score = 0
    st.killCount = 0
    st.pressed = False

    # Reset timers
    last_enemy_spawn = time.time()
    # Unpause
    st.pause = False

def main():
    run = True
    st.game_state="mainmenu"
    while run:
        clock.tick(22)
        events= pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                run = False
        while st.game_state=="mainmenu":
            mm.draw()
            mm.handleMenu()
          
        if st.game_state=="start":
            createEnemies()
            if player.staminaGauge<100:
                player.staminaGauge+=1/3
            for event in events:
                if event.type ==pygame.MOUSEBUTTONDOWN and st.pause:
                    if restart.collidepoint(event.pos):
                        reset()
                if event.type == pygame.KEYDOWN:
                    if not st.pause:
                        if event.key== pygame.K_SPACE:
                            player.standing= False
                            player.attacking= True
                            player.signature=False
                            player.stancephase=0
                            if player.comboTimer>0:
                                player.comboIndex+=1
                                player.comboTimer-=1
                            else:
                                player.comboIndex=0
                                player.comboTimer=10

                        elif event.key== pygame.K_LSHIFT:
                            if player.vel < player.x < st.screen_width - player.width - player.vel and player.staminaGauge>=20:
                                player.x+= player.facing*40
                                player.standing= False
                                player.dashing= True
                                player.dashCount=0
                                player.staminaGauge-=20
                
                        elif event.key== pygame.K_z and player.staminaGauge>=90:
                            st.pressed=True
                            if st.killCount!=0:
                                player.standing= False
                                player.signature= True
                                player.attacking= True
                                player.signatureCount=0
                                player.staminaGauge-=80
                                new_slash= pj.Projectile(player.x, player.feet_y-10,64,64,player.facing)   
                                new_slash.getsugatenshou=True
                                pj.projectiles.append(new_slash)
                                st.pressed=False
                            else:
                                redrawwindow()
                                pygame.display.update()
                        else:
                            st.pressed=False

                    if event.key== pygame.K_ESCAPE:
                        if st.pause:
                            st.pause=False
                        else:
                            st.pause=True
                            restart, mainmenu=draw_pause()

            keys = pygame.key.get_pressed()
            if not st.pause:
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
                            if h not in p.hitEnemies:
                                h.health-=200
                                p.hitEnemies.append(h)
                                if p.direction != h.facing:
                                    h.blown=True
                                else:
                                    h.blown=False
                
                for h in en.hollows[:]:
                    if player.hitbox.colliderect(h.body_hitbox):
                        player.hollowattack.append(h)
                        if h.attacking and player.hitbox.colliderect(h.attack_hitbox):
                            if 21 <=h.attackCount <24:
                                player.hit()
                                if not player.down:
                                    h.hit= True
                                    player.hit()
                        elif not player.signature and player.attacking:
                            if player.attackCount==0:
                                if player.facing==h.facing:
                                    h.facing*=-1
                                h.attacking= True
                                h.gothit()
                                if player.combo:
                                    h.health-=40
                        else:
                            h.hit= False
                            player.stationaryPhase= False
                            player.gotHit=False
                    else:
                        if h in player.hollowattack:
                            h.hit= False
                            player.stationaryPhase= False
                            player.gotHit= False
                if player.health<=0:
                    st.game_state="gameover"
                redrawwindow()
        elif st.game_state=="gameover":
            text=st.font.render("Game Over! Try again",1,(255,255,255))
            st.win.blit(text,(st.screen_width//2-150, st.screen_height//2-50))
            pygame.display.update()
            time.sleep(2)
            reset()
            st.game_state="start"
            pygame.display.update()
    pygame.quit()
main()