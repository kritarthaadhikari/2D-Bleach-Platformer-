import pygame as py
import enemy as en
import setup as st
global i 
i=1
hollows=[]
levels= {
    1: {"hollows":3, "spawn_delay":20},
    2: {"hollows":5, "spawn_delay":10},
    3: {"hollows":7, "spawn_delay":5},
    4: {"hollows":9, "spawn_delay":2},
    5: {"hollows":2, "spawn_delay":1, "boss": True}
}

levelComplete= False
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
        st.win.blit(st.bg, (0, 0))
        for i in range(0,3):
            st.win.blit(st.ground,(i*st.screen_width - scroll,st.feet_y_initial+10))
        st.win.blit(st.arrow,(1200-scroll,st.feet_y_initial-50))
        if not (player.movement_state in ["idle"] or player.facing==-1) and (player.transform_state!="activating" and player.action!="signature"):
            scroll += 5 if not player.mode=="bankai" else 7 # Move camera right
        if scroll >= st.screen_width:
            player.x-=scroll# Move player back to start of new level
            scroll = 0
            st.scroll= False
            levelComplete= False
         
        # No display.update() here
"""Issues
spamming space while being attacked deals infinite damage
to enemy and also triggers permanent fall animation for 
the player. """