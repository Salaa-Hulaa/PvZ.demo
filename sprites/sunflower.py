import pygame
import math
from settings import *
from .plant import Plant
from .sun import Sun

class Sunflower(Plant):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.cost = SUNFLOWER_COST
        self.health = SUNFLOWER_HEALTH
        self.max_health = SUNFLOWER_HEALTH
        self.sun_generation_time = SUN_GENERATION_TIME
        self.last_sun_time = pygame.time.get_ticks()
        self.sun_generation_amount = 25
        
        # Draw pixel art sunflower
        # Center
        center = (self.image.get_width() // 2, self.image.get_height() // 2)
        center_radius = 10
        pygame.draw.rect(self.image, (139, 69, 19), (  # Brown center
            center[0] - center_radius,
            center[1] - center_radius,
            center_radius * 2,
            center_radius * 2
        ))
        
        # Pixel details in center
        pygame.draw.rect(self.image, (101, 67, 33), (  # Darker brown
            center[0] - center_radius + 2,
            center[1] - center_radius + 2,
            4, 4
        ))
        pygame.draw.rect(self.image, (101, 67, 33), (
            center[0] + center_radius - 6,
            center[1] + center_radius - 6,
            4, 4
        ))
        
        # Petals
        petal_color = (255, 255, 0)  # Yellow
        petal_highlight = (255, 223, 0)  # Darker yellow
        for i in range(8):
            angle = i * (math.pi / 4)  # 8 petals evenly spaced
            # Calculate petal position
            offset_x = int(20 * math.cos(angle))
            offset_y = int(20 * math.sin(angle))
            
            # Draw rectangular petal
            petal_rect = pygame.Rect(
                center[0] + offset_x - 5,
                center[1] + offset_y - 5,
                10, 10
            )
            pygame.draw.rect(self.image, petal_color, petal_rect)
            
            # Add highlight to petal
            highlight_rect = pygame.Rect(
                petal_rect.left + 2,
                petal_rect.top + 2,
                3, 3
            )
            pygame.draw.rect(self.image, petal_highlight, highlight_rect)
            
    def update(self, game):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_sun_time >= self.sun_generation_time:
            # Create a new sun
            sun = Sun(self.rect.centerx, self.rect.centery)
            game.suns.add(sun)
            game.all_sprites.add(sun)
            self.last_sun_time = current_time
