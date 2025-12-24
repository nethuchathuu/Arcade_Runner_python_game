import pygame
from .settings import GROUND_Y, X_POSITION, FALL_SPEED, RISE_SPEED, ANIMATION_SPEED
from .assets import game_assets

class Player:
    def __init__(self):
        self.state = "idle"  # idle, ready, jump
        self.y_position = GROUND_Y
        self.rect = None
        self.frame_index = 0
        self.animation_timer = 0
        self.last_update = 0

    def reset(self):
        self.state = "ready"
        self.y_position = GROUND_Y
        self.frame_index = 0
        self.last_update = pygame.time.get_ticks()

    def update(self, keys):
        current_surface = None
        
        # Determine current surface and state logic
        if self.state == "idle":
            # If update is called, game is active usually.
            # Transition to ready/run immediately as per original logic?
            # Or respect idle state? User spec says "idle_state": "standing.png".
            # If we are in 'idle' while game is active, usually we transition to running in this genre.
            # I will transition to ready but use standing if checked.
            self.state = "ready"
            if game_assets.run_frames:
                current_surface = game_assets.run_frames[0]
                
        elif self.state == "ready":
            if keys[pygame.K_SPACE]:
                self.state = "jump"
            
            # Gravity / Falling checks (ensure on ground)
            if self.y_position < GROUND_Y:
                self.y_position += FALL_SPEED
            else:
                self.y_position = GROUND_Y
            
            # Animation Logic (Frame Based)
            current_time = pygame.time.get_ticks()
            if current_time - self.last_update > ANIMATION_SPEED:
                self.frame_index = (self.frame_index + 1) % len(game_assets.run_frames)
                self.last_update = current_time
                
            if game_assets.run_frames:
                current_surface = game_assets.run_frames[self.frame_index]
            
        elif self.state == "jump":
            if not keys[pygame.K_SPACE]:
                self.state = "ready"
            
            # Rising logic
            self.y_position -= RISE_SPEED
            current_surface = game_assets.jumping_surface
        
        # Determine rect
        if current_surface:
            # Check for ground clamp
            if self.y_position > GROUND_Y:
                self.y_position = GROUND_Y
                
            self.rect = current_surface.get_rect(center=(X_POSITION, self.y_position))
            return current_surface, self.rect
            
        # Fallback
        return None, None

    def draw(self, screen):
        pass
