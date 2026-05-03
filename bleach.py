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
    pygame.draw.rect(st.win,"cyan",(237,116,180-1.125*(160-player.ultimateGauge),18))
    st.win.blit(st.hud_pannel, (10,10))

def redrawwindow():
    st.win.blit(st.bg, (0, 0))
    hudPannel()
    for e in en.hollows:
        e.move(st.win,player)
    player.draw(st.win)
    text= st.font.render(f"Score: {st.score}",1,(255,255,255))
    st.win.blit(text,(st.screen_width-text.get_width()-20, 0))
    if player.signatureCount>=21:
        for p in pj.projectiles[:]:
           p.move()
           p.draw(st.win)
    st.current_time= pygame.time.get_ticks()
    if st.show_text:
        if st.killCount==0 and st.current_time-st.text_start_time<= st.text_duration:
            text= st.font.render("Locked! Get a kill",1,(255,255,255))
            st.win.blit(text,(st.screen_width//2-text.get_width()//2, st.screen_height//2-text.get_height()//2))
        else:
            st.show_text= False
    st.current_time_bankai= pygame.time.get_ticks()
    if st.current_time_bankai-st.text_start_time_bankai<=st.text_duration_bankai:
        if player.ultimateGauge>=160:
            text= st.font.render("Ultimate Ready!",1,(255,255,255))
            st.win.blit(text,(st.screen_width//2-text.get_width()//2, st.screen_height//2-text.get_height()//2))
    if st.Mpause:
        st.win.blit(st.mute,(st.screen_width-100,70))
    pygame.display.update()   

last_enemy_spawn = time.time()

def createEnemies():
    global last_enemy_spawn
    i=0
    if not st.game_state=="mainmenu":
        if time.time() - last_enemy_spawn >= max(2,10-2*st.killCount):
            while(i!=st.killCount):
                new_enemy = en.Enemy(110+10*i, 149, 1200, 500)
                en.hollows.append(new_enemy)
                i+=1
            i=0
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

def enemyDamaged(enemy):
    if player.attackCount==0:
        if player.facing==enemy.facing:
            enemy.facing*=-1
        enemy.attacking= True
        enemy.gothit(player)
        if player.combo:
            enemy.health-=40*player.incrementalFactor

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
                player.staminaGauge+=1/3*player.incrementalFactor
            for event in events:
                if event.type ==pygame.MOUSEBUTTONDOWN and st.pause:
                    if restart.collidepoint(event.pos):
                        reset()
                    elif mainmenu.collidepoint(event.pos):
                        st.game_state="mainmenu"
                        reset()
                if event.type == pygame.KEYDOWN:
                    if not st.pause:
                        if event.key not in st.NON_INTERRUPT_KEYS:
                            player.interrupt()    
                        if event.key==pygame.K_m:
                            st.Mpause=not st.Mpause
                            st.pause_music()
                        if not event.key==pygame.K_b:
                            if event.key== pygame.K_SPACE:
                                if not player.attacking and not player.combo:
                                    player.standing= False
                                    player.attacking= True
                                    player.signature=False
                                    player.stancephase=0
                                    player.attackCount=0
                                    player.combo = False
                                    player.comboIndex = 0
                                    player.comboTimer = 5
                                elif player.attacking and not player.combo:
                                    player.combo= True
                                    player.comboIndex=1
                                    player.comboTimer=5
                                elif player.combo:
                                    player.comboIndex+=1
                                    player.comboTimer=5
                            
                            elif event.key== pygame.K_LSHIFT:
                                if player.vel < player.x < st.screen_width - player.width - player.vel and player.staminaGauge>=20:
                                    player.interrupt()
                                    player.x+= player.facing*40*player.incrementalFactor
                                    player.standing= False
                                    player.dashing= True
                                    player.dashCount=0
                                    player.staminaGauge-=20
                                    
                            elif event.key== pygame.K_z:
                                if st.killCount!=0 and player.staminaGauge>=90:
                                    player.interrupt()
                                    player.standing= False
                                    player.signature= True
                                    player.attacking= True
                                    player.signatureCount=0
                                    player.staminaGauge-=80
                                    new_slash= pj.Projectile(player.x, player.feet_y-10,64,64,player.facing)   
                                    new_slash.getsugatenshou=True
                                    pj.projectiles.append(new_slash)
                                else:
                                    st.show_text= True
                                    st.text_start_time= pygame.time.get_ticks()
                                    redrawwindow()
                                    pygame.display.update()
                        elif event.key==pygame.K_b and player.ultimateGauge>=160:
                            player.activateBankai()

                    if event.key== pygame.K_ESCAPE:
                        if st.pause:
                            st.pause=False
                        else:
                            st.pause=True
                            restart, mainmenu=draw_pause()

            keys = pygame.key.get_pressed()
            if not st.pause:
                if not player.bankai:
                    if not player.attacking and not player.combo:
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
                                h.health-=player.damage
                                p.hitEnemies.append(h)
                                h.facing=-1*player.facing
                                h.blown=True
                
                for h in en.hollows[:]:
                    if player.hitbox.colliderect(h.body_hitbox):
                        player.hollowattack.append(h)
                        h.attacking=True
                        if player.hitbox.colliderect(h.attack_hitbox):
                            if 21 <=h.attackCount <24:
                                player.hit()
                                if not player.down:
                                    h.hit= True  
                            if player.attackCount==0 and (player.attacking or player.combo and not player.signature):
                                enemyDamaged(h)
                        elif not player.signature and (player.attacking or player.combo):
                            enemyDamaged(h)
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