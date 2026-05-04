import pygame as py
import enemy as en
import random
import setup as st

levels= {
    1: {"hollows":3, "spawn_delay":20},
    2: {"hollows":5, "spawn_delay":10},
    3: {"hollows":7, "spawn_delay":5},
    4: {"hollows":9, "spawn_delay":2},
    5: {"hollows":2, "spawn_delay":1, "boss": True}
}
i=1
if(levels[i]):
    hollow= levels[i]["hollows"]
    delay= levels[i]["spawn_delay"]