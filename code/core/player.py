import pygame
from .settings import (
    GROUND_Y, X_POSITION, ANIMATION_SPEED, JUMP_FRAME_DURATION, GRAVITY,
    JUMP_VELOCITY, JUMP_HORIZONTAL_SPEED, EXTRA_FORCE_HOLDING, MAX_HOLD_TIME,
    MAX_JUMP_HEIGHT, MAX_FORWARD_DISPLACEMENT, ROLL_SPEED, ROLL_FRAME_DURATION
)
from .assets import game_assets

class Player:
    def __init__(self):
        self.state = "idle"  # idle, ready, jump, roll, run
        self.y_position = GROUND_Y
        self.rect = None
        self.frame_index = 0
        self.animation_timer = 0
        self.last_update = 0
        self.jump_start_time = 0
        self.vel_y = 0
        self.vel_x = 0
        self.x_position = X_POSITION
        self.current_img = None
        self.roll_offset = 45 # Offset to align roll (ht 90) with standing (ht 180) bottom

    def reset(self):
        self.state = "ready"
        self.y_position = GROUND_Y
        self.x_position = X_POSITION
        self.frame_index = 0
        self.vel_y = 0
        self.vel_x = 0
        self.last_update = pygame.time.get_ticks()
        self.initial_jump_y = GROUND_Y

    def get_current_surface(self):
         return self.current_img

    def update(self, keys):
        current_surface = None
        current_time = pygame.time.get_ticks()
        
        # State Management
        if self.state == "idle":
            self.state = "ready"
        
        # Input Handling (State Transitions)
        if self.state in ["ready", "run"]:
            if keys[pygame.K_RIGHT]:
                self.state = "roll"
                self.frame_index = 2 # Start directly at loop frames (roll3)
                self.last_update = current_time
            elif keys[pygame.K_UP]:
                self.state = "jump"
                self.vel_y = JUMP_VELOCITY
                self.vel_x = JUMP_HORIZONTAL_SPEED
                self.jump_start_time = current_time
                self.initial_jump_y = self.y_position
            elif keys[pygame.K_LEFT]:
                self.state = "stop"
                self.frame_index = 0
                self.vel_x = 0
        
        # --- State Behavior ---
        
        # STOP STATE
        if self.state == "stop":
            if keys[pygame.K_LEFT]:
                 # Stay idle/stopped
                 self.vel_x = 0
                 # Use standing/idle frame
                 current_surface = game_assets.standing_surface
            else:
                 self.state = "ready"
        
        # ROLL STATE
        if self.state == "roll":
             if keys[pygame.K_RIGHT]:
                 # Continuous Roll
                 self.vel_x = ROLL_SPEED
                 # self.x_position += self.vel_x 
                 self.y_position = GROUND_Y # Lock Y to ground
                 
                 # Loop Animation (Frames 3,4,5 -> indices 2,3,4)
                 if current_time - self.last_update > ROLL_FRAME_DURATION:
                     self.frame_index += 1
                     if self.frame_index > 4: # Loop back to 2 after 4
                         self.frame_index = 2
                     self.last_update = current_time
                 
                 # Safety check for index
                 if self.frame_index < 2 or self.frame_index > 4:
                     self.frame_index = 2
                     
                 current_surface = game_assets.roll_frames[self.frame_index] if game_assets.roll_frames else None
             else:
                 # Key released, exit roll immediately
                 self.state = "ready"
                 self.frame_index = 0
                 # Optional: Ensure we don't carry extra velocity
                 self.vel_x = 0
        
        # JUMP STATE
        elif self.state == "jump":
            time_since_jump = current_time - self.jump_start_time
            
            # Additional force while holding UP
            if keys[pygame.K_UP]:
                if time_since_jump < MAX_HOLD_TIME:
                     current_height = self.initial_jump_y - self.y_position
                     if current_height < MAX_JUMP_HEIGHT:
                         self.vel_y += EXTRA_FORCE_HOLDING
            
            # Physics
            self.vel_y += GRAVITY
            self.y_position += self.vel_y
            # self.x_position += JUMP_HORIZONTAL_SPEED # Handled by background scroll
            
            # Landing Check
            if self.y_position >= GROUND_Y:
                self.y_position = GROUND_Y
                self.state = "ready"
                self.vel_y = 0
            
            # Animation Sync (Variable Height Jump logic for frames)
            # Sync rule: short press (1-3), long press (1-5).
            # We approximate this by mapping vertical velocity to frames, 
            # which naturally reflects the jump arc.
            # Frames 1-5. 
            # 1: Launch (-16), 2: Rise, 3: Peak/High Rise, 4: Fall Start, 5: Land
            if game_assets.jump_frames:
                frame_count = len(game_assets.jump_frames)
                if frame_count >= 5:
                    if self.vel_y < -10: idx = 0 # Launch
                    elif self.vel_y < -4: idx = 1 # Rise
                    elif self.vel_y < 2:  idx = 2 # Peak (approx 0)
                    elif self.vel_y < 10: idx = 3 # Fall
                    else: idx = 4 # Landing
                    
                    # Clamp index
                    idx = max(0, min(idx, frame_count - 1))
                    current_surface = game_assets.jump_frames[idx]
                else:
                    current_surface = game_assets.jump_frames[0]

        # READY/RUN STATE (Fallback)
        if self.state in ["ready", "run"]:
             # Run Animation
             if current_time - self.last_update > ANIMATION_SPEED:
                 self.frame_index = (self.frame_index + 1) % len(game_assets.run_frames)
                 self.last_update = current_time
             
             if game_assets.run_frames:
                 current_surface = game_assets.run_frames[self.frame_index]
             
             # Movement Clamp/Reset in Ready
             # Actually 'ready' implies running on ground in this game.
             self.y_position = GROUND_Y
        
        # Clamp Forward Position
        max_x = X_POSITION + MAX_FORWARD_DISPLACEMENT
        if self.x_position > max_x:
            self.x_position = max_x
            
        # Determine Rect
        if current_surface:
             self.current_img = current_surface
             # If rolling, shift center Y down to align bottom
             draw_y = self.y_position
             if self.state == "roll":
                 draw_y += self.roll_offset
                 
             self.rect = current_surface.get_rect(center=(int(self.x_position), int(draw_y)))
             return current_surface, self.rect
            
        return None, None
    
    def draw(self, screen):
        if self.current_img and self.rect:
            screen.blit(self.current_img, self.rect)
