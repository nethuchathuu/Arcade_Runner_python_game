import pygame
from .settings import SCREEN_WIDTH, SCREEN_HEIGHT, X_POSITION, GROUND_Y
from .assets import game_assets

class UI:
    def __init__(self):
        # Ensure font module is initialized if not already (pygame.init handles it)
        if not pygame.font.get_init():
            pygame.font.init()
        self.font = pygame.font.Font(None, 50)
        self.score_color = (64, 64, 64)
        self.msg_color = (111, 196, 169)

    def draw_score(self, screen, score):
        score_surf = self.font.render(f'Score: {score}', True, self.score_color)
        score_rect = score_surf.get_rect(center=(SCREEN_WIDTH/2, 50))
        screen.blit(score_surf, score_rect)

    def draw_start_screen(self, screen):
        # Draw standing player
        if game_assets.standing_surface:
            mario_rect = game_assets.standing_surface.get_rect(center=(X_POSITION, GROUND_Y))
            screen.blit(game_assets.standing_surface, mario_rect)
        
        msg = self.font.render('Press Space to Start', True, self.msg_color)
        msg_rect = msg.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
        screen.blit(msg, msg_rect)

    def draw_game_over(self, screen, score):
        if game_assets.standing_surface:
            mario_rect = game_assets.standing_surface.get_rect(center=(X_POSITION, GROUND_Y))
            screen.blit(game_assets.standing_surface, mario_rect)
        
        msg = self.font.render(f'Game Over! Score: {score}', True, self.msg_color)
        msg_rect = msg.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
        screen.blit(msg, msg_rect)
