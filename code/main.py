import pygame
import sys
import os
from core.settings import SCREEN_WIDTH, SCREEN_HEIGHT, CAPTION, CURRENT_SETTINGS, BASE_DIR, JUMP_HORIZONTAL_SPEED

# Initialize Pygame
pygame.init()
pygame.mixer.init()

CLOCK = pygame.time.Clock()
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(CAPTION)

# Import modules (after pygame init for asset loading dependencies)
from core.assets import game_assets
from core.player import Player
from core.obstacles import create_obstacle, move_obstacles, draw_obstacles
from core.collision import check_collision
from core.ui import UI
from core.intro_ui import IntroUI
from core.over_ui import GameOverUI
from core.background import Background

# Load Assets
game_assets.load()

# Load Audio
# Basic error handling for missing audio files
intro_music_path = os.path.join(BASE_DIR, "../assets/intro.mp3")
game_music_path = os.path.join(BASE_DIR, "../assets/game_audio.mp3")

has_intro_music = os.path.exists(intro_music_path)
has_game_music = os.path.exists(game_music_path)

def play_music(music_type):
    if music_type == "intro" and has_intro_music:
        pygame.mixer.music.load(intro_music_path)
        pygame.mixer.music.play(-1)
    elif music_type == "game" and has_game_music:
        pygame.mixer.music.load(game_music_path)
        pygame.mixer.music.play(-1)
    else:
        pygame.mixer.music.stop()

# Game Objects
player = Player()
ui = UI()
intro_ui = IntroUI()
game_over_ui = GameOverUI()
background = Background()
obstacle_list = []
score = 0

# Game States: 'intro', 'playing', 'game_over'
game_state = "intro" 
game_paused = False
current_music = None

play_music("intro")
current_music = "intro"

SPAWN_OBSTACLE = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_OBSTACLE, CURRENT_SETTINGS["spawn_rate"])

while True:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        # Global Pause (only if playing)
        if game_state == "playing":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_paused = not game_paused
                # Pause/Unpause music?
                if game_paused:
                    pygame.mixer.music.pause()
                else:
                    pygame.mixer.music.unpause()

    # --- STATE MACHINE ---
    
    if game_state == "intro":
        intro_ui.draw(SCREEN)
        
        # Event handling for intro
        for event in events:
            if intro_ui.handle_event(event) == "start_game":
                game_state = "playing"
        
        if game_state == "playing":
             score = 0
             obstacle_list = []
             player.reset()
             play_music("game")
             current_music = "game"
             
    elif game_state == "playing":
        if not game_paused:
            # 1. Events
            for event in events:
                if event.type == SPAWN_OBSTACLE:
                    target_x = player.rect.centerx if player.rect else player.x_position
                    obstacle_list.append(create_obstacle(target_x))
        
            # 2. Player Update (Determine State)
            keys = pygame.key.get_pressed()
            player_surf, player_rect = player.update(keys)
            
            # 3. Calculate Scroll Boost for Rolling Effect
            scroll_boost = 0
            if player.state == "roll":
                scroll_boost = 10 # Uniform 10px shift for world "moving around player"
            elif player.state == "jump":
                scroll_boost = JUMP_HORIZONTAL_SPEED
            
            # 4. Background Update
            background.update(scroll_boost)
            
            # 5. Obstacle Update
            score_increment = move_obstacles(obstacle_list, scroll_boost)
            score += score_increment
            
            # 6. Collision
            if player_rect and check_collision(player, obstacle_list):
                 game_state = "game_over"
                 play_music("intro")
                 current_music = "intro"
        
        else:
             # Paused Logic
             player_surf, player_rect = player.get_current_surface(), player.rect
             font = pygame.font.Font(None, 60)
             pause_surf = font.render("PAUSED", True, (255, 255, 255))
             pause_rect = pause_surf.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))

        # --- DRAWING PHASE ---
        background.draw(SCREEN)
        
        if player_surf and player_rect:
            SCREEN.blit(player_surf, player_rect)
            
        draw_obstacles(SCREEN, obstacle_list)
        ui.draw_score(SCREEN, score)
        
        if game_paused:
             SCREEN.blit(pause_surf, pause_rect)

    elif game_state == "game_over":
        # Draw game objects static in background for effect
        background.draw(SCREEN)
        # Maybe draw player/obstacles static? Defaults to just background + UI usually looks cleaner
        
        game_over_ui.draw(SCREEN, score)
        
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if game_over_ui.check_click(event.pos):
                    game_state = "playing"
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                 game_state = "playing"
        
        if game_state == "playing":
             score = 0
             obstacle_list = []
             player.reset()
             play_music("game")
             current_music = "game"


    pygame.display.update()
    CLOCK.tick(60)