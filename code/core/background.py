from .settings import SCREEN_WIDTH, SCREEN_HEIGHT, SCROLL_SPEED
from .assets import game_assets

class Background:
    def __init__(self):
        self.image = game_assets.background
        # Two positions for seamless scrolling
        self.x1 = 0
        self.x2 = SCREEN_WIDTH
        self.speed = SCROLL_SPEED

    def update(self, extra_speed=0):
        # Move both backgrounds to the left
        current_speed = self.speed + extra_speed
        self.x1 -= current_speed
        self.x2 -= current_speed

        # Check if off-screen (reset to the right of the other image)
        if self.x1 <= -SCREEN_WIDTH:
            self.x1 = SCREEN_WIDTH
        
        if self.x2 <= -SCREEN_WIDTH:
            self.x2 = SCREEN_WIDTH

    def draw(self, screen):
        screen.blit(self.image, (self.x1, 0))
        screen.blit(self.image, (self.x2, 0))
