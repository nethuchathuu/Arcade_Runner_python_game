import pygame
import os
from .settings import ASSETS_PATH, SCREEN_WIDTH, SCREEN_HEIGHT

# Initialize pygame display if not already (needed for convert methods usually, but assets might be loaded before init in some structures. 
# However, pygame.image.load works without display.set_mode, but convert() needs it. 
# We'll assume pygame.init() and display.set_mode are called in main before importing assets or strictly strictly lazy load.)
# Actually main.py calls init() then imports. But if we import assets at top level of main, we need display initialized for convert().
# We'll rely on main.py initializing pygame first. But imports happen before main execution if modules are imported at top.
# To be safe, we can wrap loading in a function or assume init is done. 
# Better: Just use load_image function and call it? 
# Original main.py loaded assets at top level. 
# We'll define functions to get assets or load them globally if pygame is ready.
# Main.py does: pygame.init(), then helper functions, then creates surfaces.
# Wait, main.py imports usually run immediately. 
# If I import core.assets in main.py, it runs this code. 
# So main.py must `pygame.init()` BEFORE `from core.assets import ...`? 
# No, imports are usually at top. `pygame.init()` at line 5.
# This means I should probably lazy load or make sure pygame.init() is successful.
# Or, I can just not use `.convert()` at import time if display isn't ready.
# But `convert()` is good for performance.
# I'll modify main.py to init pygame before importing core modules if they do eager loading.
# OR: separate "constants" (paths) from "loaded surfaces".
# The user asked for `assets.py`. I'll put loading logic there.
# I'll verify if `pygame.display.set_mode` is needed for `convert()`. Docs say `convert()` requires a display mode set? Actually yes, usually.
# So I will define a function `load_all_assets()` that main.py calls after init.

def load_image(filename, scale_size=None, remove_bg=False):
    path = os.path.join(ASSETS_PATH, filename)
    try:
        surface = pygame.image.load(path)
    except FileNotFoundError:
        print(f"Error: {filename} not found at {path}")
        surface = pygame.Surface(scale_size if scale_size else (50, 50))
        surface.fill((255, 0, 0))
        return surface

    if remove_bg:
        # Attempt to remove background (assume top-left pixel color is background)
        # Note: convert() requires pygame display initialized
        if pygame.display.get_surface(): 
             surface = surface.convert()
        colorkey = surface.get_at((0, 0))
        surface.set_colorkey(colorkey)
    else:
        if pygame.display.get_surface():
            surface = surface.convert_alpha()

    if scale_size:
        surface = pygame.transform.scale(surface, scale_size)
    
    return surface

class Assets:
    def __init__(self):
        self.standing_surface = None
        self.run_frames = []
        self.roll_frames = []
        self.jump_frames = []
        self.background = None
        self.car_img = None
        self.bird_img = None
        self.missile_img = None
        self.bomb_img = None

    def load(self):
        self.standing_surface = load_image("standing.png", (120, 180))
        
        # Load running animation frames
        self.run_frames = [
            load_image("runGLeft.png", (160, 200)),
            load_image("runGRight.png", (160, 200))
        ]
        
        self.roll_frames = [
             load_image(f"roll{i}.png", (120, 90), remove_bg=True) for i in range(1, 8)
        ]

        self.jump_frames = [
            load_image(f"jump{i}.png", (130, 185)) for i in range(1, 6)
        ]
        
        self.background = load_image("background.jpg", (SCREEN_WIDTH, SCREEN_HEIGHT))
        
        self.car_img = load_image("carO.png", (150, 90))
        self.bird_img = load_image("birdO.png", (100, 70))
        self.missile_img = load_image("missileO.png", (110, 60))
        self.bomb_img = load_image("bombO.png", (90, 90))

game_assets = Assets()
