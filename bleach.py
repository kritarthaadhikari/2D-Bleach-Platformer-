import pygame
import setup as st
import projectile as pj
import enemy as en
import player as pl
import time
import mainmenu as mm
import levels as lv
import random

clock = pygame.time.Clock()
player = pl.Player(64, 64, 10, 500)

def hudPannel():
    pygame.draw.rect(st.win,(255,0,0),(212,59,212,23))
    pygame.draw.rect(st.win,(0,255,0),(212,59,212- 53*(120-player.health)/30,22 ))
    pygame.draw.rect(st.win,(255,255,0),(175,89,188-(100-player.staminaGauge)*1.88,14))
    pygame.draw.rect(st.win,"cyan",(237,116,180-1.125*(160-player.ultimateGauge),18))
    st.win.blit(st.hud_pannel, (10,10))

def redrawwindow():
    if not (lv.levelComplete or  st.scroll):
        st.win.blit(st.bg, (0, 0))
    for e in en.hollows:
        e.move(st.win,player, lv.scroll if lv.levelComplete and st.scroll else 0)
    if lv.levelComplete:
        st.win.blit(st.arrow,(1100-lv.scroll,450))
        if player.action not in ["idle", "jump"] and player.facing==1:
            st.scroll=True
            lv.sideScrolling(player)
        else:
            st.scroll=False
    hudPannel()
    player.draw(st.win, lv.scroll if lv.levelComplete and st.scroll else 0)
    text= st.font.render(f"Score: {st.score}",1,(255,255,255))
    st.win.blit(text,(st.screen_width-text.get_width()-20, 0))
    if player.signatureCount>=21:
        for p in pj.projectiles[:]:
           p.move()
           p.draw(st.win, lv.scroll if lv.levelComplete and st.scroll else 0)
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

    if not st.game_state=="mainmenu" and not lv.levelComplete:
        if len(lv.hollows)==0:
            enemy = en.Enemy(110, 149, 1200, 500)
            en.hollows.append(enemy)
            lv.hollows.append(enemy)
        if (time.time() - last_enemy_spawn >= lv.levels[lv.i]["spawn_delay"]) and not len(lv.hollows)==lv.hollow:
            enemy = en.Enemy(110, 149, random.randint(0,1)*st.screen_width+random.choice([-1,1]*100), 500)
            enemy.facing=-1 if enemy.x==st.screen_width else 1
            lv.hollows.append(enemy)
            en.hollows.append(enemy)
            last_enemy_spawn = time.time()
        if lv.hollows!=[] and st.killCount==lv.hollow:
            st.killCount=0
            lv.i+=1
            lv.hollow,lv.delay=lv.increment()
            lv.hollows.clear()
            lv.levelComplete=True
        
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

    lv.i=1
    # Reset timers
    last_enemy_spawn = time.time()
    # Unpause
    st.pause = False

def enemyDamaged(enemy):
    if player.attackCount==0:
        if player.facing==enemy.facing:
            enemy.facing*=-1
        enemy.state="attacking"
        enemy.gothit(player)
        if player.action=="combo":
            enemy.health-=40*player.incrementalFactor

def main():
    run = True
    st.game_state="mainmenu"
    restart, mainmenu = None, None
    while run:
        clock.tick(22)
        print(player.action)
        print(player.hit_state)
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
                    if restart and restart.collidepoint(event.pos):
                        reset()
                    elif mainmenu and mainmenu.collidepoint(event.pos):
                        st.game_state="mainmenu"
                        reset()
                if event.type == pygame.KEYDOWN:
                    if not st.pause:
                        if event.key not in st.NON_INTERRUPT_KEYS and event.key in st.EXISTING_KEYS:
                            player.interrupt()    
                        if event.key==pygame.K_m:
                            st.Mpause=not st.Mpause
                            st.pause_music()
                        if not event.key==pygame.K_b:
                            if event.key== pygame.K_SPACE and player.action not in ["dashing", "jump"]:
                                if player.action not in ["attacking", "combo"]:
                                    player.action="attacking"
                                    player.stance_state="initial"
                                    player.attackCount=0
                                    player.comboTimer = 10
                                elif player.action=="attacking":
                                    if player.comboTimer>0:
                                        player.combo_state = "queued"
                            elif event.key== pygame.K_LSHIFT:
                                if player.vel < player.x < st.screen_width - player.width - player.vel and player.staminaGauge>=20:
                                    if player.action == "jump":
                                        player.air_dash = True
                                        player.dashCount = 0
                                        player.dashTimer = 10
                                        player.x += player.facing * 40 * player.incrementalFactor
                                        player.staminaGauge -= 20
                                    else:
                                        player.interrupt()
                                        player.x += player.facing * 40 * player.incrementalFactor
                                        player.action = "dashing"
                                        player.dashCount = 0
                                        player.staminaGauge -= 20

                            elif event.key== pygame.K_z:
                                if st.killCount!=0 and player.staminaGauge>=90:
                                    player.interrupt()
                                    player.action="signature"
                                    player.signatureCount=0
                                    player.staminaGauge-=80
                                    new_slash= pj.Projectile(player.x, player.feet_y-10,64,64,player.facing)   
                                    new_slash.getsugatenshou=True
                                    pj.projectiles.append(new_slash)
                                    st.getsugatenshoSound.play(0)
                                else:
                                    st.show_text= True
                                    st.text_start_time= pygame.time.get_ticks()
                                    redrawwindow()
                        elif event.key==pygame.K_b:
                            if player.mode=="shikai" and player.ultimateGauge>=160:
                                player.activateDeactivateBankai()
                            elif player.mode=="bankai":
                                player.activateDeactivateBankai()
                    if event.key== pygame.K_ESCAPE:
                        if st.pause:
                            st.pause=False
                        else:
                            st.pause=True
                            restart, mainmenu=draw_pause()

            keys = pygame.key.get_pressed()
            if not st.pause:
                if player.action == "attacking" and player.comboTimer > 0:
                    player.comboTimer -= 1
                elif player.action != "attacking":
                    player.comboTimer = 0

                if player.transform_state != "activating":
                    if player.action not in ["attacking", "combo", "signature"] and player.transform_state!= "activating":
                        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and player.x > player.vel:
                            player.x -= player.vel
                            player.movement_state = "left"
                            player.facing= -1
                            player.action="knockeddown" if player.hit_state in ["got_hit", "stationary"] else player.action
                        elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and (player.x+ player.width+ player.vel < st.screen_width or (lv.levelComplete and st.scroll)):
                            player.x += player.vel
                            player.movement_state = "right"
                            player.facing= 1
                            player.action="knockeddown" if player.hit_state in ["got_hit", "stationary"] else player.action
                        else:
                            if player.action not in ["dashing", "jump"]:      
                                player.action="idle"
                                player.dashCount=0
                            player.movement_state = "idle"
                            player.walkCount = 0

                    # Jump logic
                    if player.action != "jump":
                        if keys[pygame.K_UP] or keys[pygame.K_w] :
                            player.action="jump"
                    else:
                        if player.jumpCount >= -11:
                            neg = 1
                            if player.jumpCount < 0: neg = -1
                            player.feet_y -= (player.jumpCount ** 2) * 0.5 * neg
                            player.x+=player.facing*2
                            player.jumpCount -= 1
                        else:
                            player.jumpCount = 11
                            player.action="idle"
                            player.feet_y=500
                            player.air_dash = False

                # Collisions
                for p in pj.projectiles[:]:
                    for h in en.hollows:
                        if p.colliderect(h.body_hitbox) and player.signatureCount>=21:
                            if h not in p.hitEnemies:
                                h.health-=player.damage
                                p.hitEnemies.append(h)
                                h.facing=-1*player.facing
                                h.state="blown"
                
                for h in en.hollows[:]:
                    if player.hitbox.colliderect(h.body_hitbox):
                        player.hollowattack.append(h)
                        if h.state=="idle":
                            h.state="attacking"
                        if player.hitbox.colliderect(h.attack_hitbox):
                            if 21 <=h.attackCount <24:
                                player.hit()
                                if player.action != "knockeddown":
                                    if h.state=="attacking":
                                        h.state="hit"  
                            if player.attackCount==0 and (player.action in ["attacking", "combo"]):
                                enemyDamaged(h)
                        elif(player.action in ["attacking", "combo"]):
                            enemyDamaged(h)
                        else:
                            if h.state!="falling" and h.state!="dead":
                                h.state="idle"
                            player.hit_state= "normal"
                    else:
                        if h in player.hollowattack:
                            if h.state not in ["falling", "dead"]:
                                h.state="idle"
                            player.hit_state= "normal"
                if player.health<=0:
                    st.game_state="gameover"
                redrawwindow()
        elif st.game_state=="gameover":
            text=st.font.render("Game Over! Try again",1,(255,255,255))
            st.win.blit(text,(st.screen_width//2-150, st.screen_height//2-50))
            pygame.display.update()
            time.sleep(1)
            reset()
            st.game_state="start"
            pygame.display.update()
    pygame.quit()
main()