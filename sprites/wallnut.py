import pygame
from settings import *
from .plant import Plant

class WallNut(Plant):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.cost = WALLNUT_COST
        self.health = WALLNUT_HEALTH
        self.max_health = WALLNUT_HEALTH
        
        # Draw pixel art wallnut
        # Main body
        nut_color = (139, 69, 19)  # Brown
        pygame.draw.rect(self.image, nut_color, (
            10, 10,
            self.image.get_width() - 20,
            self.image.get_height() - 20
        ))
        
        # Highlights
        highlight_color = (160, 82, 45)
        pygame.draw.rect(self.image, highlight_color, (
            12, 12,
            8, 8
        ))
        pygame.draw.rect(self.image, highlight_color, (
            20, 15,
            6, 6
        ))
        
        # Face features
        # Eyes
        eye_color = (101, 67, 33)  # Dark brown
        # Left eye
        pygame.draw.rect(self.image, eye_color, (
            25, 25,
            8, 8
        ))
        # Right eye
        pygame.draw.rect(self.image, eye_color, (
            45, 25,
            8, 8
        ))
        
        # Mouth (slightly worried expression)
        pygame.draw.rect(self.image, eye_color, (
            30, 40,
            20, 4
        ))
        
    def update(self, game):
        pass  # 墙果不需要特殊的更新逻辑
