import pygame
import random
from .settings import CURRENT_SETTINGS, SCREEN_WIDTH, GROUND_Y
from .assets import game_assets

def create_obstacle():
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
        rect = img.get_rect(midbottom=(SCREEN_WIDTH + 100, 100))
        y_speed = 5

    return {"type": obstacle_type, "rect": rect, "img": img, "speed": speed, "y_speed": y_speed}

def move_obstacles(obstacles):
    score_increment = 0
    # Create a copy to modify the list while iterating if we were using a for loop on the list directly
    # But usually it's safer to iterate a copy
    for obstacle in obstacles[:]: 
        obstacle["rect"].x -= obstacle["speed"]
        obstacle["rect"].y += obstacle["y_speed"]
        
        # Remove if off screen
        if obstacle["rect"].right < 0:
            obstacles.remove(obstacle)
            score_increment += 10
    return score_increment

def draw_obstacles(screen, obstacles):
    for obstacle in obstacles:
        screen.blit(obstacle["img"], obstacle["rect"])
