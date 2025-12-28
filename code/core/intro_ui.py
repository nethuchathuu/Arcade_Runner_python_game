import pygame
import os
import math
from .settings import SCREEN_WIDTH, SCREEN_HEIGHT, ASSETS_PATH

class IntroUI:
    def __init__(self):
        self.state = "title_loading" # title_loading, controls_instruction
        self.start_time = pygame.time.get_ticks()
        
        # --- Load Assets ---
        self.bg1 = self._load_image("intro_bg.jpg")
        self.bg2 = self._load_image("intro_bg2.jpg")
        
        # Fonts
        self.title_font_size = 150
        self.title_font = pygame.font.Font(None, self.title_font_size)
        self.heading_font = pygame.font.Font(None, 48)
        self.action_font = pygame.font.Font(None, 32)
        self.note_font = pygame.font.Font(None, 24)
        
        # Slide 1 Config
        self.s1_duration = 5000
        
        # Slide 2 Config
        self.controls = [
            {"key": "UP ARROW", "action": "Jump (hold to jump higher)", "anim": "slide_left"},
            {"key": "RIGHT ARROW", "action": "Roll forward to avoid bombs", "anim": "slide_right"},
            {"key": "SPACE", "action": "Start / Pause Game", "anim": "fade_in"}
        ]

    def _load_image(self, filename):
        try:
            path = os.path.join(ASSETS_PATH, filename)
            if os.path.exists(path):
                img = pygame.image.load(path).convert()
                return pygame.transform.scale(img, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except Exception as e:
            print(f"Error loading {filename}: {e}")
        
        # Fallback surface
        s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        s.fill((20, 20, 40))
        return s

    def handle_event(self, event):
        """
        Handles events for the Intro UI.
        Returns 'start_game' if the game should start, else None.
        """
        if self.state == "controls_instruction":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return "start_game"
            if event.type == pygame.MOUSEBUTTONDOWN:
                return "start_game"
        return None

    def draw(self, screen):
        current_time = pygame.time.get_ticks()
        elapsed = current_time - self.start_time
        
        if self.state == "title_loading":
            if elapsed >= self.s1_duration:
                self.state = "controls_instruction"
                self.start_time = current_time
                elapsed = 0
            
            self._draw_slide1(screen, elapsed)
            
        elif self.state == "controls_instruction":
            self._draw_slide2(screen, elapsed)

    def _draw_slide1(self, screen, elapsed):
        # -- Background --
        screen.blit(self.bg1, (0, 0))
        
        # -- Config --
        margin_right = 150
        target_right_x = SCREEN_WIDTH - margin_right
        
        # Animation: Slide In from Right
        anim_duration = 1200
        t = min(elapsed / anim_duration, 1.0)
        eased_t = 1 - (1 - t)**3 # Ease out cubic
        
        # Start from off-screen right
        start_offset = 600
        current_offset = start_offset * (1 - eased_t)
        
        # Text "Arcade\nRunner"
        lines = ["Arcade", "Runner"]
        line_spacing = 20
        
        # Calculate total height to center vertically
        # Font height approx 3/4 of size usually, but let's measure
        line_heights = [self.title_font.size(line)[1] for line in lines]
        total_text_height = sum(line_heights) + line_spacing * (len(lines) - 1)
        
        start_y = (SCREEN_HEIGHT - total_text_height) // 2 - 50 # slightly higher to make room for bar
        
        current_y = start_y
        for line in lines:
            # Glow/Shadow
            self._draw_text_with_effects(screen, line, self.title_font, (255, 255, 255), 
                                       target_right_x + current_offset, current_y, "right")
            current_y += self.title_font.size(line)[1] + line_spacing

        # -- Loading Bar --
        # 25% width
        bar_w = int(SCREEN_WIDTH * 0.25)
        bar_h = 12
        bar_y = current_y + 40 # Below text
        
        # Align right to same margin
        bar_x = target_right_x + current_offset - bar_w
        
        # Draw Background Bar
        pygame.draw.rect(screen, (44, 44, 44), (bar_x, bar_y, bar_w, bar_h), border_radius=10)
        
        # Fill animation
        fill_progress = min(elapsed / 5000.0, 1.0)
        fill_width = int(bar_w * fill_progress)
        
        if fill_width > 0:
            # Fill color #00FFD1 -> (0, 255, 209)
            pygame.draw.rect(screen, (0, 255, 209), (bar_x, bar_y, fill_width, bar_h), border_radius=10)

    def _draw_slide2(self, screen, elapsed):
        # -- Background --
        screen.blit(self.bg2, (0, 0))
        
        # -- Heading --
        fade_dur = 900
        alpha = min(elapsed / fade_dur, 1.0) * 255
        
        heading_surf = self.heading_font.render("How to Play", True, (255, 255, 255))
        heading_surf.set_alpha(int(alpha))
        heading_rect = heading_surf.get_rect(center=(SCREEN_WIDTH // 2, 100))
        screen.blit(heading_surf, heading_rect)
        
        # -- Controls --
        start_y = 250
        gap = 80
        
        for i, item in enumerate(self.controls):
            item_y = start_y + i * gap
            
            # Stagger animations
            item_delay = i * 300
            item_elapsed = elapsed - item_delay
            
            display_x = SCREEN_WIDTH // 2
            
            if item_elapsed < 0:
                continue 
                
            alpha_val = 255
            
            if item["anim"] == "slide_left": 
                progress = min(item_elapsed / 600.0, 1.0)
                eased = 1 - (1 - progress)**2
                start_x_pos = -400
                display_x = start_x_pos + (SCREEN_WIDTH // 2 - start_x_pos) * eased
                
            elif item["anim"] == "slide_right":
                progress = min(item_elapsed / 600.0, 1.0)
                eased = 1 - (1 - progress)**2
                start_x_pos = SCREEN_WIDTH + 400
                display_x = start_x_pos + (SCREEN_WIDTH // 2 - start_x_pos) * eased
                
            else: # fade_in
                display_x = SCREEN_WIDTH // 2
                alpha_val = min(item_elapsed / 800.0, 1.0) * 255
                
            text = f"{item['key']}: {item['action']}"
            t_surf = self.action_font.render(text, True, (255, 255, 255))
            if alpha_val < 255:
                t_surf.set_alpha(int(alpha_val))
                
            t_rect = t_surf.get_rect(center=(display_x, item_y))
            screen.blit(t_surf, t_rect)

        # -- Note (Pulse) --
        pulse_val = (math.sin(elapsed * (2 * math.pi / 1200)) + 1) / 2
        
        tip_text = "Tip: Rolling helps you escape falling bombs!"
        r = int(150 + 105 * pulse_val)
        g = int(120 + 95 * pulse_val)
        b = 0
        
        tip_surf = self.note_font.render(tip_text, True, (r, g, b))
        tip_rect = tip_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100))
        screen.blit(tip_surf, tip_rect)

    def _draw_text_with_effects(self, screen, text, font, color, x, y, align="center"):
        # Shadow
        shadow_dist = 4
        shadow_surf = font.render(text, True, (0, 0, 0))
        
        # Glow (Simulated with outlines)
        glow_color = (255, 255, 255)
        glow_surf = font.render(text, True, glow_color)
        
        main_surf = font.render(text, True, color)
        
        if align == "right":
            rect = main_surf.get_rect(topright=(x, y))
        elif align == "left":
            rect = main_surf.get_rect(topleft=(x, y))
        else:
            rect = main_surf.get_rect(center=(x, y))
            
        # Draw Shadow
        screen.blit(shadow_surf, (rect.x + shadow_dist, rect.y + shadow_dist))
        
        # Draw Glow (simple 1px outline for now to save perf, or blit multiple times)
        # Using 2px offset for "glow" feel
        glow_offsets = [(-2, 0), (2, 0), (0, -2), (0, 2), (-1, -1), (1, 1), (-1, 1), (1, -1)]
        for dx, dy in glow_offsets:
             screen.blit(glow_surf, (rect.x + dx, rect.y + dy))
             
        # Main Text
        screen.blit(main_surf, rect)
