import pygame
import random
from .settings import CURRENT_SETTINGS, SCREEN_WIDTH, GROUND_Y
from .assets import game_assets

def create_obstacle(player_x=None):
    obstacle_type = random.choice(["car", "bird", "missile", "bomb"])
    speed = random.randint(*CURRENT_SETTINGS["speed_range"])
    
    img = None
    rect = None
    y_speed = 0
    
    if obstacle_type == "car":
        img = game_assets.car_img
        rect = img.get_rect(midbottom=(SCREEN_WIDTH + 100, GROUND_Y + 40))
        y_speed = 0
    elif obstacle_type == "bird":
        img = game_assets.bird_img
        y_pos = random.randint(100, 300)
        rect = img.get_rect(midbottom=(SCREEN_WIDTH + 100, y_pos))
        y_speed = 0
    elif obstacle_type == "missile":
        img = game_assets.missile_img
        y_pos = random.randint(300, 500)
        rect = img.get_rect(midbottom=(SCREEN_WIDTH + 100, y_pos))
        y_speed = 0
    elif obstacle_type == "bomb":
        img = game_assets.bomb_img
        # Bomb spawns directly above player's current X
        spawn_x = player_x if player_x is not None else 200
        rect = img.get_rect(midbottom=(spawn_x, -50)) # Start above screen
        y_speed = speed # Matches the speed of other obstacles (running speed)
        speed = 0 # No X movement for bombs

    return {"type": obstacle_type, "rect": rect, "img": img, "speed": speed, "y_speed": y_speed}

def move_obstacles(obstacles):
    score_increment = 0
    for obstacle in obstacles[:]: 
        
        # Apply movement based on type configuration (implicit by speed values set in create)
        if obstacle["type"] == "bomb":
             obstacle["rect"].y += obstacle["y_speed"]
             # Bounds check for bomb (bottom of screen)
             if obstacle["rect"].top > GROUND_Y: # Hit ground
                 obstacles.remove(obstacle)
                 # Bombs don't give score when hitting ground? Or maybe they do.
                 # User said "increase on obstacle passed". 
                 # For falling bomb, avoiding it means it hits ground.
                 score_increment += 10
        else:
             obstacle["rect"].x -= obstacle["speed"]
             # Bounds check for side moving obstacles
             if obstacle["rect"].right < 0:
                 obstacles.remove(obstacle)
                 score_increment += 10
                 
    return score_increment

def draw_obstacles(screen, obstacles):
    for obstacle in obstacles:
        screen.blit(obstacle["img"], obstacle["rect"])
