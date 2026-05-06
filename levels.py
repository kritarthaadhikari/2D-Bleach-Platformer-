import pygame as py
import enemy as en
import random
import player
import setup as st
global i 
i=1
hollows=[]
levels= {
    1: {"hollows":3, "spawn_delay":2},
    2: {"hollows":5, "spawn_delay":10},
    3: {"hollows":7, "spawn_delay":5},
    4: {"hollows":9, "spawn_delay":2},
    5: {"hollows":2, "spawn_delay":1, "boss": True}
}

levelComplete= True
global scroll 
scroll=0
hollow= levels[i]["hollows"]
delay= levels[i]["spawn_delay"]
def increment():
    hollow= levels[i]["hollows"]
    delay= levels[i]["spawn_delay"]
    return hollow, delay

def sideScrolling(player):
    global levelComplete
    levelComplete= True
    global scroll
    if st.scroll:
        for i in range(0,3):
            st.win.blit(st.bg,(i*st.screen_width - scroll,0))  # Note: -scroll to move left
        scroll += 5  # Move camera right
        if scroll > st.screen_width:
            scroll = 0
            st.scroll= False
            levelComplete= False
            player.x-=st.screen_width  # Move player back to start of new level
        # No display.update() here
"""Issues
spamming space while being attacked deals infinite damage
to enemy and also triggers permanent fall animation for 
the player. """