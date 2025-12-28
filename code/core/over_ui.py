import pygame
from .settings import SCREEN_WIDTH, SCREEN_HEIGHT

class GameOverUI:
    def __init__(self):
        self.large_font = pygame.font.Font(None, 80)
        self.medium_font = pygame.font.Font(None, 50)
        self.small_font = pygame.font.Font(None, 30)
        
        self.play_again_rect = pygame.Rect(SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 + 50, 240, 60)

    def draw(self, screen, score):
        # Translucent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))
        
        # Game Over Text
        # Simple "shake" or flash logic could be here if we tracked frames.
        ticks = pygame.time.get_ticks()
        color_g = 50 + (ticks % 500) // 5 
        
        text_surf = self.large_font.render("GAME OVER", True, (255, color_g, 50))
        text_rect = text_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
        screen.blit(text_surf, text_rect)
        
        # Score
        score_surf = self.medium_font.render(f"Score: {score}", True, (255, 255, 255))
        score_rect = score_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
        screen.blit(score_surf, score_rect)
        
        # Play Again Button
        mouse_pos = pygame.mouse.get_pos()
        color = (255, 100, 100) if self.play_again_rect.collidepoint(mouse_pos) else (200, 50, 50)
        
        pygame.draw.rect(screen, (150, 30, 30), self.play_again_rect.move(0, 5), border_radius=10)
        pygame.draw.rect(screen, color, self.play_again_rect, border_radius=10)
        
        btn_text = self.small_font.render("PLAY AGAIN", True, (255, 255, 255))
        btn_text_rect = btn_text.get_rect(center=self.play_again_rect.center)
        screen.blit(btn_text, btn_text_rect)

    def check_click(self, pos):
        if self.play_again_rect.collidepoint(pos):
            return True
        return False
