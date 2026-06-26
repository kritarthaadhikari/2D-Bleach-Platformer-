import pygame
import setup as st
import sys
menu=pygame.transform.scale(pygame.image.load('images/setup/mainmenu.jpg'),(1280,720)).convert()

def draw():
    st.win.blit(menu,(0,0))
    playquit_text= pygame.transform.scale(pygame.image.load('images/setup/playquit.png').convert_alpha(), (400, 300))
    st.win.blit(playquit_text,(st.screen_width//2-200, st.screen_height//2+80))
    play_rect=pygame.Rect(st.screen_width//2-170, st.screen_height//2+120, 340, 70)
    instruct_rect= pygame.Rect(st.screen_width//2-170,st.screen_height//2+205, 340,70)
    quit_rect = pygame.Rect(st.screen_width//2-170, st.screen_height//2+285, 340, 70)

    pygame.display.update()
    return play_rect,instruct_rect,quit_rect

def handleMenu():
    play_rect, instruct_rect, quit_rect = draw()
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_m:
                st.Mpause=not st.Mpause
                st.pause_music()
        if event.type==pygame.MOUSEBUTTONDOWN:
            if play_rect.collidepoint(event.pos):
                st.game_state="start"
            elif instruct_rect.collidepoint(event.pos):
                st.game_state="instructions"
            elif quit_rect.collidepoint(event.pos):
                pygame.quit()
                quit()

def instructions():
    st.win.fill((20, 45, 72))
    st.win.blit(st.instructions,(290,0))
    pygame.display.update()

