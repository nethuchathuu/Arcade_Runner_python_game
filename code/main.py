import pygame
import sys
from core.settings import SCREEN_WIDTH, SCREEN_HEIGHT, CAPTION, CURRENT_SETTINGS

# Initialize Pygame
pygame.init()
CLOCK = pygame.time.Clock()
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(CAPTION)

# Import modules (after pygame init for asset loading dependencies)
from core.assets import game_assets
from core.player import Player
from core.obstacles import create_obstacle, move_obstacles, draw_obstacles
from core.collision import check_collision
from core.ui import UI
from core.background import Background

# Load Assets
game_assets.load()

# Game Objects
player = Player()
ui = UI()
background = Background()
obstacle_list = []
score = 0
game_active = False

SPAWN_OBSTACLE = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_OBSTACLE, CURRENT_SETTINGS["spawn_rate"])

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if game_active:
            if event.type == SPAWN_OBSTACLE:
                obstacle_list.append(create_obstacle())
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                player.reset()
                obstacle_list.clear() # Clear obstacles on restart
                score = 0

    # Draw Background
    if game_active:
        background.update()
    background.draw(SCREEN)

    if game_active:
        # Input Handling & Player Update
        keys = pygame.key.get_pressed()
        player_surf, player_rect = player.update(keys)
        
        # Draw Player
        if player_surf and player_rect:
            SCREEN.blit(player_surf, player_rect)
        
        # Obstacle Logic
        score_increment = move_obstacles(obstacle_list)
        score += score_increment
        draw_obstacles(SCREEN, obstacle_list)
        
        # Collision
        if check_collision(player_rect, obstacle_list):
            game_active = False
            # set player to idle or just stop
            game_active = False 
            
        ui.draw_score(SCREEN, score)
        
    else:
        if score == 0:
            ui.draw_start_screen(SCREEN)
        else:
            ui.draw_game_over(SCREEN, score)

    pygame.display.update()
    CLOCK.tick(60)