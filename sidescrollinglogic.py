import pygame
import time
pygame.init()

clock= pygame.time.Clock()
Screen_width = 1200
Screen_height = 600
win = pygame.display.set_mode((Screen_width, Screen_height))
pygame.display.set_caption('Side Scrolling Logic Test')
bg= pygame.image.load("images/setup/background.png")
bg= pygame.transform.scale(bg, (Screen_width, Screen_height))
arrow= pygame.transform.flip(pygame.transform.smoothscale(pygame.image.load('images/setup/arrow.png'),(64,64)),True, False)
#scrolling parameters
scroll=0
run= True
while run:
    clock.tick(60)
    for i in range(0,3):
        win.blit(bg,(i*Screen_width+scroll,0))
        win.blit(arrow,(0,0))
    scroll-=5
    if abs(scroll)>Screen_width:
        scroll=0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run= False
    pygame.display.update()