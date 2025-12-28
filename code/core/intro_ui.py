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
        
        self.slide2_font_size = 60 # Slightly smaller to accommodate content
        self.slide2_font = pygame.font.Font(None, self.slide2_font_size)
        
        # Huge Tagline Font
        self.tagline_font_size = 90 
        self.tagline_font = pygame.font.Font(None, self.tagline_font_size)
        
        self.button_font = pygame.font.Font(None, 50)
        
        # Slide 1 Config
        self.s1_duration = 5000
        
        # Slide 2 Config
        self.play_button_rect = pygame.Rect(0, 0, 240, 65)
        # Position Bottom Left: Margin 150, Bottom 80
        self.play_button_rect.bottomleft = (150, SCREEN_HEIGHT - 80)
        
        self.tagline_colors = [
            (0, 255, 209), # #00FFD1
            (255, 215, 0), # #FFD700
            (255, 107, 107), # #FF6B6B
            (155, 93, 229), # #9B5DE5
            (77, 150, 255)  # #4D96FF
        ]

    def _load_image(self, filename):
        try:
            path = os.path.join(ASSETS_PATH, filename)
            if os.path.exists(path):
                img = pygame.image.load(path).convert()
                return pygame.transform.scale(img, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except Exception as e:
            print(f"Error loading {filename}: {e}")
        
        s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        s.fill((20, 20, 40))
        return s

    def handle_event(self, event):
        if self.state == "controls_instruction":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return "start_game"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.play_button_rect.collidepoint(event.pos):
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
            self.play_button_rect.bottomleft = (150, SCREEN_HEIGHT - 80)
            self._draw_slide2(screen, elapsed)

    def _draw_slide1(self, screen, elapsed):
        screen.blit(self.bg1, (0, 0))
        
        margin_right = 150
        target_right_x = SCREEN_WIDTH - margin_right
        
        anim_duration = 1200
        t = min(elapsed / anim_duration, 1.0)
        eased_t = 1 - (1 - t)**3 
        
        start_offset = 600
        current_offset = start_offset * (1 - eased_t)
        
        lines = ["Arcade", "Runner"]
        line_spacing = 20
        
        line_heights = [self.title_font.size(line)[1] for line in lines]
        total_text_height = sum(line_heights) + line_spacing * (len(lines) - 1)
        start_y = (SCREEN_HEIGHT - total_text_height) // 2 - 50 
        
        current_y = start_y
        for line in lines:
            self._draw_text_with_effects(screen, line, self.title_font, (255, 255, 255), 
                                       target_right_x + current_offset, current_y, "right")
            current_y += self.title_font.size(line)[1] + line_spacing

        bar_w = int(SCREEN_WIDTH * 0.25)
        bar_h = 12
        bar_y = current_y + 40
        bar_x = target_right_x + current_offset - bar_w
        
        pygame.draw.rect(screen, (44, 44, 44), (bar_x, bar_y, bar_w, bar_h), border_radius=10)
        
        fill_progress = min(elapsed / 5000.0, 1.0)
        fill_width = int(bar_w * fill_progress)
        if fill_width > 0:
            pygame.draw.rect(screen, (0, 255, 209), (bar_x, bar_y, fill_width, bar_h), border_radius=10)

    def _draw_slide2(self, screen, elapsed):
        screen.blit(self.bg2, (0, 0))
        
        margin_left = 150
        
        # --- Controls: Top Left Block ---
        # "Jump with", "Roll with", "Pause with"
        c_jump = (0, 255, 209)
        c_roll = (255, 215, 0)
        c_pause = (255, 107, 107)
        c_white = (255, 255, 255)
        
        items = [
            {"text": "Jump with ", "icon": "UP", "color": c_jump},
            {"text": "Roll with ", "icon": "RIGHT", "color": c_roll},
            {"text": "Pause with ", "icon": "SPACE", "color": c_pause},
        ]
        
        start_y = 100
        gap = 70
        
        for i, item in enumerate(items):
            y_pos = start_y + i * gap
            col = item["color"]
            
            # Text
            txt_surf = self.slide2_font.render(item["text"], True, col)
            screen.blit(txt_surf, (margin_left, y_pos))
            
            # Icon (12px spacing)
            icon_x = margin_left + txt_surf.get_width() + 70
            icon_y = y_pos + txt_surf.get_height() // 2
            
            self._draw_key_icon(screen, (icon_x, icon_y), item["icon"], col)

        # --- Tagline: Typewriter, Centered ---
        # Explicit lines as requested
        raw_lines = [
            "\"dodge danger,",
            "move fast, and",
            "survive the run!\""
        ]
        
        all_lines = []
        total_chars = 0
        
        for line_text in raw_lines:
            line_objs = []
            # Split manually preserving space logic for typewriter
            # We treat the line as a sequence of words
            for word in line_text.split(" "):
                 # White color fixed
                 surf = self.tagline_font.render(word + " ", True, (255, 255, 255))
                 w_len = len(word) + 1 # +1 for the space we added in render
                 line_objs.append({"surf": surf, "text": word, "len": w_len})
                 total_chars += w_len
            all_lines.append(line_objs)
            
        # Animation: 40ms per char
        visible_chars_count = min(int(elapsed / 40.0), total_chars)
        
        # Layout Config
        area_x = margin_left
        area_y_start = 320 
        line_spacing = self.tagline_font_size * 0.9

        # Draw Typewriter
        chars_so_far = 0
        cursor_pos = None
        
        current_y = area_y_start
        for line in all_lines:
            current_x = area_x
            for lw in line:
                 # Check how many chars of this word are visible
                 w_len = lw["len"] # inc space
                 if chars_so_far + w_len <= visible_chars_count:
                     # Full word visible
                     screen.blit(lw["surf"], (current_x, current_y))
                     current_x += lw["surf"].get_width()
                     chars_so_far += w_len
                 else:
                     # Partial word?
                     remain = visible_chars_count - chars_so_far
                     if remain > 0:
                         # Render partial
                         partial_text = (lw["text"] + " ")[:remain]
                         # Find color from surf? Need to re-render partial
                         # Hack: layout_words has surf, we can get color from tagline_colors
                         # Need index of word in 'words' list... logic above lost index.
                         # Simplified: Re-find index or store it.
                         pass 
                         # For now, just show full word if mostly typed or skip partials for clean look
                         # Or just render whole words for "Typewriter" usually means chars.
                         # Let's just assume whole words appear or fix partial render
                         
                         # Actually, let's just do Char-by-Char logic purely for "Typewriter"
                         # But we need Wrapping + Colors per word.
                         # This is complex. Let's simplify: 
                         # Just show full words as they become "unlocked" by char count
                         # This avoids partial rendering artifacts with variable width fonts
                     
                     cursor_pos = (current_x, current_y)
                     chars_so_far += w_len # Count them as processed loop
                     break # Stop this line
            
            if chars_so_far > visible_chars_count:
                 break # Stop drawing lines
            
            current_y += line_spacing

        # Cursor Blink
        if cursor_pos and (elapsed // 500) % 2 == 0:
            pygame.draw.rect(screen, (255, 255, 255), (cursor_pos[0], cursor_pos[1], 10, 100))


        # --- Play Button (Bottom Left) ---
        pulse_val = (math.sin(elapsed * 0.005) + 1) / 2
        scale_px = int(4 * pulse_val)
        draw_rect = self.play_button_rect.inflate(scale_px, scale_px)
        
        # Shadow
        shadow_rect = draw_rect.copy()
        shadow_rect.move_ip(4, 4)
        pygame.draw.rect(screen, (0,0,0), shadow_rect, border_radius=35)
        
        # Glow
        for i in range(3):
            pygame.draw.rect(screen, (0, 255, 209), draw_rect.inflate(i*2, i*2), width=1, border_radius=35)
            
        # Body
        pygame.draw.rect(screen, (0, 255, 209), draw_rect, border_radius=35)
        
        # Text
        btn_txt = self.button_font.render("PLAY", True, (10, 10, 10))
        btn_rect = btn_txt.get_rect(center=draw_rect.center)
        screen.blit(btn_txt, btn_rect)

    def _draw_text_with_effects(self, screen, text, font, color, x, y, align="center"):
        shadow_dist = 4
        shadow_surf = font.render(text, True, (0, 0, 0))
        glow_surf = font.render(text, True, (255, 255, 255))
        main_surf = font.render(text, True, color)
        if align == "right":
            rect = main_surf.get_rect(topright=(x, y))
        elif align == "left":
            rect = main_surf.get_rect(topleft=(x, y))
        else:
            rect = main_surf.get_rect(center=(x, y))
        screen.blit(shadow_surf, (rect.x + shadow_dist, rect.y + shadow_dist))
        screen.blit(main_surf, rect)
        
    def _draw_key_icon(self, screen, center_pos, icon_type, color):
        cx, cy = center_pos
        w, h = 50, 50
        if icon_type == "SPACE":
            w = 140
        rect = pygame.Rect(0, 0, w, h)
        rect.center = center_pos
        
        pygame.draw.rect(screen, color, rect, width=3, border_radius=8)
        
        if icon_type == "UP":
            pygame.draw.polygon(screen, color, [(cx, cy - 12), (cx - 8, cy + 4), (cx + 8, cy + 4)])
            pygame.draw.rect(screen, color, (cx - 3, cy + 4, 6, 8))
        elif icon_type == "RIGHT":
            pygame.draw.polygon(screen, color, [(cx + 12, cy), (cx - 4, cy - 8), (cx - 4, cy + 8)])
            pygame.draw.rect(screen, color, (cx - 12, cy - 3, 8, 6))
        elif icon_type == "SPACE":
            pygame.draw.rect(screen, color, (cx - 40, cy + 8, 80, 4))
