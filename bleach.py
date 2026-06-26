import pygame
import setup as st
import projectile as pj
import enemy as en
import player as pl
import time
import mainmenu as mm
import levels as lv
import random
import aizen
import ending
clock = pygame.time.Clock()
player = pl.Player(64, 64, 10, st.feet_y_initial)
aizen_boss= aizen.Aizen(900, st.feet_y_initial)
shine_x=-100
DEBUG = False

def hudPannel():
    st.win.blit(st.hud_pannel, (-20,-60))

def draw_bar(x, y, width, height,
             value, max_value,
             color1, color2,
             glow_color,
             animated=False):
    global shine_x
    fill_width = int((value / max_value) * width)
    glow_points = [
        (x + 4, y),
        (x + width, y),
        (x + width - 10, y + height),
        (x, y + height)
    ]
    pygame.draw.polygon(st.win, glow_color, glow_points, 2)

    #GRADIENT FILL
    inner_x = x + 8
    inner_y = y + 2
    inner_width = fill_width - 7
    inner_height = height - 4
    if inner_width > 0:
        for i in range(inner_width):
            ratio = i / inner_width
            r = color1[0] + (color2[0] - color1[0]) * ratio
            g = color1[1] + (color2[1] - color1[1]) * ratio
            b = color1[2] + (color2[2] - color1[2]) * ratio
            pygame.draw.line(
                st.win,
                (int(r), int(g), int(b)),
                (inner_x + i-4, inner_y),
                (inner_x + i-7, inner_y + inner_height+2)
            )

    #BORDER
    pygame.draw.polygon(st.win, (220,220,220), glow_points, 1)

    #ANIMATED SHINE
    if animated:
        shine_x += 6
        if shine_x > width + 80:
            shine_x = -120
        shine_surface = pygame.Surface((width, height),
                                    pygame.SRCALPHA)
        pygame.draw.polygon(
            shine_surface,
            (255,255,255,90),
            [
                (shine_x, 0),
                (shine_x + 25, 0),
                (shine_x - 5, height),
                (shine_x - 30, height)
            ]
        )
        st.win.blit(shine_surface, (x, y))

def redrawwindow():
    st.win.blit(st.bg, (0, 0))
    if not st.scroll:
        st.win.blit(st.ground,(0,st.feet_y_initial+10))
    for e in en.hollows:
        e.move(st.win,player)
    if lv.levelComplete:
        if player.movement_state not in ["idle"]:
            st.scroll=True
        lv.sideScrolling(player)
    if player.mode=="bankai":
        player.health-=1/30
        if player.ultimateGauge>0:
            player.ultimateGauge-=1/30
    hudPannel()
    player.draw(st.win, lv.scroll if lv.levelComplete and st.scroll else 0)
    text= st.font.render(f"Score: {st.score}",1,(255,255,255))
    st.win.blit(text,(st.screen_width-text.get_width()-20, 0))
    text= st.font.render(f"Stage- {lv.i}",1,(255,165,0))
    st.win.blit(text, (st.screen_width//2-text.get_width()+80,100))
    for p in pj.cero[:]:
        p.move(aizen_boss)
        p.draw(st.win,aizen_boss)
    for p in pj.projectiles[:]:
        if player.signatureCount>=21:
            p.move(player)
            p.draw(st.win, lv.scroll if lv.levelComplete and st.scroll else 0, player)
    st.current_time= pygame.time.get_ticks()
    st.current_time_bankai= pygame.time.get_ticks()
    st.current_time_ult=pygame.time.get_ticks()
    if st.show_text:
        if st.killCount==0 and st.current_time-st.text_start_time<= st.text_duration:
            text= st.font.render("Locked! Get a kill",1,(0,0,0))
            st.win.blit(text,(st.screen_width//2-text.get_width()//2, st.screen_height//2-text.get_height()//2))
        else:
            st.show_text= False
    elif st.show_text_bankai:
        if st.current_time_bankai-st.text_start_time_bankai<=st.text_duration_bankai:
            text= st.font.render("Bankai Ready!",1,(0,0,0))
            st.win.blit(text,(st.screen_width//2-text.get_width()//2, st.screen_height//2-text.get_height()//2))
        else:
            st.show_text_bankai=False
    elif st.show_text_ultimate:
        if st.current_time_ult-st.text_start_time_ult<=st.text_duration_ult:
            text=st.font.render("Ultimate Ready",1,(0,0,0))
            st.win.blit(text,(st.screen_width//2-text.get_width()//2, st.screen_height//2-text.get_height()//2))
        else:
            st.show_text_ultimate=False
            
    if st.Mpause:
        st.win.blit(st.mute,(st.screen_width-100,70))
     # HP BAR
    draw_bar(
        150, 58,
        195, 8,
        player.health, 200,
        (120,0,0),
        (255,60,60),
        (255,0,0)
    )
    # STAMINA BAR
    draw_bar(
        150, 145,
        180, 8,
        player.staminaGauge, 100,
        (0,100,180),
        (120,240,255),
        (0,180,255)
    )
    # ULTIMATE BAR
    draw_bar(
        215, 103,
        125, 10,
        player.ultimateGauge, 160,
        (40,0,60),
        (180,0,255),
        (200,100,255),
        animated=True
    )
    if lv.boss and not st.scroll and not lv.levelComplete:
        aizen_boss.move(player)
    pygame.display.update()   

last_enemy_spawn = time.time()

def createEnemies(): 
    global last_enemy_spawn
    if not st.game_state=="mainmenu" and not lv.levelComplete and not lv.boss:
        if len(lv.hollows)==0:
            enemy = en.Enemy(110, 149, 1200, st.feet_y_initial)
            enemy.static_x=1200
            if not st.Mpause:
                st.hollowSound.play(0)
            en.hollows.append(enemy)
            lv.hollows.append(enemy)
        if lv.i<=5:
            if (time.time() - last_enemy_spawn >= lv.levels[lv.i]["spawn_delay"]) and not len(lv.hollows)==lv.hollow:
                enemy = en.Enemy(110, 149, random.randint(0,1)*st.screen_width+random.choice([-1,1]*100), st.feet_y_initial)
                enemy.facing=-1 if enemy.x==st.screen_width else 1
                enemy.static_x=enemy.x
                if not st.Mpause:
                    st.hollowSound.play(0)
                lv.hollows.append(enemy)
                en.hollows.append(enemy)
                last_enemy_spawn = time.time()
        if lv.hollows!=[] and st.killCountperRound==lv.hollow:
            st.killCountperRound=0
            lv.i+=1
            if lv.i>5 and aizen_boss.status=="dead":    
                st.game_state="victory"
            if lv.i<=5:
                lv.hollow,lv.delay,lv.boss=lv.increment()
                lv.hollows.clear()
                lv.levelComplete=True
        
def draw_pause():
    pygame.draw.rect(st.surface,(128,128,128,150),[0,0, st.screen_width,st.screen_height])
    pygame.draw.rect(st.surface,'dark gray',[st.screen_width//2-210,160,440,50],0,12)
    restart= pygame.draw.rect(st.surface,'white',[st.screen_width//2-210,220, 210,50],0,12) 
    mainmenu= pygame.draw.rect(st.surface,'white',[st.screen_width//2+20,220, 210,50],0,12) 
    instructions= pygame.draw.rect(st.surface, 'white',[st.screen_width//2-210,290, 430,50],0,12)
    st.surface.blit(st.font.render("Game Paused: Esc to Resume",True,'black'),(st.screen_width//2-200,160))
    st.surface.blit(st.font.render('Restart',True, 'black'),[st.screen_width//2-150,220, 210,50])
    st.surface.blit(st.font.render('Main Menu',True, 'black'),[st.screen_width//2+50,220, 210,50])
    st.surface.blit(st.font.render('Instructions',True,'black'),[st.screen_width//2-80,290, 430,50])
    st.win.blit(st.surface,(0,0))
    pygame.display.update()
    return restart, mainmenu,instructions

def reset():
    global player, aizen_boss, last_enemy_spawn
    player = pl.Player(64, 64, 10, st.feet_y_initial)
    aizen_boss = aizen.Aizen(900, st.feet_y_initial)  # after fixing #3
    en.hollows.clear()
    pj.projectiles.clear()
    pj.cero.clear()
    st.score = 0
    st.killCount = 0
    st.killCountperRound = 0
    st.show_text = False
    st.scroll = False
    st.ending_sequence = None
    st.lastTeleport = pygame.time.get_ticks()
    st.lastCero = pygame.time.get_ticks()

    st.getsugatenshoSound.stop()
    st.bankaiSound.stop()

    lv.i = 1
    lv.scroll = 0
    lv.levelComplete = False
    lv.hollow, lv.delay, lv.boss = lv.increment()
    lv.hollows.clear()

    last_enemy_spawn = time.time()
    st.pause = False

def enemyDamaged(enemy):
    if player.action=="visored":
        enemy.gothit(player)
        return
    elif 12> player.attackCount>=9:
        enemy.state="attacking"
        enemy.gothit(player)
        if player.action=="combo":
            enemy.health-=10*player.incrementalFactor

def hit(player):
    player.health-=100
    player.hit_state="got_hit"
    player.action="hit"

def main():
    run = True
    st.game_state="mainmenu"
    restart, mainmenu,instructions = None, None,None
    while run:
        clock.tick(30)
        events= pygame.event.get()
        # compute camera offset / screen position early so event handlers can use it
        cam_offset = lv.scroll if (lv.levelComplete and st.scroll) else 0
        screen_x = player.x - cam_offset
        for event in events:
            if event.type == pygame.QUIT:
                run = False
        while st.game_state=="mainmenu":
            mm.draw()
            mm.handleMenu()
        if st.game_state=="instructions":
            mm.instructions()
            for event in events:
                if event.type== pygame.KEYDOWN:
                    if event.key== pygame.K_ESCAPE:
                        if not st.pause:
                            st.game_state="mainmenu"
                        else:
                            st.game_state="start"
                
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
                    elif instructions and instructions.collidepoint(event.pos):
                        st.game_state="instructions"
                if event.type == pygame.KEYDOWN:
                    if not st.pause:
                        if event.key not in st.NON_INTERRUPT_KEYS and event.key in st.EXISTING_KEYS:
                            player.interrupt()    
                        if event.key==pygame.K_m:
                            st.Mpause=not st.Mpause
                            st.pause_music()
                        if not( event.key==pygame.K_l or event.key==pygame.K_i) :
                            if event.key== pygame.K_j and (player.action not in ["dashing"] and not player.jump):
                                if player.action not in ["attacking", "combo"]:
                                    player.action="attacking"
                                    player.stance_state="initial"
                                    player.attackCount=0
                                    player.comboTimer = 10
                                elif player.action=="attacking":
                                    if player.comboTimer>0:
                                        player.combo_state = "queued"
                            elif event.key== pygame.K_LSHIFT:
                                if -player.vel <screen_x< st.screen_width- player.width - player.vel and player.staminaGauge>=20:
                                    if player.jump:
                                        player.air_dash = True
                                        player.dashCount = 0
                                        player.dashTimer = 10
                                        player.x += player.facing * 60 * player.incrementalFactor
                                        if not -player.vel <screen_x< st.screen_width- player.width - player.vel:
                                            if screen_x>st.screen_width- player.width - player.vel:
                                                player.x= st.screen_height-player.width-player.vel
                                            elif screen_x<-player.vel:
                                                player.x=player.vel

                                        player.staminaGauge -= 20
                                    else:
                                        player.interrupt()
                                        player.x += player.facing * 60 * player.incrementalFactor
                                        if not -player.vel <screen_x< st.screen_width- player.width - player.vel:
                                            if screen_x>st.screen_width- player.width - player.vel:
                                                player.x= st.screen_height-player.width-player.vel
                                            elif screen_x<-player.vel:
                                                player.x=player.vel
                                        player.action = "dashing"
                                        player.dashCount = 0
                                        player.staminaGauge -= 20

                            elif event.key== pygame.K_k:
                                if st.killCount!=0 and player.staminaGauge>=90 and not player.jump:
                                    player.interrupt()
                                    player.action="signature"
                                    player.signatureCount=0
                                    player.staminaGauge-=80
                                    for h in en.hollows[:]:
                                        if player.hitbox.colliderect(h.attack_hitbox):
                                            player.action="hit"
                                    new_slash= pj.Projectile(player.x, player.feet_y-10,64,64,player.facing)   
                                    new_slash.getsugatenshou=True
                                    pj.projectiles.append(new_slash)
                                    if not st.Mpause:
                                        st.getsugatenshoSound.play(0)
                                    if player.action=="hit" :
                                        st.getsugatenshoSound.stop()
                                else:
                                    st.show_text= True
                                    st.text_start_time= pygame.time.get_ticks()
                                    redrawwindow()
                        elif event.key==pygame.K_l:
                            if player.mode=="shikai" and player.ultimateGauge>=80:
                                player.activateDeactivateBankai()
                            elif player.mode=="bankai":
                                player.activateDeactivateBankai()
                        elif event.key== pygame.K_i and not st.scroll:
                            if player.mode=="bankai" and player.ultimateGauge>=150:
                                player.ultimateGauge-=150
                                if not st.Mpause:
                                    st.ichigoScream.play(0)
                                player.visoredAttack()
                    if event.key== pygame.K_ESCAPE:
                        if st.pause:
                            st.pause=False
                        else:
                            st.pause=True
                            restart, mainmenu,instructions=draw_pause()
                    

            keys = pygame.key.get_pressed()
            if not st.pause:
                if player.action!="visored":
                    if not player.action=="hitbyCero":
                        if player.action == "attacking" and player.comboTimer > 0:
                            player.comboTimer -= 1
                        elif player.action != "attacking":
                            player.comboTimer = 0

                        if player.transform_state != "activating":
                            if player.action not in ["attacking", "combo", "signature"]:
                                # Determine camera offset and player's screen position
                                cam_offset = lv.scroll if (lv.levelComplete and st.scroll) else 0
                                screen_x = player.x - cam_offset
                                # Prevent player's world x from going left of the camera view
                                min_world_x = cam_offset
                                if player.x < min_world_x:
                                    player.x = min_world_x

                                if ( keys[pygame.K_a]) and screen_x > player.vel:
                                    player.x -= player.vel
                                    player.movement_state = "left"
                                    player.facing= -1
                                    player.action="knockeddown" if player.hit_state in ["got_hit", "stationary"] else player.action
                                elif ( keys[pygame.K_d]) and (screen_x + player.width + player.vel < st.screen_width or (lv.levelComplete and st.scroll)):
                                    player.x += player.vel
                                    player.movement_state = "right"
                                    player.facing= 1
                                    player.action="knockeddown" if player.hit_state in ["got_hit", "stationary"] else player.action
                                else:
                                    if player.action not in ["dashing"] and not player.jump:      
                                        player.action="idle"
                                        player.dashCount=0
                                    player.movement_state = "idle"
                                    player.walkCount = 0

                            # Jump logic
                            if player.transform_state!="activating":
                                if not player.jump:
                                    if keys[pygame.K_w]:
                                        player.jump=True
                                        player.interrupt()
                                else:
                                    if player.jumpCount >= -9:
                                        neg = 1
                                        if player.jumpCount < 0: neg = -1
                                        player.feet_y -= (player.jumpCount ** 2) * 0.5 * neg
                                        player.x+=player.facing*2
                                        player.jumpCount -= 1
                                    else: 
                                        player.jumpCount = 9
                                        player.jump=False
                                        player.feet_y=st.feet_y_initial
                                        player.air_dash = False
                                
                    # Collisions
                    for p in pj.projectiles[:]:
                        if player.signatureCount>=21:
                            if aizen_boss.status=="alive" and lv.boss:
                                if p.colliderect(aizen_boss.hitbox):
                                    if aizen_boss not in p.hitEnemies:
                                        aizen_boss.hit(player.damage//2)
                                        if player.ultimateGauge<160:
                                            st.previousGauge=player.ultimateGauge
                                            player.ultimateGauge+=10
                                            st.bankaiUltimateReady(player,st.previousGauge)
                                            player.ultimateGauge=min(player.ultimateGauge, 160)
                                        p.hitEnemies.append(aizen_boss) 
                                        if aizen_boss.health <= 0:
                                            aizen_boss.status = "dead"
                                            aizen_boss.action = "hit"
                                            st.game_state="victory"
                            for h in en.hollows:
                                if p.colliderect(h.body_hitbox):
                                    if h not in p.hitEnemies:
                                        h.health-=player.damage
                                        p.hitEnemies.append(h)
                                        h.facing=-1*player.facing
                                        if h.state in ["attacking","hit"]:
                                            h.state="idle"
                                        if player.ultimateGauge<160:
                                            st.previousGauge=player.ultimateGauge
                                            player.ultimateGauge+=5
                                            st.bankaiUltimateReady(player,st.previousGauge)
                                            player.ultimateGauge=min(player.ultimateGauge, 160)
                                        h.blown=True
                                        h.blownCount=0
                    
                    for p in pj.cero[:]:
                        if p.colliderect(player.hitbox):
                            player.action="hitbyCero"
                            player.aizen_hit()
                            pj.cero.remove(p)
                    if lv.boss and aizen_boss.status=="alive":
                        if player.attackhitbox!=None and player.attackhitbox.colliderect(aizen_boss.hitbox) and player.action in ["attacking", "combo"]:
                            if player.attackCount>=9 and player.attackCount<=12:
                                aizen_boss.hit(1 * player.incrementalFactor)
                                st.previousGauge=player.ultimateGauge
                                player.ultimateGauge+=5
                                st.bankaiUltimateReady(player,st.previousGauge)
                                if aizen_boss.health <= 0:
                                    aizen_boss.status = "dead"
                                    aizen_boss.action = "hit"
                                    st.game_state="victory"
                        if aizen_boss.hitbox.colliderect(player.hitbox):
                            if aizen_boss.action in ["attack", "jump_attack", "combo_attack"]:
                                player.aizen_hit()
            
                    for h in en.hollows[:]:
                        if player.hitbox.colliderect(h.body_hitbox):
                            if h not in player.hollowattack:
                                player.hollowattack.append(h)
                            if h.state in ["idle"] and not player.jump:
                                h.state="attacking"
                            if player.hitbox.colliderect(h.attack_hitbox):
                                if 21 <=h.attackCount <24 or h.state=="hit":
                                    player.hit()
                            if player.attackhitbox!=None and player.attackhitbox.colliderect(h.body_hitbox):
                                if player.attackCount>=9 and player.attackCount<12 and (player.action in ["attacking", "combo"]):
                                    enemyDamaged(h)
                            if(player.action in ["attacking", "combo"]):
                                enemyDamaged(h)
                        elif player.attackhitbox!=None and player.attackhitbox.colliderect(h.body_hitbox):
                            if player.attackCount>=9 and player.attackCount<=12 and player.action in ["attacking", "combo"]:
                                    enemyDamaged(h)
                        else:
                            if h in player.hollowattack:
                                if h.state not in ["falling", "dead"]:
                                    h.state="idle"
                                player.hit_state= "normal"
                elif player.action in ["visored"]:
                    player.jump=False
                    player.jumpCount=9
                    if player.hitbox.colliderect(aizen_boss.hitbox):
                        if player.visoredCount>=20 and player.visoredCount<=35 and lv.boss and not lv.levelComplete:
                            aizen_boss.hit(20*player.incrementalFactor)
                            st.previousGauge=player.ultimateGauge
                            player.ultimateGauge+=5
                            st.bankaiUltimateReady(player,st.previousGauge)
                            aizen_boss.action="hit"
                            if aizen_boss.health<=0:
                                aizen_boss.status="dead"
                                st.game_state="victory"
                    else:
                        for h in en.hollows[:]:
                            if player.hitbox.colliderect(h.body_hitbox):
                                if player.visoredCount>=20 and player.visoredCount<=35:
                                    enemyDamaged(h)
                if player.health<=0:
                    st.game_state="defeat"
                redrawwindow()
        elif st.game_state == "victory":
            if st.ending_sequence is None:
                time.sleep(1)
                st.ending_sequence = ending.EndingSequence("victory")
            player.feet_y=st.feet_y_initial
            st.ending_sequence.update(player)
            st.ending_sequence.draw(st.win)
            pygame.display.update()
            if st.ending_sequence.is_done():
                st.ending_sequence = None
                reset()
                st.game_state = "mainmenu"

        elif st.game_state == "defeat":
            if st.ending_sequence is None:
                time.sleep(1)
                st.ending_sequence = ending.EndingSequence("defeat")
            st.ending_sequence.update(player)
            st.ending_sequence.draw(st.win)
            pygame.display.update()
            if st.ending_sequence.is_done():
                st.ending_sequence = None
                reset()
                st.game_state = "mainmenu"
    pygame.quit()
main()