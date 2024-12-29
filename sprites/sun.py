import pygame
import random
from settings import *

class Sun(pygame.sprite.Sprite):
    def __init__(self, x, y, value=25):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.set_colorkey(BLACK)  # Make black background transparent
        self.rect = self.image.get_rect()
        
        # Position and movement
        self.rect.x = x
        self.rect.y = y
        self.target_y = y + random.randint(20, 50)  # Random drop distance
        self.y = float(self.rect.y)  # For precise position tracking
        self.y_speed = 2  # Falling speed
        
        # Properties
        self.value = value
        self.creation_time = pygame.time.get_ticks()
        self.lifetime = SUN_LIFETIME
        
        # Draw pixel art sun
        self.draw_sun()
        
    def draw_sun(self):
        # Main sun body (yellow square with orange border)
        sun_color = YELLOW
        border_color = (255, 165, 0)  # Orange
        
        # Draw main body
        pygame.draw.rect(self.image, border_color, (2, 2, 26, 26))
        pygame.draw.rect(self.image, sun_color, (4, 4, 22, 22))
        
        # Add highlights
        highlight_color = (255, 255, 200)  # Light yellow
        pygame.draw.rect(self.image, highlight_color, (6, 6, 8, 8))
        pygame.draw.rect(self.image, highlight_color, (8, 8, 4, 4))
        
    def update(self, game):
        # Update position
        if self.rect.y < self.target_y:
            self.y += self.y_speed
            self.rect.y = int(self.y)
            
        # Check lifetime
        current_time = pygame.time.get_ticks()
        if current_time - self.creation_time > self.lifetime:
            self.kill()
            
    def collect(self):
        self.kill()
        return self.value
