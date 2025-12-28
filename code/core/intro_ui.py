import pygame
from .settings import SCREEN_WIDTH, SCREEN_HEIGHT

class IntroUI:
    def __init__(self):
        # Using default fonts for now, or consider loading a specific font if assets have one.
        # Assets list didn't show fonts.
        self.large_font = pygame.font.Font(None, 80)
        self.medium_font = pygame.font.Font(None, 40)
        self.small_font = pygame.font.Font(None, 30)
        
        self.play_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 100, 200, 60)
        
        # Determine audio path
        # Audio loading should happen in main or assets usually, but UI might hold reference or trigger plays.
        # "assets/intro.mp3" logic is handled in valid logic.

    def draw(self, screen):
        screen.fill((30, 30, 30)) # Dark background
        
        # Title
        title_surf = self.large_font.render("Arcade Runner", True, (255, 200, 50))
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
        
        # Animation effect (simple vertical offset based on time)
        offset_y = 0 # Placeholder for animation logic if time is passed in
        # We can implement simple "throb" or "slide" if we had a tick counter. 
        # For now static is fine, or simple time based calc:
        ticks = pygame.time.get_ticks()
        offset_y = (ticks // 200) % 10 - 5
        
        screen.blit(title_surf, (title_rect.x, title_rect.y + offset_y))
        
        # Instructions
        instructions = [
            ("UP ARROW", "Jump"),
            ("RIGHT ARROW", "Roll"),
            ("LEFT ARROW", "Stop"),
            ("SPACE", "Start/Pause")
        ]
        
        start_y = SCREEN_HEIGHT // 2 - 50
        for idx, (key, action) in enumerate(instructions):
            text = f"{key}: {action}"
            instr_surf = self.small_font.render(text, True, (200, 200, 200))
            rect = instr_surf.get_rect(center=(SCREEN_WIDTH // 2, start_y + idx * 30))
            screen.blit(instr_surf, rect)

        # Play Button
        # Check hover
        mouse_pos = pygame.mouse.get_pos()
        color = (0, 255, 100) if self.play_button_rect.collidepoint(mouse_pos) else (0, 200, 80)
        
        # Draw button with simple shadow/depth
        pygame.draw.rect(screen, (0, 150, 60), self.play_button_rect.move(0, 5), border_radius=10)
        pygame.draw.rect(screen, color, self.play_button_rect, border_radius=10)
        
        btn_text = self.medium_font.render("PLAY", True, (255, 255, 255))
        btn_text_rect = btn_text.get_rect(center=self.play_button_rect.center)
        screen.blit(btn_text, btn_text_rect)

    def check_click(self, pos):
        if self.play_button_rect.collidepoint(pos):
            return True
        return False
