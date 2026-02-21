import pygame
import setup as st
menu= pygame.transform.scale(pygame.image.load('images/mainmenu.jpg'),(st.screen_width,st.screen_height))

def draw():
    st.win.blit(menu,(0,0))
    play_text= st.fontmm.render('PLAY', True,(255, 191, 0))
    play_rect=play_text.get_rect(center=(st.screen_width//2, st.screen_height//2+120))
    st.win.blit(play_text,play_rect)

    quit_text = st.fontmm.render('QUIT', True, (255, 191, 0))
    quit_rect = quit_text.get_rect(center=(st.screen_width//2, st.screen_height//2 + 220))
    st.win.blit(quit_text, quit_rect)

    pygame.display.update()
    return play_rect, quit_rect

def handleMenu():
    play_rect,quit_rect= draw()
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            quit()

        if event.type==pygame.MOUSEBUTTONDOWN:
            if play_rect.collidepoint(event.pos):
                st.game_state= "start"
            elif quit_rect.collidepoint(event.pos):
                pygame.quit()
                quit()

